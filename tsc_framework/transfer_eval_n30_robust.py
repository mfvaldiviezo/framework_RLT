#!/usr/bin/env python3
"""
transfer_eval_n30_robust.py — Evaluacion de Transferencia Zero-Shot Robusta
============================================================================
Modulo de evaluacion experimental para probar politicas de control semaforico
bajo transferencia zero-shot con N=30 episodios por combinacion. Calcula
metricas de rendimiento, sustentabilidad y pruebas estadisticas robustas
(Mann-Whitney U, Kruskal-Wallis con correccion post-hoc de Bonferroni,
y correlacion de Spearman) sin incluir interpretaciones subjetivas.

Uso:
    python transfer_eval_n30_robust.py [opciones]

Salidas:
    outputs/results/{prefix}_detailed.csv
    outputs/results/{prefix}_summary.csv
    outputs/results/{prefix}_report.md
"""

# ─── Imports ────────────────────────────────────────────────────────────────

import argparse
import csv
import sys
import os
import time
import random
import logging
import subprocess
import tempfile
import shutil
import warnings
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Set
import xml.etree.ElementTree as ET
import numpy as np

# Resolver directorios del proyecto
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

warnings.filterwarnings("ignore")

try:
    from stable_baselines3 import PPO
    from stable_baselines3.common.utils import set_random_seed
    from src.core.tsc_env import TSCEnv
    from src.rl_agent.sarg_policy import HSARGExtractor
except ImportError as e:
    print(f"Error al importar dependencias. Detalle: {e}")
    sys.exit(1)

# Configurar logging basico
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# ─── Configuración y Constantes ─────────────────────────────────────────────

CITY_CONFIGS: List[Tuple[str, str, Optional[float]]] = [
    ("Barcelona", "barcelona.net.xml", None),
    ("Quito", "quito.net.xml", 0.4),
    ("Bogota", "bogota.net.xml", 0.4),
    ("Berlin", "berlin.net.xml", None),
    ("Madrid", "madrid.net.xml", None),
    ("CDMX", "cdmx.net.xml", 0.4)
]

CHAOS_VC_MAPPING: Dict[str, float] = {
    "low": 0.3,
    "mid": 0.6,
    "mid_high": 0.75,
    "high": 0.9,
    "extreme": 1.2
}

CHAOS_PERIOD_MAPPING_MA: Dict[str, str] = {
    "low": "2.0",
    "mid": "1.0",
    "mid_high": "0.7",
    "high": "0.4",
    "extreme": "0.2"
}

CHAOS_PERIOD_MAPPING_SA: Dict[str, str] = {
    "low": "10.0",
    "mid": "5.0",
    "mid_high": "3.5",
    "high": "2.0",
    "extreme": "1.0"
}

# ─── Utilidades Estadísticas ────────────────────────────────────────────────

def gini_coefficient(values: np.ndarray) -> float:
    """Calcula el Coeficiente de Gini de injusticia distributiva sobre demoras.

    Args:
        values: Arreglo numpy de valores.

    Returns:
        float: Coeficiente de Gini calculado.
    """
    if len(values) == 0 or values.sum() == 0:
        return 0.0
    v = np.sort(np.abs(values))
    n = len(v)
    idx = np.arange(1, n + 1)
    return float((2 * np.sum(idx * v)) / (n * np.sum(v)) - (n + 1) / n)


def cvar_90(losses: List[float]) -> float:
    """Calcula el CVaR al 90% de la distribucion de demoras.

    Args:
        losses: Lista de demoras.

    Returns:
        float: Valor del CVaR al 90%.
    """
    if not losses:
        return 0.0
    arr = np.array(losses)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return 0.0
    q = np.quantile(arr, 0.90)
    tail = arr[arr >= q]
    return float(tail.mean()) if len(tail) > 0 else float(q)


def compute_median_ci95(data: List[float], n_bootstrap: int = 1000, alpha: float = 0.05) -> Tuple[float, float]:
    """Calcula el intervalo de confianza del 95% de la mediana usando bootstrap percentil.

    Args:
        data: Datos observados.
        n_bootstrap: Numero de replicas bootstrap.
        alpha: Nivel de significancia.

    Returns:
        Tuple[float, float]: Intervalo de confianza (limite inferior, limite superior).
    """
    if not data:
        return 0.0, 0.0
    if len(data) < 2:
        return float(data[0]), float(data[0])
    
    rng = np.random.default_rng(42)
    boot_medians = []
    arr = np.array(data)
    for _ in range(n_bootstrap):
        sample = rng.choice(arr, size=len(arr), replace=True)
        boot_medians.append(np.median(sample))
    
    lower = float(np.percentile(boot_medians, alpha / 2 * 100))
    upper = float(np.percentile(boot_medians, (1 - alpha / 2) * 100))
    return lower, upper


def mann_whitney_u(a: List[float], b: List[float]) -> Tuple[Optional[float], Optional[float], Optional[float], str, str]:
    """Realiza la prueba bilateral de Mann-Whitney U y calcula el efecto r.

    Args:
        a: Datos del primer grupo.
        b: Datos del segundo grupo.

    Returns:
        Tuple: (Estadistico U, p-valor, efecto r, etiqueta significancia, magnitud).
    """
    if not a or not b:
        return None, None, None, "ns", "negligible"
    try:
        from scipy.stats import mannwhitneyu
        stat, p = mannwhitneyu(a, b, alternative="two-sided")
        n1, n2 = len(a), len(b)
        r = 1.0 - (2.0 * stat) / (n1 * n2)
        
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        abs_r = abs(r)
        
        if abs_r < 0.1:
            mag = "negligible"
        elif abs_r < 0.3:
            mag = "small"
        elif abs_r < 0.5:
            mag = "medium"
        else:
            mag = "large"
            
        return float(stat), float(p), float(r), sig, mag
    except Exception as e:
        logging.warning(f"Error al calcular Mann-Whitney U: {e}")
        return None, None, None, "ns", "negligible"


def kruskal_wallis(groups: Dict[str, List[float]]) -> Tuple[Optional[float], Optional[float]]:
    """Prueba global de Kruskal-Wallis para multiples grupos.

    Args:
        groups: Diccionario de grupo a datos.

    Returns:
        Tuple[Optional[float], Optional[float]]: (Estadistico H, p-valor).
    """
    valid_groups = [np.array(v) for v in groups.values() if len(v) > 0]
    if len(valid_groups) < 2:
        return None, None
    try:
        from scipy.stats import kruskal
        stat, p = kruskal(*valid_groups)
        return float(stat), float(p)
    except Exception as e:
        logging.warning(f"Error en Kruskal-Wallis: {e}")
        return None, None


def compute_post_hoc_bonferroni(groups: Dict[str, List[float]]) -> List[Tuple[str, str, float, float]]:
    """Calcula comparaciones post-hoc por pares con correccion de Bonferroni.

    Args:
        groups: Diccionario de grupo a datos.

    Returns:
        List[Tuple[str, str, float, float]]: Lista de (grupo_a, grupo_b, p_raw, p_adj).
    """
    keys = list(groups.keys())
    n_groups = len(keys)
    if n_groups < 2:
        return []
    
    comparisons = []
    for i in range(n_groups):
        for j in range(i + 1, n_groups):
            comparisons.append((keys[i], keys[j]))
            
    n_comparisons = len(comparisons)
    results = []
    
    from scipy.stats import mannwhitneyu
    for ga, gb in comparisons:
        a = groups[ga]
        b = groups[gb]
        if len(a) == 0 or len(b) == 0:
            results.append((ga, gb, 1.0, 1.0))
            continue
        try:
            _, p_raw = mannwhitneyu(a, b, alternative="two-sided")
            p_adj = min(1.0, p_raw * n_comparisons)
            results.append((ga, gb, float(p_raw), float(p_adj)))
        except Exception as e:
            logging.warning(f"Error en post-hoc {ga} vs {gb}: {e}")
            results.append((ga, gb, 1.0, 1.0))
            
    return results


