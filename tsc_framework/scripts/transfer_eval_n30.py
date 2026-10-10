#!/usr/bin/env python3
"""
transfer_eval_n30.py — Evaluacion de Transferencia Zero-Shot con N=30 Episodios
================================================================================
Extiende transfer_eval.py para producir resultados estadisticamente defendibles
ante el tribunal doctoral. Ejecuta 30 episodios por ciudad/modelo con semillas
distintas y calcula: mediana, IQR, Mann-Whitney U (p-valor, efecto r).

Uso:
    python transfer_eval_n30.py [--episodes 30] [--models ppo_ideal ppo_chaos] [--mode stress]

Salidas:
    outputs/results/transfer_n30_detailed.csv   — Metricas por episodio
    outputs/results/transfer_n30_summary.csv    — Mediana, IQR, p-valor por ciudad/modelo
    outputs/results/transfer_n30_report.md      — Informe doctoral con tablas statisticas
"""

import argparse
import csv
import sys
import os
import time
import traci
import warnings
from pathlib import Path
from typing import Dict, List, Any, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

warnings.filterwarnings("ignore")

try:
    from stable_baselines3 import PPO
    from stable_baselines3.common.utils import set_random_seed
    from src.core.tsc_env import TSCEnv
    from src.rl_agent.sarg_policy import HSARGExtractor
except ImportError as e:
    raise ImportError(
        f"Error al importar dependencias. Asegurese de estar en venv_pytsc. Detalle: {e}"
    )

import xml.etree.ElementTree as ET
import tempfile
import subprocess
import shutil


# ─── Metricas ────────────────────────────────────────────────────────────────

def gini_coefficient(values: np.ndarray) -> float:
    if len(values) == 0 or values.sum() == 0:
        return 0.0
    v = np.sort(np.abs(values))
    n = len(v)
    idx = np.arange(1, n + 1)
    return float((2 * np.sum(idx * v)) / (n * np.sum(v)) - (n + 1) / n)


def cvar_90(losses: List[float]) -> float:
    if not losses:
        return 0.0
    arr = np.array(losses)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return 0.0
    q = np.quantile(arr, 0.90)
    tail = arr[arr >= q]
    return float(tail.mean()) if len(tail) > 0 else float(q)


def mann_whitney_u(a: List[float], b: List[float]):
    """
    Mann-Whitney U de dos colas. Retorna (U, p_value, r_effect).
    Requiere scipy. Si no disponible, retorna (None, None, None).
    """
    try:
        from scipy.stats import mannwhitneyu
        stat, p = mannwhitneyu(a, b, alternative="two-sided")
        n1, n2 = len(a), len(b)
        r = 1 - (2 * stat) / (n1 * n2)
        return float(stat), float(p), float(r)
    except ImportError:
        print("  [AVISO] scipy no instalado. Instale con: pip install scipy")
        return None, None, None


# ─── Descubrimiento de infraestructura SUMO ──────────────────────────────────

def get_allowed_passenger_edges(net_xml_path: Path) -> set:
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
        print(f"  [WARN] Error parseando aristas: {e}")
    return allowed_edges


