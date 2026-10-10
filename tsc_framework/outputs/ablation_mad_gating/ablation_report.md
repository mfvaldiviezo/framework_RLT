==============================================================================
  ESTUDIO DE ABLACIÓN MAD-GATING — INFORME COMPLETO
  Para revisores IEEE T-ITS
==============================================================================

Total simulaciones: 1,200
Variantes: ['coopsarg_gating_off', 'coopsarg_gating_on', 'hsarg_gating_off', 'hsarg_gating_on']
Ciudades: ['Barcelona', 'Quito']
Chaos levels: ['low', 'mid', 'mid_high', 'high', 'extreme']

------------------------------------------------------------------------------
HIPÓTESIS DEL ESTUDIO
------------------------------------------------------------------------------

H₀ (nula):        El MAD-Gating NO afecta la equidad distributiva.
                   Gini(gating=ON) = Gini(gating=OFF)

H₁ (alternativa): El MAD-Gating MEJORA la equidad distributiva.
                   Gini(gating=ON) < Gini(gating=OFF)

Predicción: El efecto será MAYOR en Quito (topología lineal) que en
           Barcelona (grid isótropa), y MAYOR en Coop-SARG (doble
           gating) que en H-SARG (gating simple).

------------------------------------------------------------------------------
RESULTADOS: Gini con y sin MAD-Gating
------------------------------------------------------------------------------

Variante               Ciudad       Chaos       Gini_ON Gini_OFF        Δ Effect_r        p    Sig
------------------------------------------------------------------------------------------------
hsarg_gating_on        Quito        low          0.4480   0.4800  +0.0320    1.000   0.0000    ***
hsarg_gating_on        Quito        mid          0.4395   0.4929  +0.0534    1.000   0.0000    ***
hsarg_gating_on        Quito        mid_high     0.4482   0.4979  +0.0496    1.000   0.0000    ***
hsarg_gating_on        Quito        high         0.4372   0.5072  +0.0699    1.000   0.0000    ***
hsarg_gating_on        Quito        extreme      0.4454   0.5538  +0.1085    1.000   0.0000    ***
hsarg_gating_on        Barcelona    low          0.3577   0.3923  +0.0346    1.000   0.0000    ***
hsarg_gating_on        Barcelona    mid          0.3561   0.3887  +0.0326    1.000   0.0000    ***
hsarg_gating_on        Barcelona    mid_high     0.3525   0.3872  +0.0347    1.000   0.0000    ***
hsarg_gating_on        Barcelona    high         0.3629   0.4083  +0.0454    1.000   0.0000    ***
hsarg_gating_on        Barcelona    extreme      0.3671   0.4107  +0.0436    1.000   0.0000    ***
coopsarg_gating_on     Quito        low          0.4023   0.4764  +0.0741    1.000   0.0000    ***
coopsarg_gating_on     Quito        mid          0.3983   0.5273  +0.1290    1.000   0.0000    ***
coopsarg_gating_on     Quito        mid_high     0.3949   0.5353  +0.1403    1.000   0.0000    ***
coopsarg_gating_on     Quito        high         0.4096   0.5606  +0.1509    1.000   0.0000    ***
coopsarg_gating_on     Quito        extreme      0.4154   0.5809  +0.1655    1.000   0.0000    ***
coopsarg_gating_on     Barcelona    low          0.2917   0.3611  +0.0693    1.000   0.0000    ***
coopsarg_gating_on     Barcelona    mid          0.2790   0.3634  +0.0844    1.000   0.0000    ***
coopsarg_gating_on     Barcelona    mid_high     0.2974   0.3682  +0.0709    1.000   0.0000    ***
coopsarg_gating_on     Barcelona    high         0.2900   0.4086  +0.1185    1.000   0.0000    ***
coopsarg_gating_on     Barcelona    extreme      0.2983   0.4084  +0.1101    1.000   0.0000    ***

------------------------------------------------------------------------------
TEST AGREGADO (Quito, todas las variantes y chaos levels)
------------------------------------------------------------------------------

  Gini(gating=ON)  = 0.4239 ± 0.0213 (n=300)
  Gini(gating=OFF) = 0.5212 ± 0.0346 (n=300)
  Δ = +0.0973
  Mann-Whitney U = 0.0, p = 0.000000
  Effect size r = 1.000 (LARGE)

   Se RECHAZA H₀ con p < 0.001.
  El MAD-Gating mejora SIGNIFICATIVAMENTE la equidad en Quito.

------------------------------------------------------------------------------
TAMAÑO DEL EFECTO POR NIVEL DE CAOS (Coop-SARG, Quito)
------------------------------------------------------------------------------

        low: ΔGini = +0.0741 (gating OFF - gating ON)
        mid: ΔGini = +0.1290 (gating OFF - gating ON)
   mid_high: ΔGini = +0.1403 (gating OFF - gating ON)
       high: ΔGini = +0.1509 (gating OFF - gating ON)
    extreme: ΔGini = +0.1655 (gating OFF - gating ON)

------------------------------------------------------------------------------
TRADE-OFF: ¿El MAD-Gating perjudica el throughput?
------------------------------------------------------------------------------

  HSARG      Quito       : delay_ON=19556s, delay_OFF=21032s, Δ=+7.5%
  HSARG      Barcelona   : delay_ON=13735s, delay_OFF=15438s, Δ=+12.4%
  COOPSARG   Quito       : delay_ON=18774s, delay_OFF=20957s, Δ=+11.6%
  COOPSARG   Barcelona   : delay_ON=14166s, delay_OFF=15461s, Δ=+9.1%

==============================================================================
  CONCLUSIÓN: El MAD-Gating mejora la equidad SIN sacrificar eficiencia
  en topologías lineales (Quito). En grids (Barcelona), el efecto es
  menor pero aún positivo. Coop-SARG muestra mayor beneficio que H-SARG
  gracias al doble mecanismo de gating + equity boost.
==============================================================================