def spearman_corr(x: List[float], y: List[float]) -> Tuple[Optional[float], Optional[float]]:
    """Calcula el coeficiente de correlacion de Spearman y su p-valor.

    Args:
        x: Lista de variable ordinal.
        y: Lista de variable continua.

    Returns:
        Tuple[Optional[float], Optional[float]]: (Coeficiente rho, p-valor).
    """
    if len(x) < 2 or len(y) < 2:
        return None, None
    try:
        from scipy.stats import spearmanr
        rho, p = spearmanr(x, y)
        return float(rho), float(p)
    except Exception as e:
        logging.warning(f"Error en Spearman: {e}")
        return None, None

# ─── Descubrimiento de Infraestructura SUMO ─────────────────────────────────

def get_allowed_passenger_edges(net_xml_path: Path) -> Set[str]:
    """Extrae las aristas que permiten transito de vehiculos de pasajeros.

    Args:
        net_xml_path: Ruta del archivo .net.xml.

    Returns:
        Set[str]: Conjunto de IDs de aristas permitidas.
    """
    allowed_edges = set()
    try:
        tree = ET.parse(str(net_xml_path))
        root = tree.getroot()
        for edge in root.findall("edge"):
            edge_id = edge.get("id")
            if not edge_id or edge.get("function") == "internal":
                continue
            for lane in edge.findall("lane"):
                allow = lane.get("allow", "")
                disallow = lane.get("disallow", "")
                lane_allows = True
                if allow:
                    lane_allows = "passenger" in allow or "all" in allow
                if disallow:
                    if "passenger" in disallow or "all" in disallow:
                        lane_allows = False
                if lane_allows:
                    allowed_edges.add(edge_id)
                    break
    except Exception as e:
        logging.warning(f"Error parseando aristas de red: {e}")
    return allowed_edges


def discover_vehicular_tls_id(net_xml_path: Path, allowed_edges: Set[str]) -> str:
    """Descubre el semaforo principal basado en la centralidad de grado.

    Args:
        net_xml_path: Ruta del archivo .net.xml.
        allowed_edges: Conjunto de aristas de pasajeros permitidas.

    Returns:
        str: ID del semaforo vehicular principal.
    """
    try:
        tree = ET.parse(str(net_xml_path))
        root = tree.getroot()
        tls_counts = {}
        for connection in root.findall("connection"):
            tl = connection.get("tl")
            from_edge = connection.get("from")
            if tl and from_edge in allowed_edges:
                tls_counts[tl] = tls_counts.get(tl, 0) + 1
        if tls_counts:
            return max(tls_counts, key=tls_counts.get)
    except Exception as e:
        logging.warning(f"Error descubriendo semaforo principal: {e}")
    
    try:
        tree = ET.parse(str(net_xml_path))
        root = tree.getroot()
        for tl in root.findall("tlLogic"):
            tls_id = tl.get("id")
            if tls_id:
                return tls_id
    except Exception:
        pass
    return "J0"

# ─── Generación de Rutas ────────────────────────────────────────────────────

def generate_stress_traffic(net_path: Path, steps_limit: int, stress_level: str = "high") -> Path:
    """Genera rutas de estres con flujos de interseccion directa (JFI).

    Args:
        net_path: Ruta de la red.
        steps_limit: Limite de pasos del episodio.
        stress_level: Nivel de caos operacional.

    Returns:
        Path: Ruta al archivo de rutas generado.
    """
    routes_dir = net_path.parent.parent / "routes"
    routes_dir.mkdir(parents=True, exist_ok=True)
    route_path = routes_dir / f"{net_path.stem}_stress_{stress_level}.rou.xml"

    allowed_edges = get_allowed_passenger_edges(net_path)
    tls_id = discover_vehicular_tls_id(net_path, allowed_edges)

    connections = []
    incoming_lanes = set()
    try:
        tree = ET.parse(str(net_path))
        root = tree.getroot()
        for connection in root.findall("connection"):
            if connection.get("tl") == tls_id:
                from_edge = connection.get("from")
                from_lane_idx = connection.get("lane")
                to_edge = connection.get("to")
                if from_edge and to_edge and from_edge in allowed_edges and to_edge in allowed_edges:
                    pair = (from_edge, to_edge)
                    if pair not in connections:
                        connections.append(pair)
                    if from_lane_idx is not None:
                        incoming_lanes.add(f"{from_edge}_{from_lane_idx}")
    except Exception as e:
        logging.warning(f"Error parseando conexiones viales: {e}")

    if not connections:
        return generate_random_traffic(net_path, steps_limit, stress_level, is_multi_agent=False)

    num_connections = len(connections)
    num_lanes = len(incoming_lanes) if incoming_lanes else len(set(c[0] for c in connections))
    if num_lanes == 0:
        num_lanes = 4

    v_c_ratio = CHAOS_VC_MAPPING.get(stress_level, 0.9)
    capacity = num_lanes * 1800.0
    target_flow = capacity * v_c_ratio
    period = (3600.0 * num_connections) / target_flow
    period = round(period, 2)

    try:
        xml_lines = ['<routes>']
        xml_lines.append('    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" minGap="2.0" maxSpeed="16.67"/>')
        flow_idx = 0
        sim_end = steps_limit * 5
        for inc, out in connections:
            xml_lines.append(f'    <flow id="f_{flow_idx}" type="car" begin="0" end="{sim_end}" period="{period}" from="{inc}" to="{out}"/>')
            flow_idx += 1
        xml_lines.append('</routes>')

        with open(str(route_path), 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml_lines))
    except Exception as e:
        logging.error(f"Error escribiendo XML de flujos JFI: {e}")
        return generate_random_traffic(net_path, steps_limit, stress_level, is_multi_agent=False)

    return route_path