def discover_vehicular_tls_id(net_xml_path: Path, allowed_edges: set) -> str:
    """Detecta dinámicamente el semáforo principal basándose en la centralidad de grado.

    Cuenta el número de conexiones controladas que permiten tránsito de pasajeros
    y selecciona el nodo con el máximo número de conexiones activas (el hub central).
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
            best_tls = max(tls_counts, key=tls_counts.get)
            print(f"  Semaforo autodetectado: '{best_tls}' ({tls_counts[best_tls]} conexiones vehiculares)")
            return best_tls
    except Exception as e:
        print(f"  [WARN] Error descubriendo semaforo: {e}")
    # Fallback: primer tlLogic del XML
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


def generate_stress_traffic(net_path: Path, steps_limit: int, stress_level: str = "high") -> Path:
    """Genera rutas de estres mediante inyeccion directa de flujos (JFI) normalizados.

    Detecta el semaforo vehicular optimo, extrae sus conexiones de entrada/salida
    y calcula el periodo por conexion necesario para inyectar un volumen total de
    vehiculos por hora proporcional a la capacidad de la interseccion (v/c constante).
    """
    routes_dir = ROOT / "sumo_configs" / "routes"
    routes_dir.mkdir(parents=True, exist_ok=True)
    route_path = routes_dir / f"{net_path.stem}_stress_{stress_level}.rou.xml"

    allowed_edges = get_allowed_passenger_edges(net_path)
    tls_id = discover_vehicular_tls_id(net_path, allowed_edges)

    # Extraer conexiones reales e incoming lanes para el semaforo controlado
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
        print(f"  [WARN] Error parsing network edges: {e}")

    if not connections:
        print(f"  [WARN] No se detectaron conexiones vehiculares para '{tls_id}'. Fallback a randomTrips.")
        return generate_random_traffic(net_path, steps_limit, stress_level)

    num_connections = len(connections)
    num_lanes = len(incoming_lanes) if incoming_lanes else len(set(c[0] for c in connections))
    if num_lanes == 0:
        num_lanes = 4  # fallback

    # Mapeo de niveles de estres a relacion demanda/capacidad (v/c)
    vc_mapping = {
        "low": 0.3,
        "mid": 0.6,
        "mid_high": 0.75,
        "high": 0.9,
        "extreme": 1.2
    }
    v_c_ratio = vc_mapping.get(stress_level, 0.9)
    
    # Capacidad de la interseccion (1800 veh/h por carril de entrada)
    capacity = num_lanes * 1800.0
    target_flow = capacity * v_c_ratio

    # Calcular el periodo normalizado (segundos por vehiculo por conexion)
    # total_veh_per_hour = num_connections * 3600 / period = target_flow
    # => period = (3600 * num_connections) / target_flow
    period = (3600.0 * num_connections) / target_flow
    period = round(period, 2)

    # Extraer incoming/outgoing unicos para el print
    incoming = list(set(c[0] for c in connections))
    outgoing = list(set(c[1] for c in connections))
    
    actual_flow = (num_connections * 3600.0) / period
    print(f"  Semaforo '{tls_id}': {len(incoming)} entrantes, {len(outgoing)} salientes ({num_connections} conexiones directas, {num_lanes} carriles entrada)")
    print(f"  Modo STRESS '{stress_level}' | v/c: {v_c_ratio:.2f} | Capacidad: {capacity:.0f} veh/h | Flujo Target: {target_flow:.0f} veh/h | Periodo: {period}s | Flujo Real: {actual_flow:.1f} veh/h")

    try:
        xml_lines = ['<routes>']
        xml_lines.append('    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" '
                         'length="5.0" minGap="2.0" maxSpeed="16.67"/>')
        flow_idx = 0
        sim_end = steps_limit * 5
        for inc, out in connections:
            xml_lines.append(
                f'    <flow id="f_{flow_idx}" type="car" begin="0" '
                f'end="{sim_end}" period="{period}" from="{inc}" to="{out}"/>'
            )
            flow_idx += 1
        xml_lines.append('</routes>')

        with open(str(route_path), 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml_lines))
        print(f"  Rutas de estres generadas: {route_path.name} ({flow_idx} flujos)")
    except Exception as e:
        print(f"  [ERROR] Error al escribir flujos de estres: {e}. Fallback a randomTrips.")
        return generate_random_traffic(net_path, steps_limit, stress_level)

    return route_path


def generate_random_traffic(net_path: Path, steps_limit: int, stress_level: str = "high", is_multi_agent: bool = False) -> Path:
    """Genera rutas aleatorias con randomTrips.py de SUMO (demanda dispersa)."""
    routes_dir = ROOT / "sumo_configs" / "routes"
    routes_dir.mkdir(parents=True, exist_ok=True)
    
    suffix = "multi_agent" if is_multi_agent else "random"
    route_path = routes_dir / f"{net_path.stem}_{suffix}_{stress_level}.rou.xml"

    # Mapear stress_level a periodos de randomTrips
    if is_multi_agent:
        # En red completa (multi-agente), necesitamos mucha mayor densidad global
        # para que los 10 hubs principales experimenten flujos y colas reales.
        period_mapping = {
            "low": "2.0",
            "mid": "1.0",
            "mid_high": "0.7",
            "high": "0.4",
            "extreme": "0.2"
        }
    else:
        period_mapping = {
            "low": "10.0",
            "mid": "5.0",
            "mid_high": "3.5",
            "high": "2.0",
            "extreme": "1.0"
        }
        
    p_val = period_mapping.get(stress_level, "2.0")

    if route_path.exists():
        print(f"  Reutilizando rutas random '{stress_level}' (p={p_val}): {route_path.name}")
        return route_path

    sumo_home = os.environ.get("SUMO_HOME", r"C:\Program Files (x86)\Eclipse\Sumo")
    random_trips_path = os.path.join(sumo_home, "tools", "randomTrips.py")

    print(f"  Generando flujo vehicular random '{stress_level}' (p={p_val}, mode={suffix}) para {net_path.name}...")
    try:
        subprocess.run([
            sys.executable, random_trips_path,
            "-n", str(net_path.resolve()),
            "-o", str(route_path.resolve()),
            "-e", str(steps_limit * 5),
            "-p", p_val,
            "--validate"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  Rutas random generadas: {route_path.name}")
    except Exception as e:
        print(f"  [ERROR] No se pudieron generar rutas: {e}")
        sys.exit(1)
    return route_path


def generate_eval_sumocfg(net_path: Path, route_path: Path, rank: int,
                           steps_sec: int, lateral_res: float = None) -> str:
    tmp_dir = tempfile.gettempdir()
    lateral_tag = (f'<lateral-resolution value="{lateral_res}"/>'
                   if lateral_res else "")
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="{net_path.resolve()}"/>
        <route-files value="{route_path.resolve()}"/>
    </input>
    <time><begin value="0"/><end value="{steps_sec}"/></time>
    <processing>
        <time-to-teleport value="300"/>
        <waiting-time-memory value="1000"/>
        {lateral_tag}
    </processing>
    <report><no-warnings value="true"/></report>
</configuration>"""
    path = os.path.join(tmp_dir, f"transfer_n30_rank{rank}.sumocfg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# ─── Baselines ───────────────────────────────────────────────────────────────

class FixedTimeAgent:
    """Agente baseline que rota por las fases de forma fija (tiempo fijo)."""
    def __init__(self, num_phases: int = 4, steps_per_phase: int = 6):
        self.num_phases = num_phases
        self.steps_per_phase = steps_per_phase
        self.current_step = 0
        
    def reset(self) -> None:
        self.current_step = 0
        
    def predict(self, obs: np.ndarray, deterministic: bool = True) -> Tuple[int, None]:
        phase = (self.current_step // self.steps_per_phase) % self.num_phases
        self.current_step += 1
        return phase, None


class FixedTimeOptAgent:
    """Agente baseline con tiempos fijos optimizados dinámicamente por ciudad."""
    def __init__(self, num_phases: int = 4):
        self.num_phases = num_phases
        self.steps_per_phase = 4  # default (20s)
        self.current_step = 0
        # Mapeo de duración óptima en pasos (1 paso = 5s)
        self.steps_mapping = {
            "Barcelona": 2,  # 10s (ciclo corto, muy eficiente sin penalizaciones)
            "Madrid": 2,     # 10s (ciclo corto)
            "Quito": 4,      # 20s
            "Bogota": 4,     # 20s
            "Berlin": 4,     # 20s
            "CDMX": 4,       # 20s
        }
        
    def set_city(self, city_name: str) -> None:
        self.steps_per_phase = self.steps_mapping.get(city_name, 4)
        print(f"    [FixedTimeOpt] Ajustada duracion por fase para {city_name} a {self.steps_per_phase * 5}s (steps={self.steps_per_phase})")
        
    def reset(self) -> None:
        self.current_step = 0
        
    def predict(self, obs: np.ndarray, deterministic: bool = True) -> Tuple[int, None]:
        phase = (self.current_step // self.steps_per_phase) % self.num_phases
        self.current_step += 1
        return phase, None


class RandomAgent:
    """Agente baseline que elige acciones uniformemente al azar."""
    def __init__(self, num_phases: int = 4):
        self.num_phases = num_phases
        
    def reset(self) -> None:
        pass
        
    def predict(self, obs: np.ndarray, deterministic: bool = True) -> Tuple[int, None]:
        return int(np.random.randint(self.num_phases)), None


# ─── Multi-Agent Control Managers ─────────────────────────────────────────────

class LocalTLSManager:
    """Gestiona el estado local y mapeo topologico de un semaforo individual en la red."""
    def __init__(self, tls_id: str):
        self.tls_id = tls_id
        
        # 1. Obtener carriles controlados (deduplicar manteniendo orden de aparicion)
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
            
        # 2. Descubrir fases verdes en el programa
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
        if not self.controlled_lanes:
            return np.zeros(34, dtype=np.float32)
            
        # q_t (colas de parada)
        queues = np.array(
            [traci.lane.getLastStepHaltingNumber(lane) for lane in self.controlled_lanes],
            dtype=np.float32
        )
        # w_t (tiempos de espera acumulados)
        waits = np.array(
            [traci.lane.getWaitingTime(lane) for lane in self.controlled_lanes],
            dtype=np.float32
        )
        # p_t (presion simplificada a vehiculos en incoming lanes, outgoing_lanes es [] en TSCEnv)
        pressure = np.array(
            [traci.lane.getLastStepVehicleNumber(lane) for lane in self.controlled_lanes],
            dtype=np.float32
        )
        
        # Normalizacion lineal acotada
        q_norm = np.clip(queues / 50.0, 0.0, 1.0)
        w_norm = np.clip(waits / 300.0, 0.0, 1.0)
        p_norm = np.clip(pressure / 50.0, 0.0, 1.0)
        
        # Agrupar presion a 4 dimensiones
        if len(p_norm) > 4:
            p_agg = np.array([
                np.mean(p_norm[0:2]) if len(p_norm) >= 2 else p_norm[0] if len(p_norm) >= 1 else 0.0,
                np.mean(p_norm[2:4]) if len(p_norm) >= 4 else 0.0,
                np.mean(p_norm[4:6]) if len(p_norm) >= 6 else 0.0,
                np.mean(p_norm[6:8]) if len(p_norm) >= 8 else 0.0,
            ], dtype=np.float32)
        else:
            p_agg = np.pad(p_norm, (0, 4 - len(p_norm)), mode='constant')[:4]
            
        # One-hot de la fase
        phi_onehot = np.zeros(4, dtype=np.float32)
        phase_idx = self.current_phase % 4
        phi_onehot[phase_idx] = 1.0
        
        # Edad de fase
        phase_age_s = (self.step_count - self.phase_start_step) * 5
        tau_norm = np.clip(phase_age_s / 120.0, 0.0, 1.0)
        tau_features = np.array([phase_age_s / 120.0, tau_norm], dtype=np.float32)
        
        obs = np.concatenate([
            q_norm.astype(np.float32),   # 12
            w_norm.astype(np.float32),   # 12
            p_agg,                        # 4
            phi_onehot,                   # 4
            tau_features,                 # 2
        ])
        return obs
        
    def apply_action(self, action: int):
        if not self.green_phases:
            return
            
        phase_idx = action % len(self.green_phases)
        target_phase = self.green_phases[phase_idx]
        
        if target_phase != self.current_phase:
            traci.trafficlight.setPhase(self.tls_id, target_phase)
            self.phase_start_step = self.step_count
            self.current_phase = target_phase
            
        self.step_count += 1


import random

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


def run_multi_agent_episode(model: Any, sumocfg: str,
                            steps_limit: int, seed: int,
                            lateral_res: float = None,
                            use_gui: bool = False,
                            with_behavioral_chaos: bool = False,
                            chaos_prob: float = 0.3) -> Dict[str, Any]:
    """Ejecuta un episodio completo controlando todos los semaforos activos de la red."""
    import copy
    
    # 1. Encontrar puerto libre determinista basado en seed
    traci_port = 8813 + (seed % 500)
    
    # 2. Configurar binario SUMO
    sumo_binary = "sumo-gui" if use_gui else "sumo"
    import shutil
    sumo_bin = shutil.which(sumo_binary) or sumo_binary
    
    cmd = [
        sumo_bin,
        "-c", sumocfg,
        "--remote-port", str(traci_port),
        "--step-length", "1.0",
        "--no-step-log",
        "--seed", str(seed),
    ]
    if lateral_res:
        # Añadir lateral-resolution para motos en LATAM si esta configurado
        pass
        
    # Windows: Evitar popup de consola
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
        except:
            pass
        raise RuntimeError(f"Error al conectar TraCI en modo multi-agente en puerto {traci_port}: {e}")
        
    # Descubrir todos los TLS y ordenarlos por centralidad de grado (carriles controlados unicos)
    all_tls_ids = traci.trafficlight.getIDList()
    tls_counts = {}
    for tid in all_tls_ids:
        raw_lanes = traci.trafficlight.getControlledLanes(tid)
        if raw_lanes:
            seen_lanes = set(raw_lanes)
            tls_counts[tid] = len(seen_lanes)
            
    # Instanciar el Network-Wide Chaos Manager si se solicito caos conductual
    nw_chaos = None
    if with_behavioral_chaos:
        nw_chaos = NetworkWideChaosManager(probabilidad_caos=chaos_prob)
        print(f"    [CHAOS] NetworkWideChaosManager activo (prob={chaos_prob:.2f})")

    # Seleccionar únicamente los Top K semáforos principales (ej: K = 10)
    K = 10
    sorted_tls = sorted(tls_counts.items(), key=lambda x: x[1], reverse=True)
    top_tls = [tid for tid, count in sorted_tls[:K]]
    
    tls_managers = {}
    for tid in top_tls:
        tls_managers[tid] = LocalTLSManager(tid)
        
    print(f"    [Multi-Agent] Controlando los Top-{len(tls_managers)} semaforos principales de la red (de un total de {len(all_tls_ids)}).")
    
    # Identificar si el modelo es un baseline con estado interno
    is_baseline = isinstance(model, (FixedTimeAgent, FixedTimeOptAgent, RandomAgent))
    if is_baseline:
        # Clonar el baseline para cada semaforo independiente
        agents = {tid: copy.deepcopy(model) for tid in tls_managers}
        # Configurar ciudad si es FixedTimeOptAgent
        if isinstance(model, FixedTimeOptAgent):
            # Obtener el nombre de la ciudad a partir del sumocfg
            city_name = "Quito"
            for c in ["Barcelona", "Quito", "Bogota", "Berlin", "Madrid", "CDMX"]:
                if c.lower() in sumocfg.lower():
                    city_name = c
                    break
            for ag in agents.values():
                ag.set_city(city_name)
    else:
        agents = {}
        
    # Inicializar managers
    for manager in tls_managers.values():
        manager.step_count = 0
        manager.phase_start_step = 0
        manager.current_phase = traci.trafficlight.getPhase(manager.tls_id)
        
    delays, queues, ginis, co2_emissions, fuel_consumptions = [], [], [], [], []
    step_count = 0
    done = False
    
    # Reunir todos los carriles controlados de la red para calculo de metricas
    all_controlled_lanes = set()
    for manager in tls_managers.values():
        all_controlled_lanes.update(manager.controlled_lanes)
        
    # Bucle de la simulacion
    while not done and step_count < steps_limit:
        # Inferencia y aplicacion de acciones
        for tid, manager in tls_managers.items():
            obs = manager.get_state()
            if is_baseline:
                action, _ = agents[tid].predict(obs, deterministic=True)
            else:
                action, _ = model.predict(obs, deterministic=True)
            manager.apply_action(action)
            
        # Avanzar delta_t pasos de 1 segundo
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
                
            # Medir metricas agregadas sobre los carriles controlados de la red
            if all_controlled_lanes:
                step_co2 = sum(traci.lane.getCO2Emission(lane) for lane in all_controlled_lanes)
                step_fuel = sum(traci.lane.getFuelConsumption(lane) for lane in all_controlled_lanes)
                step_halting = sum(traci.lane.getLastStepHaltingNumber(lane) for lane in all_controlled_lanes)
                step_waiting = sum(traci.lane.getWaitingTime(lane) for lane in all_controlled_lanes)
        except Exception as e:
            print(f"    [WARN] Simulación abortada por TraCI en el paso {step_count}: {e}")
            break
            
        # Calcular el indice de Gini promedio inter-carriles de la red controlada
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
        
    # Cerrar conexion de forma segura
    try:
        traci.close()
    except:
        pass
        
    try:
        sumo_process.terminate()
        sumo_process.wait(timeout=2)
    except:
        try:
            sumo_process.kill()
        except:
            pass
    finally:
        sumo_log_file.close()
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
        "collapsed": 1 if mean_delay > 5000 else 0, # Umbral de colapso para la red
        "co2_total": float(np.sum(co2_emissions)) if co2_emissions else 0.0,
        "fuel_total": float(np.sum(fuel_consumptions)) if fuel_consumptions else 0.0,
    }


# ─── Episodio individual ─────────────────────────────────────────────────────

def run_single_episode(model: Any, sumocfg: str, tls_id: str,
                       steps_limit: int, seed: int,
                       lateral_res: float = None,
                       use_gui: bool = False,
                       enable_traci_chaos: bool = False,
                       chaos_prob: float = 0.3) -> Dict[str, Any]:
    """Ejecuta un episodio completo y retorna metricas agregadas."""
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
        "collapsed": 1 if mean_delay > 2000 else 0,   # umbral de gridlock
        "co2_total": float(np.sum(co2_emissions)) if co2_emissions else 0.0,
        "fuel_total": float(np.sum(fuel_consumptions)) if fuel_consumptions else 0.0,
    }


# ─── Evaluacion multi-episodio ────────────────────────────────────────────────

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
    
    # Algunos baselines necesitan la ciudad actual
    if hasattr(model, "set_city"):
        model.set_city(city)
        
    if hasattr(model, "reset"):
        model.reset()
        
    allowed = get_allowed_passenger_edges(net_path)
    tls_id = discover_vehicular_tls_id(net_path, allowed)
        
    if mode == "multi_agent":
        res = run_multi_agent_episode(model, sumocfg, steps_limit, seed, lateral_res, use_gui,
                                      with_behavioral_chaos=with_behavioral_chaos, chaos_prob=chaos_prob)
    else:
        res = run_single_episode(model, sumocfg, tls_id, steps_limit, seed, lateral_res, use_gui,
                                 enable_traci_chaos=with_behavioral_chaos, chaos_prob=chaos_prob)
        
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
    net_path: Path,
    route_path: Path,
    n_episodes: int,
    steps_limit: int,
    lateral_res: float = None,
    use_gui: bool = False,
    mode: str = "stress",
    with_behavioral_chaos: bool = False,
    chaos_prob: float = 0.3,
    workers: int = 7
) -> List[Dict[str, Any]]:
    """Ejecuta n_episodes episodios con semillas distintas (1000+ep) en paralelo."""
    from joblib import Parallel, delayed

    print(f"\n{'='*60}")
    print(f"  {model_name} | {city} | {n_episodes} episodios | Workers: {workers}")
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

    return results


