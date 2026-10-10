==============================================================================
  ESTUDIO DE ABLACIÓN MAD-GATING — RESULTADOS REALES (SUMO)
==============================================================================

Total simulaciones SUMO: 1,200
Variantes: ['coopsarg_gating_off', 'coopsarg_gating_on', 'hsarg_gating_off', 'hsarg_gating_on']
Ciudades: ['Barcelona', 'Quito']

------------------------------------------------------------------------------
EFECTO DEL MAD-GATING EN EQUIDAD (Gini)
------------------------------------------------------------------------------
Variante               Ciudad     Chaos      Gini_ON Gini_OFF        Δ        p   Sig
----------------------------------------------------------------------------------
hsarg_gating_on        Barcelona  low         0.1683   0.1915  +0.0233   0.0002   ***
hsarg_gating_on        Barcelona  mid         0.5536   0.2957  -0.2579   1.0000    ns
hsarg_gating_on        Barcelona  mid_high    0.8005   0.3342  -0.4663   1.0000    ns
hsarg_gating_on        Barcelona  high        0.8227   0.6134  -0.2092   1.0000    ns
hsarg_gating_on        Barcelona  extreme     0.8399   0.7890  -0.0509   1.0000    ns
hsarg_gating_on        Quito      low         0.0150   0.0147  -0.0003   0.4441    ns
hsarg_gating_on        Quito      mid         0.0902   0.0932  +0.0030   0.3050    ns
hsarg_gating_on        Quito      mid_high    0.1278   0.1250  -0.0028   0.7587    ns
hsarg_gating_on        Quito      high        0.1979   0.1998  +0.0020   0.3476    ns
hsarg_gating_on        Quito      extreme     0.2499   0.2669  +0.0170   0.0278     *
coopsarg_gating_on     Barcelona  low         0.1902   0.1892  -0.0010   0.5964    ns
coopsarg_gating_on     Barcelona  mid         0.2936   0.2919  -0.0018   0.6686    ns
coopsarg_gating_on     Barcelona  mid_high    0.3370   0.3369  -0.0002   0.4209    ns
coopsarg_gating_on     Barcelona  high        0.6191   0.6236  +0.0045   0.1170    ns
coopsarg_gating_on     Barcelona  extreme     0.7886   0.7843  -0.0043   0.6134    ns
coopsarg_gating_on     Quito      low         0.0142   0.0154  +0.0012   0.1889    ns
coopsarg_gating_on     Quito      mid         0.0911   0.0954  +0.0043   0.2553    ns
coopsarg_gating_on     Quito      mid_high    0.1283   0.1241  -0.0042   0.7351    ns
coopsarg_gating_on     Quito      high        0.1961   0.1998  +0.0037   0.2145    ns
coopsarg_gating_on     Quito      extreme     0.2661   0.2711  +0.0050   0.2649    ns

------------------------------------------------------------------------------
TEST AGREGADO (Quito)
------------------------------------------------------------------------------
  Gini(gating=ON)  = 0.1377 ± 0.0862
  Gini(gating=OFF) = 0.1405 ± 0.0891
  Δ = +0.0029
  Mann-Whitney U = 44125.5, p = 0.340291, r = 0.019
  [WARN] No significativo

==============================================================================