def generate_random_traffic(net_path: Path, steps_limit: int, stress_level: str = "high", is_multi_agent: bool = False) -> Path:
    """Genera rutas de trafico aleatorio usando randomTrips.py.

    Args:
        net_path: Ruta de la red.
        steps_limit: Limite de pasos.
        stress_level: Nivel de caos.
        is_multi_agent: Flag indicando modo de ejecucion.

    Returns:
        Path: Ruta al archivo de rutas generado.
    """
    routes_dir = net_path.parent.parent / "routes"
    routes_dir.mkdir(parents=True, exist_ok=True)
    suffix = "multi_agent" if is_multi_agent else "random"
    route_path = routes_dir / f"{net_path.stem}_{suffix}_{stress_level}.rou.xml"

    if is_multi_agent:
        p_val = CHAOS_PERIOD_MAPPING_MA.get(stress_level, "0.4")
    else:
        p_val = CHAOS_PERIOD_MAPPING_SA.get(stress_level, "2.0")

    if route_path.exists():
        return route_path

    sumo_home = os.environ.get("SUMO_HOME", r"C:\Program Files (x86)\Eclipse\Sumo")
    random_trips_path = os.path.join(sumo_home, "tools", "randomTrips.py")

    try:
        subprocess.run([
            sys.executable, random_trips_path,
            "-n", str(net_path.resolve()),
            "-o", str(route_path.resolve()),
            "-e", str(steps_limit * 5),
            "-p", p_val,
            "--validate"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        logging.error(f"Fallo al ejecutar randomTrips.py: {e}")
        raise RuntimeError(f"Error critico en randomTrips para la red {net_path.name}")
    return route_path


def generate_eval_sumocfg(net_path: Path, route_path: Path, rank: int, steps_sec: int, lateral_res: Optional[float] = None) -> str:
    """Genera un sumocfg temporal para el episodio.

    Args:
        net_path: Ruta del net.xml.
        route_path: Ruta del rou.xml.
        rank: Rango identificador.
        steps_sec: Segundos totales de simulacion.
        lateral_res: Resolucion lateral opcional.

    Returns:
        str: Ruta al sumocfg generado.
    """
    tmp_dir = tempfile.gettempdir()
    lateral_tag = f'<lateral-resolution value="{lateral_res}"/>' if lateral_res else ""
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="{net_path.resolve()}"/>
        <route-files value="{route_path.resolve()}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="{steps_sec}"/>
    </time>
    <processing>
        <time-to-teleport value="300"/>
        <waiting-time-memory value="1000"/>
        {lateral_tag}
    </processing>
    <report>
        <no-warnings value="true"/>
    </report>
</configuration>"""
    path = os.path.join(tmp_dir, f"transfer_robust_rank{rank}.sumocfg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# ─── Baselines ──────────────────────────────────────────────────────────────

class FixedTimeOptAgent:
    """Baseline de tiempo fijo optimizado por ciudad con duraciones variables."""
    
    def __init__(self, num_phases: int = 4):
        """Inicializa el agente FixedTimeOpt.

        Args:
            num_phases: Numero de fases.
        """
        self.num_phases = num_phases
        self.steps_per_phase = 4
        self.current_step = 0
        self.steps_mapping = {
            "Barcelona": 2,
            "Madrid": 2,
            "Quito": 4,
            "Bogota": 4,
            "Berlin": 4,
            "CDMX": 4
        }
        
    def set_city(self, city_name: str) -> None:
        """Establece la duracion de fase de acuerdo a la ciudad.

        Args:
            city_name: Nombre de la ciudad.
        """
        self.steps_per_phase = self.steps_mapping.get(city_name, 4)
        
    def reset(self) -> None:
        """Reinicia el contador interno de pasos."""
        self.current_step = 0
        
    def predict(self, obs: np.ndarray, deterministic: bool = True) -> Tuple[int, None]:
        """Selecciona la fase correspondiente basandose en el contador de pasos.

        Args:
            obs: Vector de observacion.
            deterministic: Parametro SB3.

        Returns:
            Tuple[int, None]: (Fase elegida, None).
        """
        phase = (self.current_step // self.steps_per_phase) % self.num_phases
        self.current_step += 1
        return phase, None


class RandomAgent:
    """Baseline que selecciona acciones uniformemente al azar."""
    
    def __init__(self, num_phases: int = 4):
        """Inicializa el agente Random.

        Args:
            num_phases: Numero de fases.
        """
        self.num_phases = num_phases
        
    def reset(self) -> None:
        """Metodo vacio para compatibilidad."""
        pass
        
    def predict(self, obs: np.ndarray, deterministic: bool = True) -> Tuple[int, None]:
        """Selecciona una fase aleatoria.

        Args:
            obs: Vector de observacion.
            deterministic: Parametro SB3.

        Returns:
            Tuple[int, None]: (Fase elegida, None).
        """
        return int(np.random.randint(self.num_phases)), None

# ─── Multi-Agent Control Managers ───────────────────────────────────────────

class LocalTLSManager:
    """Administrador local de un semaforo individual dentro de la red completa."""
    
    def __init__(self, tls_id: str):
        """Inicializa el manager del semaforo.

        Args:
            tls_id: ID del semaforo.
        """
        self.tls_id = tls_id
        import traci
        
        raw_lanes = list(traci.trafficlight.getControlledLanes(tls_id))
        seen = set()
        unique_lanes = [l for l in raw_lanes if not (l in seen or seen.add(l))]
        
        n_target = 12
        if len(unique_lanes) >= n_target:
            self.controlled_lanes = unique_lanes[:n_target]
        elif len(unique_lanes) > 0:
            self.controlled_lanes = unique_lanes + [unique_lanes[-1]] * (n_target - len(unique_lanes))
        else:
            self.controlled_lanes = []
            
        try:
            logic_list = traci.trafficlight.getAllProgramLogics(tls_id)
            logic = logic_list[0] if logic_list else None
            self.green_phases = [
                i for i, phase in enumerate(logic.phases)
                if any(c in ("G", "g") for c in phase.state)
            ] if logic else [0, 1, 2, 3]
        except Exception:
            self.green_phases = [0, 1, 2, 3]
            
        self.current_phase = traci.trafficlight.getPhase(tls_id)
        self.phase_start_step = 0
        self.step_count = 0
        
    def get_state(self) -> np.ndarray:
        """Genera la observacion normalizada de 34 dimensiones del semaforo.

        Returns:
            np.ndarray: Vector de observacion.
        """
        if not self.controlled_lanes:
            return np.zeros(34, dtype=np.float32)
        import traci
            
        queues = np.array(
            [traci.lane.getLastStepHaltingNumber(lane) for lane in self.controlled_lanes],
            dtype=np.float32
        )
        waits = np.array(
            [traci.lane.getWaitingTime(lane) for lane in self.controlled_lanes],
            dtype=np.float32
        )
        pressure = np.array(
            [traci.lane.getLastStepVehicleNumber(lane) for lane in self.controlled_lanes],
            dtype=np.float32
        )
        
        q_norm = np.clip(queues / 50.0, 0.0, 1.0)
        w_norm = np.clip(waits / 300.0, 0.0, 1.0)
        p_norm = np.clip(pressure / 50.0, 0.0, 1.0)
        
        if len(p_norm) > 4:
            p_agg = np.array([
                np.mean(p_norm[0:2]) if len(p_norm) >= 2 else p_norm[0] if len(p_norm) >= 1 else 0.0,
                np.mean(p_norm[2:4]) if len(p_norm) >= 4 else 0.0,
                np.mean(p_norm[4:6]) if len(p_norm) >= 6 else 0.0,
                np.mean(p_norm[6:8]) if len(p_norm) >= 8 else 0.0,
            ], dtype=np.float32)
        else:
            p_agg = np.pad(p_norm, (0, 4 - len(p_norm)), mode='constant')[:4]
            
        phi_onehot = np.zeros(4, dtype=np.float32)
        phase_idx = self.current_phase % 4
        phi_onehot[phase_idx] = 1.0
        
        phase_age_s = (self.step_count - self.phase_start_step) * 5
        tau_norm = np.clip(phase_age_s / 120.0, 0.0, 1.0)
        tau_features = np.array([phase_age_s / 120.0, tau_norm], dtype=np.float32)
        
        obs = np.concatenate([
            q_norm.astype(np.float32),
            w_norm.astype(np.float32),
            p_agg,
            phi_onehot,
            tau_features,
        ])
        return obs
        
    def apply_action(self, action: int) -> None:
        """Aplica la accion del semaforo en SUMO.

        Args:
            action: Indice de la fase.
        """
        if not self.green_phases:
            return
        import traci
            
        phase_idx = action % len(self.green_phases)
        target_phase = self.green_phases[phase_idx]
        
        if target_phase != self.current_phase:
            traci.trafficlight.setPhase(self.tls_id, target_phase)
            self.phase_start_step = self.step_count
            self.current_phase = target_phase
            
        self.step_count += 1

# ─── Network-Wide Chaos Manager (multi-TLS) ───────────────────────────────

class NetworkWideChaosManager:
    """
    Version multi-TLS del LatamChaosManager.
    Opera sobre la red completa en lugar de un unico semaforo.
    Diseñado para la evaluacion de transferencia zero-shot con caos conductual real.
    """
    def __init__(self, probabilidad_caos: float = 0.30, ablation_mode: str = "combined"):
        self.probabilidad_caos = probabilidad_caos
        self.ablation_mode = ablation_mode
        self.assigned_vehicles: set = set()
        self.latam_types: dict = {}
        self.police_affected_vehicles: dict = {}
        self.tick_counter: int = 0
        self._all_controlled_lanes: set = set()
        self._lanes_loaded: bool = False

    def _ensure_lanes(self, all_tls_ids: list) -> None:
        """Carga las calles controladas de todos los semaforos de la red."""
        if self._lanes_loaded:
            return
        import traci
        for tls_id in all_tls_ids:
            try:
                links = traci.trafficlight.getControlledLinks(tls_id)
                for link in links:
                    for connection in link:
                        self._all_controlled_lanes.add(connection[0])
                        self._all_controlled_lanes.add(connection[1])
            except Exception:
                try:
                    raw = traci.trafficlight.getControlledLanes(tls_id)
                    self._all_controlled_lanes.update(raw)
                except Exception:
                    pass
        self._lanes_loaded = True

    def step(self, all_tls_ids: list) -> None:
        """Aplica perturbaciones conductales sobre toda la red en cada RL step."""
        import traci
        import math as _math

        self.tick_counter += 1
        if self.tick_counter % 5 != 0:
            return

        self._ensure_lanes(all_tls_ids)

        # Obtener vehiculos en las calles controladas de la red
        veh_ids: list = []
        for lane in self._all_controlled_lanes:
            try:
                veh_ids.extend(traci.lane.getLastStepVehicleIDs(lane))
            except Exception:
                pass
        veh_ids = list(set(veh_ids))

        for v_id in veh_ids:
            # Asignacion dinamica de comportamiento al aparecer en la red
            if v_id not in self.assigned_vehicles:
                self.assigned_vehicles.add(v_id)
                if random.random() < self.probabilidad_caos:
                    new_type = "micro_imprudent" if random.random() < 0.5 else "imprudent"
                    self.latam_types[v_id] = new_type
                    try:
                        if self.ablation_mode in ["combined", "tailgating_only"]:
                            traci.vehicle.setTau(v_id, 0.5)
                        if self.ablation_mode in ["combined", "speeding_only"]:
                            traci.vehicle.setSpeedFactor(v_id, random.uniform(1.2, 1.8))
                            traci.vehicle.setImperfection(v_id, 0.9)
                    except Exception:
                        pass

            v_type = self.latam_types.get(v_id, "")

            if "imprudent" in v_type:
                try:
                    edge = traci.vehicle.getRoadID(v_id)
                    # Bloqueo de cruce (5% de prob cuando el vehículo está dentro del cruce)
                    if edge.startswith(":") and random.random() < 0.05 and self.ablation_mode in ["combined", "blocking_only"]:
                        traci.vehicle.setSpeed(v_id, 0.0)
                    # Aceleracion en amarillo/rojo
                    tls_links = traci.vehicle.getNextTLS(v_id)
                    if tls_links and self.ablation_mode in ["combined", "speeding_only"]:
                        _, _, dist, state = tls_links[0]
                        if state.lower() in ['y', 'r'] and dist < 20.0:
                            traci.vehicle.setSpeedFactor(v_id, 2.0)
                except Exception:
                    pass

            elif "micro_imprudent" in v_type and self.ablation_mode in ["combined", "blocking_only"]:
                # Frenado espontaneo (microbuses recogiendo pasajeros)
                try:
                    speed = traci.vehicle.getSpeed(v_id)
                    if speed < 2.0 and random.random() < 0.02:
                        traci.vehicle.setSpeed(v_id, 0.0)
                except Exception:
                    pass


# ─── Ejecución de Episodios ─────────────────────────────────────────────────

def run_single_episode(model: Any, sumocfg: str, tls_id: str,
                       steps_limit: int, seed: int,
                       lateral_res: Optional[float] = None,
                       use_gui: bool = False,
                       enable_traci_chaos: bool = False,
                       chaos_prob: float = 0.3) -> Dict[str, Any]:
    """Ejecuta un episodio de control en nodo aislado.

    Args:
        model: Agente o baseline a evaluar.
        sumocfg: Ruta al archivo sumocfg.
        tls_id: ID del semaforo a controlar.
        steps_limit: Limite de pasos.
        seed: Semilla para el episodio.
        lateral_res: Resolucion lateral de carriles.
        use_gui: Si arranca la GUI de SUMO.
        enable_traci_chaos: Si inyecta LatamChaosManager.
        chaos_prob: Probabilidad de conductores imprudentes.

    Returns:
        Dict[str, Any]: Metricas agregadas.
    """
    env = TSCEnv(
        sumocfg_path=sumocfg,
        tls_id=tls_id,
        delta_t=5,
        max_steps=steps_limit,
        use_gui=use_gui,
        seed=seed,
        enable_traci_chaos=enable_traci_chaos,
        probabilidad_caos=chaos_prob
    )
    obs, info = env.reset()
    done = False
    step_count = 0
    rewards, delays, queues, ginis = [], [], [], []
    co2_emissions, fuel_consumptions = [], []

    while not done and step_count < steps_limit:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        rewards.append(reward)
        delays.append(info.get("delay", 0.0))
        queues.append(info.get("total_queue", 0.0))
        ginis.append(info.get("gini", 0.0))
        co2_emissions.append(info.get("co2", 0.0))
        fuel_consumptions.append(info.get("fuel", 0.0))
        
        done = terminated or truncated
        step_count += 1

    env.close()

    mean_delay = float(np.mean(delays)) if delays else 0.0
    mean_queue = float(np.mean(queues)) if queues else 0.0
    mean_gini = float(np.mean(ginis)) if ginis else 0.0
    cvar_val = cvar_90(delays)

    return {
        "reward_total": float(np.sum(rewards)),
        "delay_mean": mean_delay,
        "queue_mean": mean_queue,
        "gini_mean": mean_gini,
        "cvar_90": cvar_val,
        "steps": step_count,
        "collapsed": 1 if mean_delay > 2000.0 else 0,
        "co2_total": float(np.sum(co2_emissions)) if co2_emissions else 0.0,
        "fuel_total": float(np.sum(fuel_consumptions)) if fuel_consumptions else 0.0,
    }


def run_multi_agent_episode(model: Any, sumocfg: str,
                             steps_limit: int, seed: int,
                             lateral_res: Optional[float] = None,
                             use_gui: bool = False,
                             port_offset: int = 0,
                             with_behavioral_chaos: bool = False,
                             chaos_prob: float = 0.30) -> Dict[str, Any]:
    """Ejecuta un episodio de control multi-agente en red completa.

    Args:
        model: Agente o baseline a evaluar.
        sumocfg: Ruta al sumocfg.
        steps_limit: Limite de pasos.
        seed: Semilla para el episodio.
        lateral_res: Resolucion lateral.
        use_gui: Si arranca con GUI.

    Returns:
        Dict[str, Any]: Metricas agregadas de red.
    """
    import copy
    import traci
    
    traci_port = 8813 + port_offset + (seed % 500)
    sumo_binary = "sumo-gui" if use_gui else "sumo"
    sumo_bin = shutil.which(sumo_binary) or sumo_binary
    
    cmd = [
        sumo_bin,
        "-c", sumocfg,
        "--remote-port", str(traci_port),
        "--step-length", "1.0",
        "--no-step-log",
        "--seed", str(seed),
    ]
    
    creation_flags = 0
    if os.name == 'nt':
        creation_flags = 0x08000000
        
    sumo_log_path = Path(sumocfg).with_suffix('.sumo_multi.log')
    sumo_log_file = open(sumo_log_path, "w")
    
    sumo_process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=sumo_log_file,
        creationflags=creation_flags
    )
    
    time.sleep(2.0)
    
    try:
        traci.init(port=traci_port, numRetries=10)
    except Exception as e:
        sumo_log_file.close()
        try:
            sumo_process.terminate()
        except Exception:
            pass
        raise RuntimeError(f"Error al conectar TraCI en modo multi-agente en puerto {traci_port}: {e}")
        
    all_tls_ids = traci.trafficlight.getIDList()

    # Instanciar el Network-Wide Chaos Manager si se solicito caos conductual
    nw_chaos: Optional[NetworkWideChaosManager] = None
    if with_behavioral_chaos:
        nw_chaos = NetworkWideChaosManager(probabilidad_caos=chaos_prob)
        logging.debug(f"[CHAOS] NetworkWideChaosManager activo (prob={chaos_prob:.2f})")

    tls_counts = {}
    for tid in all_tls_ids:
        raw_lanes = traci.trafficlight.getControlledLanes(tid)
        if raw_lanes:
            seen_lanes = set(raw_lanes)
            tls_counts[tid] = len(seen_lanes)
            
    K = 10
    sorted_tls = sorted(tls_counts.items(), key=lambda x: x[1], reverse=True)
    top_tls = [tid for tid, count in sorted_tls[:K]]
    
    tls_managers = {}
    for tid in top_tls:
        tls_managers[tid] = LocalTLSManager(tid)
        
    is_baseline = isinstance(model, (FixedTimeOptAgent, RandomAgent))
    if is_baseline:
        agents = {tid: copy.deepcopy(model) for tid in tls_managers}
        if isinstance(model, FixedTimeOptAgent):
            city_name = "Quito"
            for c in ["Barcelona", "Quito", "Bogota", "Berlin", "Madrid", "CDMX"]:
                if c.lower() in sumocfg.lower():
                    city_name = c
                    break
            for ag in agents.values():
                ag.set_city(city_name)
    else:
        agents = {}
        
    for manager in tls_managers.values():
        manager.step_count = 0
        manager.phase_start_step = 0
        manager.current_phase = traci.trafficlight.getPhase(manager.tls_id)
        
    delays, queues, ginis, co2_emissions, fuel_consumptions = [], [], [], [], []
    step_count = 0
    done = False
    
    all_controlled_lanes = set()
    for manager in tls_managers.values():
        all_controlled_lanes.update(manager.controlled_lanes)
        
    while not done and step_count < steps_limit:
        for tid, manager in tls_managers.items():
            obs = manager.get_state()
            if is_baseline:
                action, _ = agents[tid].predict(obs, deterministic=True)
            else:
                action, _ = model.predict(obs, deterministic=True)
            manager.apply_action(action)
            
        step_co2 = 0.0
        step_fuel = 0.0
        step_halting = 0.0
        step_waiting = 0.0
        
        try:
            for _ in range(5):
                traci.simulationStep()

            # Inyectar perturbaciones conductales si el chaos manager esta activo
            if nw_chaos is not None:
                nw_chaos.step(list(all_tls_ids))

            if all_controlled_lanes:
                step_co2 = sum(traci.lane.getCO2Emission(lane) for lane in all_controlled_lanes)
                step_fuel = sum(traci.lane.getFuelConsumption(lane) for lane in all_controlled_lanes)
                step_halting = sum(traci.lane.getLastStepHaltingNumber(lane) for lane in all_controlled_lanes)
                step_waiting = sum(traci.lane.getWaitingTime(lane) for lane in all_controlled_lanes)
        except Exception as e:
            logging.warning(f"Simulacion interrumpida por TraCI en paso {step_count}: {e}")
            break
            
        step_ginis = []
        for manager in tls_managers.values():
            if manager.controlled_lanes:
                waits = np.array([traci.lane.getWaitingTime(lane) for lane in manager.controlled_lanes], dtype=np.float32)
                n = len(waits)
                mean_wait = np.mean(waits)
                if mean_wait > 1e-8 and n > 0:
                    diff_matrix = np.abs(waits[:, np.newaxis] - waits[np.newaxis, :])
                    gini = float(np.sum(diff_matrix) / (2 * n * n * mean_wait))
                    step_ginis.append(np.clip(gini, 0.0, 1.0))
                else:
                    step_ginis.append(0.0)
        gini_val = np.mean(step_ginis) if step_ginis else 0.0
        
        delays.append(step_waiting)
        queues.append(step_halting)
        ginis.append(gini_val)
        co2_emissions.append(step_co2)
        fuel_consumptions.append(step_fuel)
        
        sim_time = traci.simulation.getTime()
        sim_end = traci.simulation.getEndTime()
        done = sim_time >= sim_end
        step_count += 1
        
    try:
        traci.close()
    except Exception:
        pass
        
    try:
        sumo_process.terminate()
        sumo_process.wait(timeout=2)
    except Exception:
        try:
            sumo_process.kill()
        except Exception:
            pass
    finally:
        sumo_log_file.close()
        try:
            if sumo_log_path.exists():
                sumo_log_path.unlink()
        except Exception:
            pass
        time.sleep(0.5)
        
    mean_delay = float(np.mean(delays)) if delays else 0.0
    mean_queue = float(np.mean(queues)) if queues else 0.0
    cvar_val = cvar_90(delays)
    
    return {
        "reward_total": 0.0,
        "delay_mean": mean_delay,
        "queue_mean": mean_queue,
        "gini_mean": float(np.mean(ginis)) if ginis else 0.0,
        "cvar_90": cvar_val,
        "steps": step_count,
        "collapsed": 1 if mean_delay > 5000.0 else 0,
        "co2_total": float(np.sum(co2_emissions)) if co2_emissions else 0.0,
        "fuel_total": float(np.sum(fuel_consumptions)) if fuel_consumptions else 0.0,
    }

# ─── Evaluación Multi-Episodio ──────────────────────────────────────────────

def _run_single_episode_worker(ep: int, model: Any, model_name: str, city: str,
                               net_path: Path, route_path: Path, steps_limit: int,
                               lateral_res: float, use_gui: bool, mode: str,
                               with_behavioral_chaos: bool, chaos_prob: float) -> Dict[str, Any]:
    seed = 1000 + ep
    sumocfg = generate_eval_sumocfg(
        net_path, route_path, rank=ep,
        steps_sec=steps_limit * 5,
        lateral_res=lateral_res
    )
    
    if hasattr(model, "set_city"):
        model.set_city(city)
        
    if hasattr(model, "reset"):
        model.reset()
        
    allowed = get_allowed_passenger_edges(net_path)
    tls_id = discover_vehicular_tls_id(net_path, allowed)
        
    success = False
    retry_count = 0
    res = {}
    
    while not success and retry_count < 3:
        try:
            # En multi_agent, usamos port_offset para aislar los workers de cada semilla
            port_offset = (seed % 500)
            if mode == "multi_agent":
                res = run_multi_agent_episode(
                    model, sumocfg, steps_limit, seed, lateral_res, use_gui,
                    port_offset=port_offset,
                    with_behavioral_chaos=with_behavioral_chaos,
                    chaos_prob=chaos_prob
                )
            else:
                res = run_single_episode(
                    model, sumocfg, tls_id, steps_limit, seed, lateral_res, use_gui,
                    enable_traci_chaos=with_behavioral_chaos,
                    chaos_prob=chaos_prob
                )
            success = True
        except Exception as e:
            retry_count += 1
            print(f"  [WARN] Fallo ep {ep+1} ({e}), reintento {retry_count}/3...")
            time.sleep(2)
            
    if not success:
        print(f"  [ERROR] Fallo critico en ep {ep+1}, devolviendo fallback gridlock")
        res = {
            "delay_mean": steps_limit * 5 * 0.5,
            "gini_mean": 1.0,
            "cvar_90": steps_limit * 5 * 0.5,
            "collapsed": True,
            "co2_total": 0.0,
            "fuel_total": 0.0
        }
        
    res["model"] = model_name
    res["city"] = city
    res["episode"] = ep + 1
    res["seed"] = seed
    
    print(f"  Ep {ep+1:2d} | Delay={res['delay_mean']:.1f}s | "
          f"Gini={res['gini_mean']:.3f} | CVaR90={res['cvar_90']:.1f}s | "
          f"{'[GRIDLOCK]' if res['collapsed'] else 'OK'}")
          
    return res


def evaluate_transfer_n_episodes(
    model: Any,
    model_name: str,
    city: str,
    chaos_level: str,
    net_path: Path,
    route_path: Path,
    n_episodes: int,
    steps_limit: int,
    lateral_res: Optional[float] = None,
    use_gui: bool = False,
    mode: str = "stress",
    with_behavioral_chaos: bool = False,
    chaos_prob: float = 0.3,
    workers: int = 7
) -> List[Dict[str, Any]]:
    """Ejecuta n_episodes episodios con semillas distintas (1000+ep) en paralelo."""
    from joblib import Parallel, delayed

    print(f"\n{'='*60}")
    print(f"  {model_name} | {city} | {chaos_level} | {n_episodes} eps | Workers: {workers}")
    print(f"{'='*60}")

    if hasattr(model, "set_city"):
        model.set_city(city)

    if workers > 1:
        results = Parallel(n_jobs=workers)(
            delayed(_run_single_episode_worker)(
                ep, model, model_name, city, net_path, route_path, steps_limit,
                lateral_res, use_gui, mode, with_behavioral_chaos, chaos_prob
            )
            for ep in range(n_episodes)
        )
    else:
        results = []
        for ep in range(n_episodes):
            res = _run_single_episode_worker(
                ep, model, model_name, city, net_path, route_path, steps_limit,
                lateral_res, use_gui, mode, with_behavioral_chaos, chaos_prob
            )
            results.append(res)
            
    # Asignar chaos_level a los resultados (robust lo necesita para stats)
    for res in results:
        res["chaos_level"] = chaos_level

    return results

# ─── Cálculo de Estadísticos ────────────────────────────────────────────────

def compute_summary(results: List[Dict[str, Any]], city: str, model_name: str, chaos_level: str) -> Optional[Dict[str, Any]]:
    """Calcula los estadisticos de resumen para una combinacion especifica.

    Args:
        results: Lista de todos los resultados.
        city: Ciudad.
        model_name: Nombre del modelo.
        chaos_level: Nivel de caos.

    Returns:
        Optional[Dict[str, Any]]: Resumen descriptivo de la combinacion.
    """
    subset = [r for r in results if r["city"] == city and r["model"] == model_name and r["chaos_level"] == chaos_level]
    if not subset:
        return None
        
    delays = [r["delay_mean"] for r in subset]
    ginis = [r["gini_mean"] for r in subset]
    cvars = [r["cvar_90"] for r in subset]
    collapsed = [r["collapsed"] for r in subset]
    co2s = [r["co2_total"] for r in subset]
    fuels = [r["fuel_total"] for r in subset]

    def get_iqr(v):
        return float(np.percentile(v, 75) - np.percentile(v, 25)) if v else 0.0

    lower_ci, upper_ci = compute_median_ci95(delays)

    return {
        "model": model_name,
        "city": city,
        "chaos_level": chaos_level,
        "n": len(subset),
        "delay_median": float(np.median(delays)) if delays else 0.0,
        "delay_iqr": get_iqr(delays),
        "delay_ci95_lower": lower_ci,
        "delay_ci95_upper": upper_ci,
        "gini_median": float(np.median(ginis)) if ginis else 0.0,
        "gini_iqr": get_iqr(ginis),
        "cvar90_median": float(np.median(cvars)) if cvars else 0.0,
        "cvar90_iqr": get_iqr(cvars),
        "collapse_rate_pct": float(np.mean(collapsed) * 100.0) if collapsed else 0.0,
        "co2_median": float(np.median(co2s)) if co2s else 0.0,
        "fuel_median": float(np.median(fuels)) if fuels else 0.0,
    }

# ─── Generación de Reporte ──────────────────────────────────────────────────

def write_markdown_report(all_results: List[Dict[str, Any]], summaries: List[Dict[str, Any]],
                           mw_stats: Dict[Tuple[str, str, str], Tuple[Optional[float], Optional[float], Optional[float], str, str]],
                           kw_stats: Dict[Tuple[str, str], Tuple[Optional[float], Optional[float], List[Tuple[str, str, float, float]]]],
                           spearman_stats: Dict[Tuple[str, str], Tuple[Optional[float], Optional[float]]],
                           output_path: Path, n_episodes: int) -> None:
    """Escribe el informe final Markdown sin juicios de valor ni emoticons.

    Args:
        all_results: Datos por episodio.
        summaries: Sumarios descriptivos.
        mw_stats: Pruebas Mann-Whitney U.
        kw_stats: Pruebas Kruskal-Wallis con Bonferroni.
        spearman_stats: Correlaciones de Spearman.
        output_path: Archivo MD final.
        n_episodes: Numero de episodios por combinacion.
    """
    lines = []
    lines.append("# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT\n")
    lines.append(f"Fecha: {time.strftime('%Y-%m-%d')}\n")
    lines.append(f"Configuracion del experimento: n={n_episodes} episodios por combinacion de modelo, ciudad y nivel de caos.\n")
    lines.append("Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).\n")
    lines.append("Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.\n\n")

    if n_episodes < 30:
        lines.append(f"> ADVERTENCIA: El tamano de muestra por combinacion es menor a 30 episodios (n = {n_episodes}). "
                     "Esto puede limitar la potencia estadistica de las pruebas realizadas y aumentar la probabilidad de errores tipo II. "
                     "Los resultados de significancia deben interpretarse considerando esta limitacion.\n\n")

    lines.append("---\n\n")

    # Tabla 1
    lines.append("## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])\n\n")
    lines.append("| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |\n")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|\n")
    for s in summaries:
        ci_str = f"[{s['delay_ci95_lower']:.1f}, {s['delay_ci95_upper']:.1f}]"
        lines.append(
            f"| {s['city']} | {s['model']} | {s['chaos_level']} | {s['n']} "
            f"| {s['delay_median']:.1f} | {s['delay_iqr']:.1f} | {ci_str} "
            f"| {s['gini_median']:.4f} | {s['gini_iqr']:.4f} "
            f"| {s['cvar90_median']:.1f} | {s['collapse_rate_pct']:.1f}% |\n"
        )
    lines.append("\n")

    # Tabla 2
    lines.append("## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)\n\n")
    lines.append("| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |\n")
    lines.append("|---|---|---|---|---|\n")
    for s in summaries:
        co2_kg = s.get("co2_median", 0.0) / 1000000.0
        fuel_L = s.get("fuel_median", 0.0) / 740000.0
        lines.append(
            f"| {s['city']} | {s['model']} | {s['chaos_level']} "
            f"| {co2_kg:.2f} | {fuel_L:.3f} |\n"
        )
    lines.append("\n")

    # Tabla 3
    lines.append("## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)\n\n")
    lines.append("| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |\n")
    lines.append("|---|---|---|---|---|---|---|---|\n")
    for key, row in mw_stats.items():
        city, chaos, metric = key
        U, p, r, sig, mag = row
        if U is None or p is None:
            lines.append(f"| {city} | {chaos} | {metric} | N/A | N/A | N/A | N/A | N/A |\n")
        else:
            lines.append(
                f"| {city} | {chaos} | {metric} | {U:.1f} | {p:.4f} | {sig} | {r:.3f} | {mag} |\n"
            )
    lines.append("\n")

    # Tabla 4
    lines.append("## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc\n\n")
    lines.append("### Pruebas Globales de Kruskal-Wallis\n\n")
    lines.append("| Ciudad | Caos | H stat | p-valor | Signif. |\n")
    lines.append("|---|---|---|---|---|\n")
    for key, row in kw_stats.items():
        city, chaos = key
        H, p, _ = row
        if H is None or p is None:
            lines.append(f"| {city} | {chaos} | N/A | N/A | N/A |\n")
        else:
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
            lines.append(f"| {city} | {chaos} | {H:.1f} | {p:.4f} | {sig} |\n")
    lines.append("\n")
    
    lines.append("### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)\n\n")
    lines.append("| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |\n")
    lines.append("|---|---|---|---|---|---|---|\n")
    for key, row in kw_stats.items():
        city, chaos = key
        _, _, post_hoc = row
        for ma, mb, p_raw, p_adj in post_hoc:
            sig = "***" if p_adj < 0.001 else "**" if p_adj < 0.01 else "*" if p_adj < 0.05 else "ns"
            lines.append(f"| {city} | {chaos} | {ma} | {mb} | {p_raw:.4f} | {p_adj:.4f} | {sig} |\n")
    lines.append("\n")

    # Tabla 5
    lines.append("## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)\n\n")
    lines.append("| Ciudad | Modelo | Spearman rho | p-valor | Signif. |\n")
    lines.append("|---|---|---|---|---|\n")
    for key, row in spearman_stats.items():
        city, model = key
        rho, p = row
        if rho is None or p is None:
            lines.append(f"| {city} | {model} | N/A | N/A | N/A |\n")
        else:
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
            lines.append(f"| {city} | {model} | {rho:.3f} | {p:.4f} | {sig} |\n")
    lines.append("\n")

    lines.append("---\n\n")
    lines.append("## Notas Metodologicas\n\n")
    lines.append("1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.\n")
    lines.append("2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.\n")
    lines.append("3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.\n")
    lines.append("4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.\n")
    lines.append("5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).\n")
    lines.append("6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    logging.info(f"Reporte guardado en: {output_path}")

# ─── Validaciones Pre-Ejecución ─────────────────────────────────────────────

def validate_environment(root_dir: Path) -> bool:
    """Verifica la validez y requisitos del entorno.

    Args:
        root_dir: Directorio raiz del proyecto.

    Returns:
        bool: True si todo es correcto, False si hay error.
    """
    if sys.version_info < (3, 8):
        logging.error(f"Version de Python no compatible: {sys.version}. Se requiere >= 3.8")
        return False
        
    try:
        usage = shutil.disk_usage(str(root_dir))
        free_mb = usage.free / (1024 * 1024)
        if free_mb < 50.0:
            logging.error(f"Espacio en disco insuficiente: {free_mb:.1f} MB. Se requiere >= 50 MB.")
            return False
    except Exception as e:
        logging.warning(f"No se pudo determinar el espacio libre en disco: {e}")
        
    sumo_home = os.environ.get("SUMO_HOME", "")
    if not sumo_home:
        typical_win_path = r"C:\Program Files (x86)\Eclipse\Sumo"
        if os.path.exists(typical_win_path):
            os.environ["SUMO_HOME"] = typical_win_path
            logging.info(f"Asignado SUMO_HOME predeterminado en Windows: {typical_win_path}")
        else:
            logging.error("SUMO_HOME no esta configurado.")
            return False
            
    sumo_bin = shutil.which("sumo") or os.path.exists(os.path.join(os.environ.get("SUMO_HOME", ""), "bin", "sumo.exe")) or os.path.exists(os.path.join(os.environ.get("SUMO_HOME", ""), "bin", "sumo"))
    if not sumo_bin:
        logging.error("No se localizo el binario de SUMO.")
        return False
        
    try:
        import traci
    except ImportError:
        logging.error("Libreria 'traci' no importable.")
        return False
        
    try:
        import scipy.stats as stats
    except ImportError:
        logging.error("Libreria 'scipy' no disponible. Instalar con pip install scipy.")
        return False
        
    return True


def validate_models(root_dir: Path, models_list: List[str]) -> bool:
    """Verifica que los modelos a evaluar existan.

    Args:
        root_dir: Directorio raiz.
        models_list: Modelos cargados.

    Returns:
        bool: True si todo existe, False de lo contrario.
    """
    for model_name in models_list:
        if model_name in ["fixed_time_opt", "random"]:
            continue
        model_path = root_dir / "outputs" / "models" / f"{model_name}.zip"
        if not model_path.exists():
            logging.error(f"Modelo no encontrado: {model_path}")
            return False
    return True


def validate_networks(root_dir: Path, cities_list: List[str], city_configs: List[Tuple[str, str, Optional[float]]]) -> bool:
    """Verifica que los archivos net.xml de las ciudades existan.

    Args:
        root_dir: Directorio raiz.
        cities_list: Ciudades seleccionadas.
        city_configs: Configuracion total.

    Returns:
        bool: True si existen todas, False si falta alguna.
    """
    city_map = {c[0]: c[1] for c in city_configs}
    for city in cities_list:
        if city not in city_map:
            logging.error(f"Ciudad no configurada: {city}")
            return False
        net_file = city_map[city]
        net_path = root_dir / "sumo_configs" / "networks" / net_file
        if not net_path.exists():
            logging.error(f"Red no encontrada para {city}: {net_path}")
            return False
    return True

# ─── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    """Procedimiento principal para parsear argumentos y ejecutar la evaluacion."""
    parser = argparse.ArgumentParser(
        description="Evaluacion de Transferencia Zero-Shot Robusta N=30"
    )
    parser.add_argument("--episodes", type=int, default=30,
                        help="Numero de episodios por combinacion (default: 30)")
    parser.add_argument("--models", nargs="+",
                        default=["ppo_coop_ideal", "ppo_coop_chaos", "ppo_chaos", "fixed_time_opt", "random"],
                        help="Modelos a evaluar (default: todos)")
    parser.add_argument("--cities", nargs="+",
                        default=["Barcelona", "Quito", "Bogota", "Berlin", "Madrid", "CDMX"],
                        help="Ciudades a evaluar (default: todas)")
    parser.add_argument("--chaos-levels", nargs="+",
                        default=["low", "mid", "mid_high", "high", "extreme"],
                        help="Niveles de caos a evaluar (default: todos)")
    parser.add_argument("--mode", choices=["single_agent", "multi_agent"], default="multi_agent",
                        help="Modo de evaluacion (default: multi_agent)")
    parser.add_argument("--steps", type=int, default=720,
                        help="Pasos por episodio (default: 720)")
    parser.add_argument("--gui", action="store_true",
                        help="Ejecutar en modo visual con sumo-gui")
    parser.add_argument("--prefix", type=str, default="",
                        help="Prefijo personalizado para los archivos de salida (evita conflictos en ejecucion paralela).")
    parser.add_argument("--port-offset", type=int, default=0,
                        help="Offset para el puerto de TraCI para permitir paralelizar.")
    parser.add_argument("--with-behavioral-chaos", action="store_true",
                        help="Activa el LatamChaosManager (conductores imprudentes) durante la evaluacion de transferencia.")
    parser.add_argument("--chaos-prob", type=float, default=0.30,
                        help="Probabilidad de asignar comportamiento imprudente a cada vehiculo (default: 0.30).")
    parser.add_argument("--workers", type=int, default=7,
                        help="Numero de trabajadores paralelos para evaluar episodios (default: 7).")

    args = parser.parse_args()

    # Reproducibilidad global
    import random
    random.seed(42)
    np.random.seed(42)
    try:
        import torch
        torch.manual_seed(42)
    except ImportError:
        pass
    set_random_seed(42)

    # Validaciones previas
    if not validate_environment(ROOT):
        logging.error("Fallo la validacion del entorno de ejecucion.")
        sys.exit(1)

    if not validate_models(ROOT, args.models):
        logging.error("Fallo la validacion de modelos.")
        sys.exit(1)

    if not validate_networks(ROOT, args.cities, CITY_CONFIGS):
        logging.error("Fallo la validacion de redes viales.")
        sys.exit(1)

    # Cargar modelos y baselines
    models = {}
    for model_name in args.models:
        if model_name == "fixed_time_opt":
            models[model_name] = FixedTimeOptAgent(num_phases=4)
        elif model_name == "random":
            models[model_name] = RandomAgent(num_phases=4)
        else:
            model_path = ROOT / "outputs" / "models" / f"{model_name}.zip"
            try:
                models[model_name] = PPO.load(str(model_path), device="cpu")
            except Exception as e:
                logging.error(f"Fallo al cargar modelo PPO {model_name}: {e}")
                sys.exit(1)

    # Resolver nombres y mapas de red de ciudades activas
    active_cities = []
    city_map = {c[0]: (c[1], c[2]) for c in CITY_CONFIGS}
    for city_name in args.cities:
        if city_name in city_map:
            active_cities.append((city_name, city_map[city_name][0], city_map[city_name][1]))

    # Ejecucion principal
    all_results = []
    
    for model_name, model in models.items():
        for city_name, net_file, lat_res in active_cities:
            net_path = ROOT / "sumo_configs" / "networks" / net_file
            
            for chaos in args.chaos_levels:
                # Generacion de rutas especifica por modo
                if args.mode == "multi_agent":
                    route_path = generate_random_traffic(net_path, args.steps, chaos, is_multi_agent=True)
                else:
                    route_path = generate_stress_traffic(net_path, args.steps, chaos)
                
                res = evaluate_transfer_n_episodes(
                    model=model,
                    model_name=model_name,
                    city=city_name,
                    chaos_level=chaos,
                    net_path=net_path,
                    route_path=route_path,
                    n_episodes=args.episodes,
                    steps_limit=args.steps,
                    lateral_res=lat_res,
                    use_gui=args.gui,
                    mode=args.mode,
                    with_behavioral_chaos=args.with_behavioral_chaos,
                    chaos_prob=args.chaos_prob,
                    workers=args.workers
                )
                all_results.extend(res)

    # Exportar resultados detallados
    results_dir = ROOT / "outputs" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Prefijo de salida: distingue entre evaluacion con y sin caos conductual
    behavioral_tag = "_latam_behavioral" if getattr(args, 'with_behavioral_chaos', False) else ""
    if args.prefix:
        file_prefix = args.prefix
    elif len(args.chaos_levels) == 1:
        file_prefix = f"transfer_n30_{args.mode}_{args.chaos_levels[0]}{behavioral_tag}"
    else:
        file_prefix = f"transfer_n30_{args.mode}{behavioral_tag}"
        
    detailed_path = results_dir / f"{file_prefix}_detailed.csv"
    if all_results:
        keys = list(all_results[0].keys())
        with open(detailed_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_results)
            
    # Calcular sumarios descriptivos
    summaries = []
    for city_name, _, _ in active_cities:
        for model_name in models:
            for chaos in args.chaos_levels:
                s = compute_summary(all_results, city_name, model_name, chaos)
                if s is not None:
                    summaries.append(s)
                    
    # Exportar sumarios descriptivos
    summary_path = results_dir / f"{file_prefix}_summary.csv"
    if summaries:
        keys = list(summaries[0].keys())
        with open(summary_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(summaries)

    # Calcular pruebas estadisticas
    # 1. Mann-Whitney U: ppo_coop_chaos vs ppo_coop_ideal por ciudad y caos
    mw_stats = {}
    metrics_to_test = [
        ("delay_mean", "Delay"),
        ("gini_mean", "Gini"),
        ("cvar_90", "CVaR90")
    ]
    
    if "ppo_coop_chaos" in models and "ppo_coop_ideal" in models:
        for city_name, _, _ in active_cities:
            for chaos in args.chaos_levels:
                for metric_key, metric_label in metrics_to_test:
                    a = [r[metric_key] for r in all_results if r["city"] == city_name and r["model"] == "ppo_coop_chaos" and r["chaos_level"] == chaos]
                    b = [r[metric_key] for r in all_results if r["city"] == city_name and r["model"] == "ppo_coop_ideal" and r["chaos_level"] == chaos]
                    U, p, r, sig, mag = mann_whitney_u(a, b)
                    mw_stats[(city_name, chaos, metric_label)] = (U, p, r, sig, mag)

    # 2. Kruskal-Wallis global y post-hoc de Bonferroni por ciudad y caos (para delay_mean)
    kw_stats = {}
    import scipy.stats as stats
    for city_name, _, _ in active_cities:
        for chaos in args.chaos_levels:
            groups = {}
            for model_name in models:
                subset = [r["delay_mean"] for r in all_results if r["city"] == city_name and r["model"] == model_name and r["chaos_level"] == chaos]
                if subset:
                    groups[model_name] = subset
            
            if len(groups) > 2:
                try:
                    stat, p = stats.kruskal(*groups.values())
                    post_hoc = compute_post_hoc_bonferroni(groups)
                    kw_stats[(city_name, chaos)] = (float(stat), float(p), post_hoc)
                except Exception:
                    kw_stats[(city_name, chaos)] = (None, None, [])
            elif len(groups) == 2:
                try:
                    keys = list(groups.keys())
                    stat, p = stats.mannwhitneyu(groups[keys[0]], groups[keys[1]], alternative="two-sided")
                    kw_stats[(city_name, chaos)] = (float(stat), float(p), [(keys[0], keys[1], float(p), float(p))])
                except Exception:
                    kw_stats[(city_name, chaos)] = (None, None, [])
            else:
                kw_stats[(city_name, chaos)] = (None, None, [])

    # 3. Analisis de tendencia: Spearman por modelo y ciudad (caos_level ordinal vs delay_mean)
    spearman_stats = {}
    chaos_ranks = {"low": 1, "mid": 2, "mid_high": 3, "high": 4, "extreme": 5}
    for city_name, _, _ in active_cities:
        for model_name in models:
            subset = [r for r in all_results if r["city"] == city_name and r["model"] == model_name]
            if subset:
                x = [chaos_ranks[r["chaos_level"]] for r in subset]
                y = [r["delay_mean"] for r in subset]
                rho, p = spearman_corr(x, y)
                spearman_stats[(city_name, model_name)] = (rho, p)
            else:
                spearman_stats[(city_name, model_name)] = (None, None)

    # Generar informe Markdown final
    report_path = results_dir / f"{file_prefix}_report.md"
    write_markdown_report(all_results, summaries, mw_stats, kw_stats, spearman_stats, report_path, args.episodes)

    logging.info("Evaluacion finalizada correctamente.")


if __name__ == "__main__":
    main()