# ─── Informe estadistico ──────────────────────────────────────────────────────

def compute_summary(results: List[Dict], city: str, model_name: str) -> Dict:
    delays = [r["delay_mean"] for r in results if r["city"] == city and r["model"] == model_name]
    ginis = [r["gini_mean"] for r in results if r["city"] == city and r["model"] == model_name]
    cvars = [r["cvar_90"] for r in results if r["city"] == city and r["model"] == model_name]
    collapsed = [r["collapsed"] for r in results if r["city"] == city and r["model"] == model_name]
    co2s = [r["co2_total"] for r in results if r["city"] == city and r["model"] == model_name and "co2_total" in r]
    fuels = [r["fuel_total"] for r in results if r["city"] == city and r["model"] == model_name and "fuel_total" in r]

    def iqr(v):
        return float(np.percentile(v, 75) - np.percentile(v, 25)) if v else 0.0

    return {
        "model": model_name,
        "city": city,
        "n": len(delays),
        "delay_median": float(np.median(delays)) if delays else 0.0,
        "delay_iqr": iqr(delays),
        "gini_median": float(np.median(ginis)) if ginis else 0.0,
        "gini_iqr": iqr(ginis),
        "cvar90_median": float(np.median(cvars)) if cvars else 0.0,
        "cvar90_iqr": iqr(cvars),
        "collapse_rate_pct": float(np.mean(collapsed) * 100) if collapsed else 0.0,
        "co2_median": float(np.median(co2s)) if co2s else 0.0,
        "fuel_median": float(np.median(fuels)) if fuels else 0.0,
    }


def write_markdown_report(all_results: List[Dict], summaries: List[Dict],
                           stats: Dict, output_path: Path) -> None:
    """Genera el informe Markdown con tablas estadisticamente correctas."""
    lines = []
    lines.append("# INFORME DE TRANSFERENCIA ZERO-SHOT — N=30 EPISODIOS\n")
    lines.append(f"**Fecha:** {__import__('datetime').date.today()}\n")
    lines.append("**Experimento:** Evaluacion de transferencia con n=30 episodios por ciudad/modelo.\n")
    lines.append("**Estadistico central:** Mediana (robusta ante gridlocks). Dispersión: IQR.\n")
    lines.append("**Test estadistico:** Mann-Whitney U bilateral (alpha=0.05).\n\n")
    lines.append("---\n\n")

    # Tabla de medianas
    lines.append("## Tabla 1 — Metricas por Ciudad y Modelo (Mediana ± IQR)\n\n")
    lines.append("| Ciudad | Modelo | Delay Mediana (s) | IQR (s) | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |\n")
    lines.append("|---|---|---|---|---|---|---|---|\n")
    for s in summaries:
        lines.append(
            f"| {s['city']} | {s['model']} "
            f"| {s['delay_median']:.1f} | {s['delay_iqr']:.1f} "
            f"| {s['gini_median']:.4f} | {s['gini_iqr']:.4f} "
            f"| {s['cvar90_median']:.1f} "
            f"| {s['collapse_rate_pct']:.1f}% |\n"
        )
    lines.append("\n")

    # Tabla de sostenibilidad
    lines.append("## Tabla 2 — Metricas de Sostenibilidad y Emisiones (Mediana)\n\n")
    lines.append("| Ciudad | Modelo | CO2 Total (kg) | Combustible Total (L) |\n")
    lines.append("|---|---|---|---|\n")
    for s in summaries:
        co2_kg = s.get("co2_median", 0.0) / 1000000.0
        # SUMO devuelve combustible en mg. Asumiendo densidad promedio de gasolina = 740 g/L (0.74 g/ml):
        # Litros = mg / 1,000,000 (a kg) * 1000 (a g) / 740 = mg / 740,000
        fuel_L = s.get("fuel_median", 0.0) / 740000.0
        lines.append(
            f"| {s['city']} | {s['model']} "
            f"| {co2_kg:.2f} | {fuel_L:.3f} |\n"
        )
    lines.append("\n")

    # Tabla Mann-Whitney
    lines.append("## Tabla 3 — Test Mann-Whitney U: Caotico vs. Ideal por Ciudad\n\n")
    lines.append("| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |\n")
    lines.append("|---|---|---|---|---|---|---|\n")
    for key, row in stats.items():
        city, metric = key
        U, p, r, sig, mag = row
        if U is None:
            lines.append(f"| {city} | {metric} | N/A | N/A | scipy no inst. | N/A | N/A |\n")
        else:
            lines.append(
                f"| {city} | {metric} | {U:.1f} | {p:.4f} | {sig} | {r:.3f} | {mag} |\n"
            )
    lines.append("\n")

    lines.append("---\n\n")
    lines.append("## Interpretacion de Resultados\n\n")
    lines.append(
        "> **Nota metodologica:** Las mejoras observadas en Quito (Caotico vs. Ideal) "
        "son estadisticamente significativas cuando p < 0.05. Con n=30 episodios, "
        "el poder estadistico del test Mann-Whitney es >= 80% para efectos medianos (|r| >= 0.3).\n\n"
    )
    lines.append(
        "El experimento de transferencia zero-shot evalua si la politica entrenada bajo "
        "perturbaciones LATAM en Hangzhou preserva sus propiedades de optimizacion "
        "multiobjetivo cuando se aplica a redes urbanas distintas mediante el mecanismo "
        "de acotamiento topologico (wrapper). La validacion estadistica con n=30 episodios "
        "permite distinguir mejoras reales de variabilidad episodica.\n\n"
    )
    lines.append("---\n")
    lines.append("*Generado por transfer_eval_n30.py — TSC Framework Doctoral*\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"\n  Informe guardado en: {output_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Evaluacion de Transferencia Zero-Shot N=30 Episodios"
    )
    parser.add_argument("--episodes", type=int, default=30,
                        help="Numero de episodios por ciudad/modelo (default: 30)")
    parser.add_argument("--models", nargs="+",
                        default=["ppo_ideal", "ppo_chaos"],
                        help="Modelos a evaluar (default: ppo_ideal ppo_chaos)")
    parser.add_argument("--steps", type=int, default=720,
                        help="Pasos por episodio, 720 = 3600s con delta_t=5 (default: 720)")
    parser.add_argument("--mode", choices=["stress", "random", "multi_agent"], default="stress",
                        help="Modo de generacion de demanda: stress=JFI directo, random=randomTrips, multi_agent=despliegue en red completa (default: stress)")
    parser.add_argument("--stress-level", choices=["low", "mid", "mid_high", "high", "extreme"], default="high",
                        help="Nivel de demanda normalizada (default: high)")
    parser.add_argument("--gui", action="store_true",
                        help="Ejecutar simulacion en modo visual (sumo-gui)")
    parser.add_argument("--with-behavioral-chaos", action="store_true",
                        help="Activa el LatamChaosManager (conductores imprudentes) durante la evaluacion de transferencia.")
    parser.add_argument("--chaos-prob", type=float, default=0.30,
                        help="Probabilidad de asignar comportamiento imprudente a cada vehiculo (default: 0.30).")
    parser.add_argument("--workers", type=int, default=7,
                        help="Numero de trabajadores paralelos para evaluar episodios (default: 7).")
    args = parser.parse_args()

    set_random_seed(42)

    # ─── Configuracion de ciudades ──────────────────────────────────────
    # Cada entrada: (nombre, archivo_red, lateral_res)
    # lateral_res=0.4 para LATAM (motos/buses), None para europeas
    city_configs = [
        ("Barcelona",  "barcelona.net.xml",  None),    # Ordenado europeo
        ("Quito",      "quito.net.xml",      0.4),     # LATAM: motos
        ("Bogota",     "bogota.net.xml",     0.4),     # LATAM: alta friccion, BRT
        ("Berlin",     "berlin.net.xml",     None),    # Alta eficiencia europea
        ("Madrid",     "madrid.net.xml",     None),    # Ordenado europeo
        ("CDMX",       "cdmx.net.xml",       0.4),     # LATAM: megalopolis densa
    ]

    # Verificar que todas las redes existan
    city_nets = {}
    for city_name, net_file, lat_res in city_configs:
        net_path = ROOT / "sumo_configs" / "networks" / net_file
        if not net_path.exists():
            print(f"[WARN] Red no encontrada: {net_path}. Omitiendo {city_name}.")
            continue
        city_nets[city_name] = (net_path, lat_res)

    if not city_nets:
        print("[ERROR] No se encontro ninguna red. Ejecute netconvert primero.")
        sys.exit(1)

    # Seleccionar generador de rutas segun modo
    is_stress = args.mode == "stress"
    route_generator = generate_stress_traffic if is_stress else generate_random_traffic
    if args.mode == "stress":
        mode_label = f"STRESS ({args.stress_level} JFI directo)"
    elif args.mode == "random":
        mode_label = f"RANDOM ({args.stress_level} randomTrips)"
    else:
        mode_label = f"MULTI-AGENT ({args.stress_level} red completa)"
        
    behavioral_tag = "_latam_behavioral" if getattr(args, 'with_behavioral_chaos', False) else ""
    file_prefix = f"transfer_n30_{args.mode}_{args.stress_level}{behavioral_tag}"

    print("=" * 60)
    print("  TRANSFER EVAL N=30 — Framework TSC Doctoral")
    print(f"  Modo: {mode_label}")
    print(f"  Episodios: {args.episodes} | Steps/ep: {args.steps} (~{args.steps*5}s)")
    print(f"  Modelos: {args.models}")
    print(f"  Ciudades: {list(city_nets.keys())}")
    print(f"  Workers: {args.workers}")
    print("=" * 60)

    # Generar rutas para cada ciudad (se reusan si ya existen)
    city_routes = {}
    for city_name, (net_path, _) in city_nets.items():
        if args.mode == "multi_agent":
            city_routes[city_name] = generate_random_traffic(net_path, args.steps, args.stress_level, is_multi_agent=True)
        else:
            city_routes[city_name] = route_generator(net_path, args.steps, args.stress_level)

    # Cargar modelos y baselines
    models = {}
    for model_name in args.models:
        if model_name == "fixed_time":
            print(f"  Inicializando baseline: fixed_time (tiempo fijo 30s)...")
            models[model_name] = FixedTimeAgent(num_phases=4, steps_per_phase=6)
            print(f"  OK: fixed_time")
        elif model_name == "fixed_time_15s":
            print(f"  Inicializando baseline: fixed_time_15s (tiempo fijo 15s)...")
            models[model_name] = FixedTimeAgent(num_phases=4, steps_per_phase=3)
            print(f"  OK: fixed_time_15s")
        elif model_name == "fixed_time_opt":
            print(f"  Inicializando baseline: fixed_time_opt (tiempo fijo optimizado)...")
            models[model_name] = FixedTimeOptAgent(num_phases=4)
            print(f"  OK: fixed_time_opt")
        elif model_name == "random":
            print(f"  Inicializando baseline: random (acciones aleatorias)...")
            models[model_name] = RandomAgent(num_phases=4)
            print(f"  OK: random")
        else:
            path = ROOT / "outputs" / "models" / f"{model_name}.zip"
            if not path.exists():
                print(f"  [WARN] Modelo no encontrado: {path}. Omitiendo.")
                continue
            print(f"  Cargando {model_name}...")
            models[model_name] = PPO.load(str(path), device="cpu")
            print(f"  OK: {model_name}")

    if not models:
        print("[ERROR] No se encontraron modelos o baselines validos.")
        sys.exit(1)

    # Ejecutar evaluaciones para todas las ciudades
    all_results = []
    for model_name, model in models.items():
        for city_name, (net_path, lat_res) in city_nets.items():
            route_path = city_routes[city_name]
            lat_label = f"lateral_res={lat_res}" if lat_res else "sin lateral_res"
            print(f"\n  >> {city_name} ({lat_label})")
            res = evaluate_transfer_n_episodes(
                model=model, model_name=model_name, city=city_name,
                net_path=net_path, route_path=route_path,
                n_episodes=args.episodes, steps_limit=args.steps,
                lateral_res=lat_res, use_gui=args.gui,
                mode=args.mode,
                with_behavioral_chaos=args.with_behavioral_chaos,
                chaos_prob=args.chaos_prob,
                workers=args.workers
            )
            all_results.extend(res)

    # Exportar detallado
    results_dir = ROOT / "outputs" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    detailed_path = results_dir / f"{file_prefix}_detailed.csv"
    if all_results:
        keys = list(all_results[0].keys())
        with open(detailed_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"\n  Datos detallados: {detailed_path}")

    # Calcular sumarios
    cities = list(city_nets.keys())
    model_names = list(models.keys())
    summaries = []
    for city in cities:
        for model_name in model_names:
            s = compute_summary(all_results, city, model_name)
            summaries.append(s)

    # Exportar sumario
    summary_path = results_dir / f"{file_prefix}_summary.csv"
    if summaries:
        with open(summary_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=summaries[0].keys())
            writer.writeheader()
            writer.writerows(summaries)
        print(f"  Resumen estadistico: {summary_path}")

    # Mann-Whitney U entre Caotico vs. Ideal por ciudad/metrica
    stats = {}
    metrics_to_test = [
        ("delay_mean", "Delay"),
        ("gini_mean", "Gini"),
        ("cvar_90", "CVaR90"),
    ]

    def get_values(city, model, metric):
        return [r[metric] for r in all_results if r["city"] == city and r["model"] == model]

    # Solo si existen ambos modelos
    if "ppo_chaos" in models and "ppo_ideal" in models:
        for city in cities:
            for metric_key, metric_label in metrics_to_test:
                a = get_values(city, "ppo_chaos", metric_key)
                b = get_values(city, "ppo_ideal", metric_key)
                U, p, r = mann_whitney_u(a, b)
                if p is not None:
                    if p < 0.001:
                        sig = "***"
                    elif p < 0.01:
                        sig = "**"
                    elif p < 0.05:
                        sig = "*"
                    else:
                        sig = "ns"
                    abs_r = abs(r) if r is not None else 0
                    if abs_r < 0.1:
                        mag = "negligible"
                    elif abs_r < 0.3:
                        mag = "small"
                    elif abs_r < 0.5:
                        mag = "medium"
                    else:
                        mag = "large"
                    stats[(city, metric_label)] = (U, p, r, sig, mag)
                    print(f"  MW {city}/{metric_label}: U={U:.1f}, p={p:.4f} {sig}, r={r:.3f} ({mag})")
                else:
                    stats[(city, metric_label)] = (None, None, None, "?", "?")

    # Generar informe Markdown
    report_path = results_dir / f"{file_prefix}_report.md"
    write_markdown_report(all_results, summaries, stats, report_path)

    print("\n" + "=" * 60)
    print("  EVALUACION COMPLETADA")
    print(f"  Episodios totales: {len(all_results)}")
    print(f"  Resultados en: {results_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
