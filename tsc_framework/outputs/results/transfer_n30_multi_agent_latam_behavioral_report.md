# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-26
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Barcelona | ppo_coop_ideal | low | 30 | 115.2 | 42.0 | [99.2, 130.5] | 0.1755 | 0.0131 | 385.4 | 0.0% |
| Barcelona | ppo_coop_ideal | mid | 30 | 607.2 | 133.9 | [569.5, 659.0] | 0.2699 | 0.0161 | 1411.1 | 0.0% |
| Barcelona | ppo_coop_ideal | mid_high | 30 | 985.9 | 196.5 | [954.1, 1075.2] | 0.3078 | 0.0216 | 2335.4 | 0.0% |
| Barcelona | ppo_coop_ideal | high | 30 | 2023.7 | 215.9 | [1916.7, 2072.3] | 0.3974 | 0.0143 | 4302.8 | 0.0% |
| Barcelona | ppo_coop_ideal | extreme | 30 | 3354.4 | 280.3 | [3252.4, 3442.7] | 0.4238 | 0.0169 | 6560.7 | 0.0% |
| Barcelona | ppo_coop_chaos | low | 30 | 112.0 | 24.8 | [105.8, 116.8] | 0.1743 | 0.0110 | 364.0 | 0.0% |
| Barcelona | ppo_coop_chaos | mid | 30 | 663.1 | 136.7 | [593.3, 708.3] | 0.2687 | 0.0198 | 1626.7 | 0.0% |
| Barcelona | ppo_coop_chaos | mid_high | 30 | 1015.0 | 154.0 | [948.3, 1054.0] | 0.3068 | 0.0128 | 2422.3 | 0.0% |
| Barcelona | ppo_coop_chaos | high | 30 | 2038.5 | 195.6 | [1955.1, 2091.5] | 0.4010 | 0.0161 | 4458.4 | 0.0% |
| Barcelona | ppo_coop_chaos | extreme | 30 | 3401.5 | 267.3 | [3310.1, 3475.9] | 0.4313 | 0.0120 | 6712.5 | 0.0% |
| Barcelona | ppo_chaos | low | 30 | 164.1 | 37.3 | [151.9, 179.3] | 0.2335 | 0.0165 | 415.2 | 0.0% |
| Barcelona | ppo_chaos | mid | 30 | 635.7 | 139.5 | [595.9, 696.6] | 0.3322 | 0.0207 | 1386.3 | 0.0% |
| Barcelona | ppo_chaos | mid_high | 30 | 1145.3 | 237.2 | [1051.7, 1218.3] | 0.3699 | 0.0155 | 2565.2 | 0.0% |
| Barcelona | ppo_chaos | high | 30 | 2350.3 | 290.7 | [2284.2, 2427.0] | 0.4137 | 0.0167 | 5129.8 | 0.0% |
| Barcelona | ppo_chaos | extreme | 30 | 3486.4 | 273.3 | [3401.5, 3593.0] | 0.4288 | 0.0188 | 6458.5 | 0.0% |
| Barcelona | fixed_time_opt | low | 30 | 83.1 | 28.3 | [72.8, 94.1] | 0.1325 | 0.0162 | 336.2 | 0.0% |
| Barcelona | fixed_time_opt | mid | 30 | 601.8 | 130.4 | [565.9, 664.2] | 0.2617 | 0.0131 | 1444.5 | 0.0% |
| Barcelona | fixed_time_opt | mid_high | 30 | 1097.4 | 231.2 | [1031.5, 1208.8] | 0.3184 | 0.0333 | 2789.8 | 0.0% |
| Barcelona | fixed_time_opt | high | 30 | 2311.4 | 282.4 | [2121.4, 2354.6] | 0.3919 | 0.0131 | 5106.3 | 0.0% |
| Barcelona | fixed_time_opt | extreme | 30 | 3564.8 | 301.3 | [3447.2, 3684.1] | 0.4110 | 0.0146 | 7021.2 | 0.0% |
| Barcelona | random | low | 30 | 77.2 | 32.7 | [68.8, 91.6] | 0.1165 | 0.0137 | 339.8 | 0.0% |
| Barcelona | random | mid | 30 | 664.3 | 181.6 | [605.8, 714.8] | 0.2654 | 0.0212 | 1661.0 | 0.0% |
| Barcelona | random | mid_high | 30 | 1129.0 | 233.6 | [1052.2, 1233.4] | 0.3051 | 0.0217 | 2795.5 | 0.0% |
| Barcelona | random | high | 30 | 2174.4 | 318.7 | [2048.2, 2294.3] | 0.3874 | 0.0127 | 4737.7 | 0.0% |
| Barcelona | random | extreme | 30 | 3411.7 | 262.9 | [3326.8, 3501.1] | 0.4135 | 0.0138 | 6566.1 | 0.0% |
| Quito | ppo_coop_ideal | low | 30 | 359.3 | 92.0 | [321.4, 398.8] | 0.1887 | 0.0314 | 1029.4 | 0.0% |
| Quito | ppo_coop_ideal | mid | 30 | 1314.4 | 519.3 | [1150.5, 1519.4] | 0.3329 | 0.0441 | 3706.7 | 0.0% |
| Quito | ppo_coop_ideal | mid_high | 30 | 2222.5 | 495.3 | [2059.8, 2380.4] | 0.3915 | 0.0220 | 5869.5 | 0.0% |
| Quito | ppo_coop_ideal | high | 30 | 3587.9 | 773.1 | [3373.9, 3875.3] | 0.4539 | 0.0340 | 9065.4 | 0.0% |
| Quito | ppo_coop_ideal | extreme | 30 | 4487.2 | 970.7 | [4385.3, 5095.8] | 0.5685 | 0.0221 | 9675.3 | 40.0% |
| Quito | ppo_coop_chaos | low | 30 | 456.5 | 150.0 | [408.7, 517.6] | 0.2381 | 0.0310 | 1243.8 | 0.0% |
| Quito | ppo_coop_chaos | mid | 30 | 1745.9 | 630.4 | [1583.7, 1833.8] | 0.3764 | 0.0271 | 4551.9 | 0.0% |
| Quito | ppo_coop_chaos | mid_high | 30 | 2404.6 | 424.0 | [2323.1, 2535.1] | 0.4369 | 0.0249 | 6293.5 | 0.0% |
| Quito | ppo_coop_chaos | high | 30 | 3959.7 | 560.0 | [3619.2, 4052.8] | 0.5125 | 0.0257 | 9436.8 | 6.7% |
| Quito | ppo_coop_chaos | extreme | 30 | 4674.9 | 913.2 | [4563.3, 5011.9] | 0.5777 | 0.0275 | 10359.3 | 33.3% |
| Quito | ppo_chaos | low | 30 | 450.3 | 228.4 | [367.8, 520.2] | 0.2217 | 0.0374 | 1328.7 | 0.0% |
| Quito | ppo_chaos | mid | 30 | 1722.0 | 490.0 | [1557.0, 1912.9] | 0.4079 | 0.0310 | 4507.3 | 0.0% |
| Quito | ppo_chaos | mid_high | 30 | 2557.9 | 561.1 | [2407.4, 2818.4] | 0.4638 | 0.0260 | 6536.2 | 0.0% |
| Quito | ppo_chaos | high | 30 | 4107.2 | 660.1 | [3911.8, 4349.2] | 0.5303 | 0.0257 | 10038.3 | 10.0% |
| Quito | ppo_chaos | extreme | 30 | 4943.0 | 779.1 | [4719.3, 5232.3] | 0.5896 | 0.0316 | 10569.3 | 43.3% |
| Quito | fixed_time_opt | low | 30 | 312.1 | 192.8 | [254.6, 390.4] | 0.1285 | 0.0386 | 1335.5 | 0.0% |
| Quito | fixed_time_opt | mid | 30 | 1490.1 | 451.8 | [1396.3, 1628.7] | 0.3019 | 0.0357 | 4097.2 | 0.0% |
| Quito | fixed_time_opt | mid_high | 30 | 2452.9 | 410.8 | [2344.9, 2680.5] | 0.3631 | 0.0361 | 6978.0 | 0.0% |
| Quito | fixed_time_opt | high | 30 | 3588.7 | 797.5 | [3333.9, 3901.4] | 0.4316 | 0.0269 | 9537.2 | 3.3% |
| Quito | fixed_time_opt | extreme | 30 | 4454.1 | 1153.2 | [4133.8, 5034.1] | 0.5157 | 0.0157 | 9880.4 | 33.3% |
| Quito | random | low | 30 | 332.9 | 177.5 | [255.6, 384.0] | 0.1307 | 0.0470 | 1275.7 | 0.0% |
| Quito | random | mid | 30 | 1413.4 | 445.6 | [1255.4, 1604.7] | 0.2922 | 0.0390 | 4035.5 | 0.0% |
| Quito | random | mid_high | 30 | 2402.7 | 704.7 | [2086.4, 2533.5] | 0.3533 | 0.0346 | 6302.8 | 0.0% |
| Quito | random | high | 30 | 3516.0 | 598.6 | [3315.4, 3699.4] | 0.4307 | 0.0365 | 8956.5 | 6.7% |
| Quito | random | extreme | 30 | 4368.1 | 976.3 | [4191.6, 4827.9] | 0.5276 | 0.0267 | 9297.9 | 23.3% |
| Bogota | ppo_coop_ideal | low | 30 | 42.7 | 4.9 | [42.4, 44.3] | 0.2306 | 0.0070 | 112.9 | 0.0% |
| Bogota | ppo_coop_ideal | mid | 30 | 639.5 | 716.0 | [427.2, 748.2] | 0.3530 | 0.0085 | 3576.6 | 0.0% |
| Bogota | ppo_coop_ideal | mid_high | 30 | 7560.6 | 8292.1 | [5793.9, 11128.1] | 0.4526 | 0.0226 | 26082.0 | 70.0% |
| Bogota | ppo_coop_ideal | high | 30 | 63298.1 | 12099.3 | [57378.5, 64117.0] | 0.5825 | 0.0161 | 150435.6 | 100.0% |
| Bogota | ppo_coop_ideal | extreme | 30 | 118690.3 | 26126.6 | [113326.8, 129628.5] | 0.5704 | 0.0161 | 257344.8 | 100.0% |
| Bogota | ppo_coop_chaos | low | 30 | 38.4 | 2.9 | [37.9, 39.7] | 0.2266 | 0.0053 | 95.9 | 0.0% |
| Bogota | ppo_coop_chaos | mid | 30 | 700.1 | 418.9 | [613.0, 817.2] | 0.3518 | 0.0121 | 4438.4 | 0.0% |
| Bogota | ppo_coop_chaos | mid_high | 30 | 7686.4 | 6891.3 | [6260.7, 11253.0] | 0.4520 | 0.0204 | 28693.6 | 86.7% |
| Bogota | ppo_coop_chaos | high | 30 | 63657.1 | 13302.4 | [58364.8, 67990.7] | 0.5733 | 0.0205 | 143175.4 | 100.0% |
| Bogota | ppo_coop_chaos | extreme | 30 | 123885.1 | 16119.0 | [117392.9, 129765.1] | 0.5626 | 0.0105 | 263217.2 | 100.0% |
| Bogota | ppo_chaos | low | 30 | 38.9 | 3.8 | [38.4, 41.0] | 0.2275 | 0.0061 | 98.0 | 0.0% |
| Bogota | ppo_chaos | mid | 30 | 657.9 | 742.7 | [581.9, 861.1] | 0.3508 | 0.0089 | 3518.5 | 0.0% |
| Bogota | ppo_chaos | mid_high | 30 | 9384.4 | 11565.8 | [6329.0, 14896.6] | 0.4443 | 0.0218 | 37753.0 | 86.7% |
| Bogota | ppo_chaos | high | 30 | 61906.9 | 13660.7 | [57169.3, 68301.5] | 0.5802 | 0.0161 | 163230.4 | 100.0% |
| Bogota | ppo_chaos | extreme | 30 | 127236.4 | 18464.9 | [121353.5, 132002.4] | 0.5725 | 0.0131 | 274800.8 | 100.0% |
| Bogota | fixed_time_opt | low | 30 | 65.8 | 6.0 | [64.3, 67.8] | 0.2566 | 0.0049 | 158.4 | 0.0% |
| Bogota | fixed_time_opt | mid | 30 | 711.0 | 429.7 | [522.6, 929.6] | 0.3697 | 0.0113 | 4807.2 | 0.0% |
| Bogota | fixed_time_opt | mid_high | 30 | 6800.0 | 4834.6 | [4738.4, 7999.2] | 0.4577 | 0.0166 | 25592.5 | 63.3% |
| Bogota | fixed_time_opt | high | 30 | 56235.0 | 11274.4 | [54753.2, 61042.9] | 0.5754 | 0.0143 | 144623.1 | 100.0% |
| Bogota | fixed_time_opt | extreme | 30 | 118536.7 | 19848.1 | [109225.4, 125497.9] | 0.5745 | 0.0120 | 250156.6 | 100.0% |
| Bogota | random | low | 30 | 106.1 | 16.7 | [102.6, 114.6] | 0.2834 | 0.0123 | 321.7 | 0.0% |
| Bogota | random | mid | 30 | 637.4 | 316.1 | [542.7, 732.5] | 0.3863 | 0.0111 | 4158.0 | 0.0% |
| Bogota | random | mid_high | 30 | 3712.1 | 4705.7 | [2696.9, 5763.9] | 0.4769 | 0.0146 | 14426.0 | 36.7% |
| Bogota | random | high | 30 | 64062.3 | 16419.9 | [58427.8, 69015.3] | 0.5822 | 0.0161 | 158333.0 | 100.0% |
| Bogota | random | extreme | 30 | 125822.5 | 17645.2 | [117645.2, 130250.2] | 0.5864 | 0.0122 | 266785.2 | 100.0% |
| Berlin | ppo_coop_ideal | low | 30 | 28.5 | 5.3 | [27.3, 30.9] | 0.3314 | 0.0067 | 106.5 | 0.0% |
| Berlin | ppo_coop_ideal | mid | 30 | 413.9 | 137.9 | [358.8, 476.2] | 0.5397 | 0.0060 | 1499.6 | 0.0% |
| Berlin | ppo_coop_ideal | mid_high | 30 | 2730.3 | 1017.3 | [2404.9, 3213.5] | 0.5258 | 0.0336 | 7575.3 | 13.3% |
| Berlin | ppo_coop_ideal | high | 30 | 11955.2 | 3493.8 | [11183.6, 12707.0] | 0.5063 | 0.0208 | 25346.3 | 100.0% |
| Berlin | ppo_coop_ideal | extreme | 30 | 23329.3 | 3933.9 | [22662.5, 24923.6] | 0.5028 | 0.0170 | 44120.2 | 100.0% |
| Berlin | ppo_coop_chaos | low | 30 | 26.9 | 3.3 | [25.8, 27.5] | 0.3318 | 0.0079 | 86.3 | 0.0% |
| Berlin | ppo_coop_chaos | mid | 30 | 182.7 | 58.6 | [171.3, 201.8] | 0.5380 | 0.0073 | 562.9 | 0.0% |
| Berlin | ppo_coop_chaos | mid_high | 30 | 2995.1 | 2077.5 | [2665.6, 4122.9] | 0.5100 | 0.0233 | 9532.7 | 20.0% |
| Berlin | ppo_coop_chaos | high | 30 | 11544.0 | 3613.9 | [11148.8, 13639.3] | 0.5257 | 0.0165 | 23871.0 | 100.0% |
| Berlin | ppo_coop_chaos | extreme | 30 | 21172.8 | 3093.4 | [20184.3, 22013.9] | 0.5458 | 0.0177 | 38750.7 | 100.0% |
| Berlin | ppo_chaos | low | 30 | 1223.3 | 460.6 | [1026.2, 1281.3] | 0.4517 | 0.0137 | 5813.0 | 0.0% |
| Berlin | ppo_chaos | mid | 30 | 5873.5 | 640.5 | [5667.9, 6145.9] | 0.4852 | 0.0100 | 13826.0 | 100.0% |
| Berlin | ppo_chaos | mid_high | 30 | 8999.4 | 1609.1 | [8591.1, 9997.6] | 0.4717 | 0.0114 | 19456.9 | 100.0% |
| Berlin | ppo_chaos | high | 30 | 20526.5 | 3192.6 | [19831.8, 22019.2] | 0.4381 | 0.0120 | 40007.0 | 100.0% |
| Berlin | ppo_chaos | extreme | 30 | 31003.0 | 2388.4 | [29772.7, 31660.3] | 0.4154 | 0.0101 | 50808.3 | 100.0% |
| Berlin | fixed_time_opt | low | 30 | 78.4 | 22.0 | [75.3, 90.3] | 0.3566 | 0.0118 | 347.3 | 0.0% |
| Berlin | fixed_time_opt | mid | 30 | 381.9 | 83.5 | [367.8, 430.5] | 0.5461 | 0.0135 | 1416.3 | 0.0% |
| Berlin | fixed_time_opt | mid_high | 30 | 2278.8 | 2082.1 | [2007.1, 3505.9] | 0.5148 | 0.0299 | 8636.3 | 13.3% |
| Berlin | fixed_time_opt | high | 30 | 12200.7 | 2508.7 | [11124.1, 12695.9] | 0.4987 | 0.0362 | 23842.0 | 100.0% |
| Berlin | fixed_time_opt | extreme | 30 | 20151.5 | 2868.7 | [19779.2, 21668.0] | 0.5144 | 0.0193 | 39101.0 | 100.0% |
| Berlin | random | low | 30 | 159.7 | 95.1 | [141.7, 181.6] | 0.4002 | 0.0116 | 665.5 | 0.0% |
| Berlin | random | mid | 30 | 318.9 | 65.6 | [289.9, 335.1] | 0.5423 | 0.0119 | 1092.9 | 0.0% |
| Berlin | random | mid_high | 30 | 1598.9 | 1373.0 | [1267.0, 2281.2] | 0.5464 | 0.0440 | 7943.6 | 6.7% |
| Berlin | random | high | 30 | 10330.7 | 4158.4 | [8495.9, 11889.3] | 0.5475 | 0.0206 | 24432.8 | 100.0% |
| Berlin | random | extreme | 30 | 20938.4 | 3764.9 | [18882.3, 21865.1] | 0.5543 | 0.0166 | 42672.3 | 100.0% |
| Madrid | ppo_coop_ideal | low | 30 | 4.5 | 0.2 | [4.4, 4.6] | 0.0516 | 0.0022 | 19.6 | 0.0% |
| Madrid | ppo_coop_ideal | mid | 30 | 2642.0 | 290.5 | [2545.6, 2743.8] | 0.1309 | 0.0086 | 6025.1 | 0.0% |
| Madrid | ppo_coop_ideal | mid_high | 30 | 3978.0 | 307.6 | [3871.4, 4035.1] | 0.1435 | 0.0075 | 8265.9 | 0.0% |
| Madrid | ppo_coop_ideal | high | 30 | 8123.3 | 689.5 | [7909.6, 8455.7] | 0.1617 | 0.0214 | 16843.5 | 100.0% |
| Madrid | ppo_coop_ideal | extreme | 30 | 10149.1 | 810.4 | [9924.6, 10374.3] | 0.1742 | 0.0178 | 17884.5 | 100.0% |
| Madrid | ppo_coop_chaos | low | 30 | 4.0 | 0.4 | [3.9, 4.1] | 0.0477 | 0.0035 | 17.8 | 0.0% |
| Madrid | ppo_coop_chaos | mid | 30 | 2664.7 | 200.5 | [2582.1, 2715.8] | 0.1342 | 0.0078 | 6092.1 | 0.0% |
| Madrid | ppo_coop_chaos | mid_high | 30 | 3883.2 | 486.7 | [3779.1, 4067.1] | 0.1535 | 0.0106 | 8319.2 | 0.0% |
| Madrid | ppo_coop_chaos | high | 30 | 8346.8 | 506.5 | [8117.6, 8422.5] | 0.1678 | 0.0184 | 16450.4 | 100.0% |
| Madrid | ppo_coop_chaos | extreme | 30 | 10190.7 | 374.8 | [10081.7, 10345.9] | 0.1784 | 0.0215 | 17771.3 | 100.0% |
| Madrid | ppo_chaos | low | 30 | 1448.6 | 146.9 | [1430.5, 1508.6] | 0.1027 | 0.0106 | 3938.7 | 0.0% |
| Madrid | ppo_chaos | mid | 30 | 2806.8 | 205.7 | [2744.9, 2906.5] | 0.1267 | 0.0159 | 6340.8 | 0.0% |
| Madrid | ppo_chaos | mid_high | 30 | 3938.0 | 436.6 | [3805.0, 4105.5] | 0.1270 | 0.0103 | 8547.4 | 0.0% |
| Madrid | ppo_chaos | high | 30 | 7807.1 | 484.8 | [7663.0, 7953.3] | 0.1538 | 0.0173 | 16143.8 | 100.0% |
| Madrid | ppo_chaos | extreme | 30 | 10105.1 | 642.5 | [9973.8, 10380.1] | 0.1734 | 0.0287 | 17618.0 | 100.0% |
| Madrid | fixed_time_opt | low | 30 | 6.1 | 0.4 | [5.9, 6.2] | 0.0577 | 0.0045 | 27.7 | 0.0% |
| Madrid | fixed_time_opt | mid | 30 | 2819.4 | 325.7 | [2714.6, 2925.0] | 0.1388 | 0.0079 | 6634.1 | 0.0% |
| Madrid | fixed_time_opt | mid_high | 30 | 4172.0 | 374.8 | [3976.6, 4248.5] | 0.1546 | 0.0103 | 8860.1 | 3.3% |
| Madrid | fixed_time_opt | high | 30 | 8177.3 | 794.2 | [7864.9, 8387.6] | 0.1712 | 0.0178 | 16670.3 | 100.0% |
| Madrid | fixed_time_opt | extreme | 30 | 10149.8 | 873.2 | [10045.4, 10504.1] | 0.1917 | 0.0206 | 17754.0 | 100.0% |
| Madrid | random | low | 30 | 6.2 | 0.8 | [6.0, 6.7] | 0.0546 | 0.0061 | 28.0 | 0.0% |
| Madrid | random | mid | 30 | 2708.5 | 260.7 | [2635.8, 2803.6] | 0.1365 | 0.0090 | 6312.9 | 0.0% |
| Madrid | random | mid_high | 30 | 4008.7 | 322.9 | [3934.5, 4130.1] | 0.1454 | 0.0096 | 9154.7 | 0.0% |
| Madrid | random | high | 30 | 8269.7 | 706.9 | [7961.2, 8465.8] | 0.1604 | 0.0148 | 16959.8 | 100.0% |
| Madrid | random | extreme | 30 | 10409.2 | 640.8 | [10203.1, 10539.1] | 0.1796 | 0.0198 | 18291.0 | 100.0% |
| CDMX | ppo_coop_ideal | low | 30 | 3.2 | 0.3 | [3.1, 3.3] | 0.0553 | 0.0035 | 15.8 | 0.0% |
| CDMX | ppo_coop_ideal | mid | 30 | 8.8 | 1.4 | [8.2, 9.1] | 0.1093 | 0.0059 | 35.4 | 0.0% |
| CDMX | ppo_coop_ideal | mid_high | 30 | 57.9 | 31.6 | [47.2, 65.3] | 0.1696 | 0.0066 | 357.8 | 0.0% |
| CDMX | ppo_coop_ideal | high | 30 | 8112.7 | 4139.2 | [7201.7, 9235.7] | 0.3091 | 0.0107 | 23223.8 | 100.0% |
| CDMX | ppo_coop_ideal | extreme | 30 | 47486.5 | 17700.3 | [42281.7, 53133.8] | 0.4502 | 0.0298 | 111911.5 | 100.0% |
| CDMX | ppo_coop_chaos | low | 30 | 3.3 | 0.7 | [3.1, 3.6] | 0.0560 | 0.0051 | 16.9 | 0.0% |
| CDMX | ppo_coop_chaos | mid | 30 | 9.1 | 1.5 | [8.5, 9.6] | 0.1097 | 0.0044 | 36.3 | 0.0% |
| CDMX | ppo_coop_chaos | mid_high | 30 | 48.9 | 31.6 | [41.3, 65.4] | 0.1672 | 0.0061 | 299.7 | 0.0% |
| CDMX | ppo_coop_chaos | high | 30 | 7893.7 | 3693.2 | [7133.4, 9753.0] | 0.3062 | 0.0098 | 21746.9 | 93.3% |
| CDMX | ppo_coop_chaos | extreme | 30 | 54266.0 | 15908.0 | [48823.9, 59024.5] | 0.4420 | 0.0202 | 110939.8 | 100.0% |
| CDMX | ppo_chaos | low | 30 | 2.5 | 0.4 | [2.4, 2.7] | 0.0474 | 0.0026 | 13.1 | 0.0% |
| CDMX | ppo_chaos | mid | 30 | 7.6 | 0.9 | [7.0, 7.8] | 0.0955 | 0.0042 | 31.4 | 0.0% |
| CDMX | ppo_chaos | mid_high | 30 | 39.3 | 30.7 | [32.5, 48.9] | 0.1529 | 0.0057 | 223.2 | 0.0% |
| CDMX | ppo_chaos | high | 30 | 8034.4 | 3641.3 | [6297.5, 9705.9] | 0.2856 | 0.0091 | 21710.3 | 93.3% |
| CDMX | ppo_chaos | extreme | 30 | 61398.4 | 22887.2 | [53568.9, 68338.1] | 0.4339 | 0.0252 | 137958.4 | 100.0% |
| CDMX | fixed_time_opt | low | 30 | 4.6 | 0.4 | [4.5, 4.8] | 0.0591 | 0.0030 | 23.6 | 0.0% |
| CDMX | fixed_time_opt | mid | 30 | 12.1 | 1.6 | [11.5, 12.5] | 0.1152 | 0.0045 | 48.5 | 0.0% |
| CDMX | fixed_time_opt | mid_high | 30 | 67.3 | 55.1 | [55.1, 94.4] | 0.1739 | 0.0053 | 408.9 | 0.0% |
| CDMX | fixed_time_opt | high | 30 | 9814.0 | 2984.2 | [8147.6, 10393.6] | 0.3190 | 0.0080 | 27023.7 | 93.3% |
| CDMX | fixed_time_opt | extreme | 30 | 57955.4 | 22021.7 | [49566.0, 61174.6] | 0.4440 | 0.0303 | 120406.6 | 100.0% |
| CDMX | random | low | 30 | 11.7 | 2.0 | [10.9, 12.1] | 0.0790 | 0.0038 | 61.0 | 0.0% |
| CDMX | random | mid | 30 | 28.5 | 5.2 | [26.5, 29.7] | 0.1465 | 0.0069 | 117.7 | 0.0% |
| CDMX | random | mid_high | 30 | 80.8 | 46.1 | [71.1, 108.7] | 0.2163 | 0.0107 | 320.8 | 0.0% |
| CDMX | random | high | 30 | 7903.7 | 3231.8 | [6394.8, 9104.9] | 0.3546 | 0.0070 | 23003.1 | 93.3% |
| CDMX | random | extreme | 30 | 52412.8 | 20871.5 | [42328.1, 58763.1] | 0.4618 | 0.0230 | 115767.5 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Barcelona | ppo_coop_ideal | low | 4.63 | 2.028 |
| Barcelona | ppo_coop_ideal | mid | 12.20 | 5.345 |
| Barcelona | ppo_coop_ideal | mid_high | 16.04 | 7.028 |
| Barcelona | ppo_coop_ideal | high | 24.20 | 10.602 |
| Barcelona | ppo_coop_ideal | extreme | 34.32 | 15.035 |
| Barcelona | ppo_coop_chaos | low | 4.52 | 1.982 |
| Barcelona | ppo_coop_chaos | mid | 12.42 | 5.440 |
| Barcelona | ppo_coop_chaos | mid_high | 15.90 | 6.968 |
| Barcelona | ppo_coop_chaos | high | 24.08 | 10.548 |
| Barcelona | ppo_coop_chaos | extreme | 33.69 | 14.761 |
| Barcelona | ppo_chaos | low | 5.86 | 2.566 |
| Barcelona | ppo_chaos | mid | 12.86 | 5.635 |
| Barcelona | ppo_chaos | mid_high | 17.37 | 7.610 |
| Barcelona | ppo_chaos | high | 28.34 | 12.418 |
| Barcelona | ppo_chaos | extreme | 36.84 | 16.138 |
| Barcelona | fixed_time_opt | low | 2.91 | 1.276 |
| Barcelona | fixed_time_opt | mid | 10.49 | 4.596 |
| Barcelona | fixed_time_opt | mid_high | 15.42 | 6.754 |
| Barcelona | fixed_time_opt | high | 24.89 | 10.903 |
| Barcelona | fixed_time_opt | extreme | 34.30 | 15.025 |
| Barcelona | random | low | 2.55 | 1.119 |
| Barcelona | random | mid | 10.73 | 4.701 |
| Barcelona | random | mid_high | 14.87 | 6.513 |
| Barcelona | random | high | 23.70 | 10.381 |
| Barcelona | random | extreme | 33.57 | 14.707 |
| Quito | ppo_coop_ideal | low | 4.56 | 1.996 |
| Quito | ppo_coop_ideal | mid | 13.60 | 5.957 |
| Quito | ppo_coop_ideal | mid_high | 22.01 | 9.642 |
| Quito | ppo_coop_ideal | high | 34.38 | 15.063 |
| Quito | ppo_coop_ideal | extreme | 43.26 | 18.954 |
| Quito | ppo_coop_chaos | low | 5.41 | 2.369 |
| Quito | ppo_coop_chaos | mid | 16.92 | 7.412 |
| Quito | ppo_coop_chaos | mid_high | 23.66 | 10.364 |
| Quito | ppo_coop_chaos | high | 36.60 | 16.034 |
| Quito | ppo_coop_chaos | extreme | 45.71 | 20.024 |
| Quito | ppo_chaos | low | 5.41 | 2.368 |
| Quito | ppo_chaos | mid | 17.28 | 7.569 |
| Quito | ppo_chaos | mid_high | 25.87 | 11.333 |
| Quito | ppo_chaos | high | 39.57 | 17.336 |
| Quito | ppo_chaos | extreme | 47.35 | 20.743 |
| Quito | fixed_time_opt | low | 4.02 | 1.762 |
| Quito | fixed_time_opt | mid | 15.17 | 6.644 |
| Quito | fixed_time_opt | mid_high | 23.60 | 10.339 |
| Quito | fixed_time_opt | high | 34.57 | 15.146 |
| Quito | fixed_time_opt | extreme | 42.79 | 18.747 |
| Quito | random | low | 4.05 | 1.774 |
| Quito | random | mid | 14.13 | 6.191 |
| Quito | random | mid_high | 22.14 | 9.698 |
| Quito | random | high | 32.62 | 14.292 |
| Quito | random | extreme | 40.17 | 17.597 |
| Bogota | ppo_coop_ideal | low | 23.85 | 10.448 |
| Bogota | ppo_coop_ideal | mid | 66.58 | 29.167 |
| Bogota | ppo_coop_ideal | mid_high | 150.09 | 65.752 |
| Bogota | ppo_coop_ideal | high | 321.00 | 140.630 |
| Bogota | ppo_coop_ideal | extreme | 417.80 | 183.038 |
| Bogota | ppo_coop_chaos | low | 23.69 | 10.377 |
| Bogota | ppo_coop_chaos | mid | 65.63 | 28.753 |
| Bogota | ppo_coop_chaos | mid_high | 156.20 | 68.433 |
| Bogota | ppo_coop_chaos | high | 316.83 | 138.801 |
| Bogota | ppo_coop_chaos | extreme | 425.81 | 186.548 |
| Bogota | ppo_chaos | low | 23.96 | 10.495 |
| Bogota | ppo_chaos | mid | 67.04 | 29.370 |
| Bogota | ppo_chaos | mid_high | 156.70 | 68.650 |
| Bogota | ppo_chaos | high | 318.03 | 139.327 |
| Bogota | ppo_chaos | extreme | 420.78 | 184.346 |
| Bogota | fixed_time_opt | low | 25.01 | 10.955 |
| Bogota | fixed_time_opt | mid | 65.09 | 28.514 |
| Bogota | fixed_time_opt | mid_high | 141.74 | 62.094 |
| Bogota | fixed_time_opt | high | 318.72 | 139.631 |
| Bogota | fixed_time_opt | extreme | 419.43 | 183.752 |
| Bogota | random | low | 26.06 | 11.417 |
| Bogota | random | mid | 66.60 | 29.175 |
| Bogota | random | mid_high | 137.38 | 60.185 |
| Bogota | random | high | 323.64 | 141.788 |
| Bogota | random | extreme | 417.84 | 183.058 |
| Berlin | ppo_coop_ideal | low | 14.29 | 6.261 |
| Berlin | ppo_coop_ideal | mid | 44.52 | 19.504 |
| Berlin | ppo_coop_ideal | mid_high | 91.30 | 39.997 |
| Berlin | ppo_coop_ideal | high | 203.43 | 89.124 |
| Berlin | ppo_coop_ideal | extreme | 309.49 | 135.589 |
| Berlin | ppo_coop_chaos | low | 14.15 | 6.197 |
| Berlin | ppo_coop_chaos | mid | 37.72 | 16.527 |
| Berlin | ppo_coop_chaos | mid_high | 97.00 | 42.494 |
| Berlin | ppo_coop_chaos | high | 207.28 | 90.808 |
| Berlin | ppo_coop_chaos | extreme | 303.41 | 132.924 |
| Berlin | ppo_chaos | low | 42.85 | 18.771 |
| Berlin | ppo_chaos | mid | 103.29 | 45.252 |
| Berlin | ppo_chaos | mid_high | 136.09 | 59.623 |
| Berlin | ppo_chaos | high | 240.59 | 105.401 |
| Berlin | ppo_chaos | extreme | 315.76 | 138.334 |
| Berlin | fixed_time_opt | low | 15.62 | 6.844 |
| Berlin | fixed_time_opt | mid | 41.96 | 18.380 |
| Berlin | fixed_time_opt | mid_high | 89.24 | 39.096 |
| Berlin | fixed_time_opt | high | 189.88 | 83.187 |
| Berlin | fixed_time_opt | extreme | 299.36 | 131.151 |
| Berlin | random | low | 19.74 | 8.650 |
| Berlin | random | mid | 41.72 | 18.278 |
| Berlin | random | mid_high | 88.63 | 38.827 |
| Berlin | random | high | 192.53 | 84.345 |
| Berlin | random | extreme | 300.92 | 131.833 |
| Madrid | ppo_coop_ideal | low | 5.97 | 2.616 |
| Madrid | ppo_coop_ideal | mid | 28.68 | 12.563 |
| Madrid | ppo_coop_ideal | mid_high | 41.81 | 18.316 |
| Madrid | ppo_coop_ideal | high | 72.68 | 31.841 |
| Madrid | ppo_coop_ideal | extreme | 88.21 | 38.644 |
| Madrid | ppo_coop_chaos | low | 5.82 | 2.550 |
| Madrid | ppo_coop_chaos | mid | 28.66 | 12.554 |
| Madrid | ppo_coop_chaos | mid_high | 41.29 | 18.090 |
| Madrid | ppo_coop_chaos | high | 74.29 | 32.547 |
| Madrid | ppo_coop_chaos | extreme | 88.40 | 38.727 |
| Madrid | ppo_chaos | low | 20.97 | 9.185 |
| Madrid | ppo_chaos | mid | 38.24 | 16.754 |
| Madrid | ppo_chaos | mid_high | 46.75 | 20.482 |
| Madrid | ppo_chaos | high | 71.65 | 31.389 |
| Madrid | ppo_chaos | extreme | 88.01 | 38.558 |
| Madrid | fixed_time_opt | low | 5.94 | 2.601 |
| Madrid | fixed_time_opt | mid | 29.53 | 12.935 |
| Madrid | fixed_time_opt | mid_high | 42.51 | 18.624 |
| Madrid | fixed_time_opt | high | 73.33 | 32.127 |
| Madrid | fixed_time_opt | extreme | 88.84 | 38.919 |
| Madrid | random | low | 6.27 | 2.747 |
| Madrid | random | mid | 29.55 | 12.944 |
| Madrid | random | mid_high | 41.96 | 18.383 |
| Madrid | random | high | 72.95 | 31.958 |
| Madrid | random | extreme | 88.36 | 38.712 |
| CDMX | ppo_coop_ideal | low | 5.09 | 2.228 |
| CDMX | ppo_coop_ideal | mid | 10.44 | 4.573 |
| CDMX | ppo_coop_ideal | mid_high | 16.97 | 7.435 |
| CDMX | ppo_coop_ideal | high | 102.15 | 44.753 |
| CDMX | ppo_coop_ideal | extreme | 246.87 | 108.152 |
| CDMX | ppo_coop_chaos | low | 5.07 | 2.221 |
| CDMX | ppo_coop_chaos | mid | 10.44 | 4.572 |
| CDMX | ppo_coop_chaos | mid_high | 16.88 | 7.396 |
| CDMX | ppo_coop_chaos | high | 103.33 | 45.270 |
| CDMX | ppo_coop_chaos | extreme | 251.26 | 110.077 |
| CDMX | ppo_chaos | low | 5.02 | 2.198 |
| CDMX | ppo_chaos | mid | 10.25 | 4.492 |
| CDMX | ppo_chaos | mid_high | 16.62 | 7.280 |
| CDMX | ppo_chaos | high | 100.19 | 43.892 |
| CDMX | ppo_chaos | extreme | 247.58 | 108.466 |
| CDMX | fixed_time_opt | low | 5.17 | 2.265 |
| CDMX | fixed_time_opt | mid | 10.68 | 4.681 |
| CDMX | fixed_time_opt | mid_high | 17.30 | 7.579 |
| CDMX | fixed_time_opt | high | 109.80 | 48.102 |
| CDMX | fixed_time_opt | extreme | 253.95 | 111.255 |
| CDMX | random | low | 5.46 | 2.392 |
| CDMX | random | mid | 11.31 | 4.955 |
| CDMX | random | mid_high | 18.40 | 8.061 |
| CDMX | random | high | 109.03 | 47.765 |
| CDMX | random | extreme | 252.54 | 110.639 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|
| Barcelona | low | Delay | 440.0 | 0.8883 | ns | 0.022 | negligible |
| Barcelona | low | Gini | 394.0 | 0.4119 | ns | 0.124 | small |
| Barcelona | low | CVaR90 | 421.0 | 0.6735 | ns | 0.064 | negligible |
| Barcelona | mid | Delay | 521.0 | 0.2973 | ns | -0.158 | small |
| Barcelona | mid | Gini | 477.0 | 0.6952 | ns | -0.060 | negligible |
| Barcelona | mid | CVaR90 | 481.0 | 0.6520 | ns | -0.069 | negligible |
| Barcelona | mid_high | Delay | 436.0 | 0.8418 | ns | 0.031 | negligible |
| Barcelona | mid_high | Gini | 425.0 | 0.7172 | ns | 0.056 | negligible |
| Barcelona | mid_high | CVaR90 | 458.0 | 0.9117 | ns | -0.018 | negligible |
| Barcelona | high | Delay | 500.0 | 0.4643 | ns | -0.111 | small |
| Barcelona | high | Gini | 571.0 | 0.0748 | ns | -0.269 | small |
| Barcelona | high | CVaR90 | 514.0 | 0.3478 | ns | -0.142 | small |
| Barcelona | extreme | Delay | 524.0 | 0.2772 | ns | -0.164 | small |
| Barcelona | extreme | Gini | 586.0 | 0.0451 | * | -0.302 | medium |
| Barcelona | extreme | CVaR90 | 546.0 | 0.1580 | ns | -0.213 | small |
| Quito | low | Delay | 656.0 | 0.0024 | ** | -0.458 | medium |
| Quito | low | Gini | 850.0 | 0.0000 | *** | -0.889 | large |
| Quito | low | CVaR90 | 569.0 | 0.0798 | ns | -0.264 | small |
| Quito | mid | Delay | 679.0 | 0.0007 | *** | -0.509 | large |
| Quito | mid | Gini | 852.0 | 0.0000 | *** | -0.893 | large |
| Quito | mid | CVaR90 | 626.0 | 0.0095 | ** | -0.391 | medium |
| Quito | mid_high | Delay | 569.0 | 0.0798 | ns | -0.264 | small |
| Quito | mid_high | Gini | 859.0 | 0.0000 | *** | -0.909 | large |
| Quito | mid_high | CVaR90 | 566.0 | 0.0877 | ns | -0.258 | small |
| Quito | high | Delay | 552.0 | 0.1335 | ns | -0.227 | small |
| Quito | high | Gini | 859.0 | 0.0000 | *** | -0.909 | large |
| Quito | high | CVaR90 | 528.0 | 0.2519 | ns | -0.173 | small |
| Quito | extreme | Delay | 496.0 | 0.5011 | ns | -0.102 | small |
| Quito | extreme | Gini | 583.0 | 0.0501 | ns | -0.296 | small |
| Quito | extreme | CVaR90 | 451.0 | 0.9941 | ns | -0.002 | negligible |
| Bogota | low | Delay | 143.0 | 0.0000 | *** | 0.682 | large |
| Bogota | low | Gini | 241.0 | 0.0021 | ** | 0.464 | medium |
| Bogota | low | CVaR90 | 138.0 | 0.0000 | *** | 0.693 | large |
| Bogota | mid | Delay | 508.0 | 0.3953 | ns | -0.129 | small |
| Bogota | mid | Gini | 415.0 | 0.6100 | ns | 0.078 | negligible |
| Bogota | mid | CVaR90 | 502.0 | 0.4464 | ns | -0.116 | small |
| Bogota | mid_high | Delay | 480.0 | 0.6627 | ns | -0.067 | negligible |
| Bogota | mid_high | Gini | 424.0 | 0.7062 | ns | 0.058 | negligible |
| Bogota | mid_high | CVaR90 | 478.0 | 0.6843 | ns | -0.062 | negligible |
| Bogota | high | Delay | 527.0 | 0.2581 | ns | -0.171 | small |
| Bogota | high | Gini | 326.0 | 0.0679 | ns | 0.276 | small |
| Bogota | high | CVaR90 | 435.0 | 0.8303 | ns | 0.033 | negligible |
| Bogota | extreme | Delay | 516.0 | 0.3329 | ns | -0.147 | small |
| Bogota | extreme | Gini | 223.0 | 0.0008 | *** | 0.504 | large |
| Bogota | extreme | CVaR90 | 464.0 | 0.8418 | ns | -0.031 | negligible |
| Berlin | low | Delay | 283.0 | 0.0138 | * | 0.371 | medium |
| Berlin | low | Gini | 470.0 | 0.7731 | ns | -0.044 | negligible |
| Berlin | low | CVaR90 | 176.0 | 0.0001 | *** | 0.609 | large |
| Berlin | mid | Delay | 109.0 | 0.0000 | *** | 0.758 | large |
| Berlin | mid | Gini | 357.0 | 0.1715 | ns | 0.207 | small |
| Berlin | mid | CVaR90 | 105.0 | 0.0000 | *** | 0.767 | large |
| Berlin | mid_high | Delay | 577.0 | 0.0615 | ns | -0.282 | small |
| Berlin | mid_high | Gini | 305.0 | 0.0327 | * | 0.322 | medium |
| Berlin | mid_high | CVaR90 | 557.0 | 0.1154 | ns | -0.238 | small |
| Berlin | high | Delay | 503.0 | 0.4376 | ns | -0.118 | small |
| Berlin | high | Gini | 725.0 | 0.0000 | *** | -0.611 | large |
| Berlin | high | CVaR90 | 497.0 | 0.4918 | ns | -0.104 | small |
| Berlin | extreme | Delay | 227.0 | 0.0010 | ** | 0.496 | medium |
| Berlin | extreme | Gini | 898.0 | 0.0000 | *** | -0.996 | large |
| Berlin | extreme | CVaR90 | 257.0 | 0.0044 | ** | 0.429 | medium |
| Madrid | low | Delay | 56.5 | 0.0000 | *** | 0.874 | large |
| Madrid | low | Gini | 156.0 | 0.0000 | *** | 0.653 | large |
| Madrid | low | CVaR90 | 252.0 | 0.0035 | ** | 0.440 | medium |
| Madrid | mid | Delay | 446.0 | 0.9587 | ns | 0.009 | negligible |
| Madrid | mid | Gini | 641.0 | 0.0049 | ** | -0.424 | medium |
| Madrid | mid | CVaR90 | 460.0 | 0.8883 | ns | -0.022 | negligible |
| Madrid | mid_high | Delay | 429.0 | 0.7618 | ns | 0.047 | negligible |
| Madrid | mid_high | Gini | 738.0 | 0.0000 | *** | -0.640 | large |
| Madrid | mid_high | CVaR90 | 427.0 | 0.7394 | ns | 0.051 | negligible |
| Madrid | high | Delay | 478.0 | 0.6843 | ns | -0.062 | negligible |
| Madrid | high | Gini | 562.0 | 0.0993 | ns | -0.249 | small |
| Madrid | high | CVaR90 | 338.0 | 0.0993 | ns | 0.249 | small |
| Madrid | extreme | Delay | 482.0 | 0.6414 | ns | -0.071 | negligible |
| Madrid | extreme | Gini | 461.0 | 0.8766 | ns | -0.024 | negligible |
| Madrid | extreme | CVaR90 | 410.0 | 0.5592 | ns | 0.089 | negligible |
| CDMX | low | Delay | 528.0 | 0.2519 | ns | -0.173 | small |
| CDMX | low | Gini | 499.0 | 0.4733 | ns | -0.109 | small |
| CDMX | low | CVaR90 | 567.0 | 0.0850 | ns | -0.260 | small |
| CDMX | mid | Delay | 557.5 | 0.1137 | ns | -0.239 | small |
| CDMX | mid | Gini | 454.0 | 0.9587 | ns | -0.009 | negligible |
| CDMX | mid | CVaR90 | 524.0 | 0.2772 | ns | -0.164 | small |
| CDMX | mid_high | Delay | 412.0 | 0.5793 | ns | 0.084 | negligible |
| CDMX | mid_high | Gini | 352.0 | 0.1494 | ns | 0.218 | small |
| CDMX | mid_high | CVaR90 | 411.0 | 0.5692 | ns | 0.087 | negligible |
| CDMX | high | Delay | 421.0 | 0.6735 | ns | 0.064 | negligible |
| CDMX | high | Gini | 334.0 | 0.0877 | ns | 0.258 | small |
| CDMX | high | CVaR90 | 399.0 | 0.4553 | ns | 0.113 | small |
| CDMX | extreme | Delay | 559.0 | 0.1087 | ns | -0.242 | small |
| CDMX | extreme | Gini | 388.0 | 0.3632 | ns | 0.138 | small |
| CDMX | extreme | CVaR90 | 479.0 | 0.6735 | ns | -0.064 | negligible |

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| Barcelona | low | 88.0 | 0.0000 | *** |
| Barcelona | mid | 4.1 | 0.3871 | ns |
| Barcelona | mid_high | 19.2 | 0.0007 | *** |
| Barcelona | high | 55.5 | 0.0000 | *** |
| Barcelona | extreme | 24.9 | 0.0001 | *** |
| Quito | low | 28.5 | 0.0000 | *** |
| Quito | mid | 22.0 | 0.0002 | *** |
| Quito | mid_high | 12.6 | 0.0133 | * |
| Quito | high | 21.3 | 0.0003 | *** |
| Quito | extreme | 7.9 | 0.0934 | ns |
| Bogota | low | 57.4 | 0.0000 | *** |
| Bogota | mid | 1.4 | 0.8466 | ns |
| Bogota | mid_high | 24.0 | 0.0001 | *** |
| Bogota | high | 7.4 | 0.1160 | ns |
| Bogota | extreme | 9.4 | 0.0525 | ns |
| Berlin | low | 134.1 | 0.0000 | *** |
| Berlin | mid | 105.3 | 0.0000 | *** |
| Berlin | mid_high | 83.1 | 0.0000 | *** |
| Berlin | high | 77.2 | 0.0000 | *** |
| Berlin | extreme | 83.4 | 0.0000 | *** |
| Madrid | low | 134.7 | 0.0000 | *** |
| Madrid | mid | 21.3 | 0.0003 | *** |
| Madrid | mid_high | 6.4 | 0.1681 | ns |
| Madrid | high | 11.0 | 0.0270 | * |
| Madrid | extreme | 3.7 | 0.4499 | ns |
| CDMX | low | 126.2 | 0.0000 | *** |
| CDMX | mid | 120.2 | 0.0000 | *** |
| CDMX | mid_high | 34.4 | 0.0000 | *** |
| CDMX | high | 6.0 | 0.1967 | ns |
| CDMX | extreme | 8.4 | 0.0792 | ns |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|
| Barcelona | low | ppo_coop_ideal | ppo_coop_chaos | 0.8883 | 1.0000 | ns |
| Barcelona | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0001 | *** |
| Barcelona | low | ppo_coop_ideal | random | 0.0000 | 0.0001 | *** |
| Barcelona | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Barcelona | low | fixed_time_opt | random | 0.4918 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_ideal | ppo_coop_chaos | 0.2973 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_ideal | ppo_chaos | 0.6843 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_ideal | fixed_time_opt | 0.7062 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_ideal | random | 0.2643 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_chaos | ppo_chaos | 0.4643 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_chaos | fixed_time_opt | 0.1023 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_chaos | random | 0.8766 | 1.0000 | ns |
| Barcelona | mid | ppo_chaos | fixed_time_opt | 0.3112 | 1.0000 | ns |
| Barcelona | mid | ppo_chaos | random | 0.4376 | 1.0000 | ns |
| Barcelona | mid | fixed_time_opt | random | 0.1023 | 1.0000 | ns |
| Barcelona | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.8418 | 1.0000 | ns |
| Barcelona | mid_high | ppo_coop_ideal | ppo_chaos | 0.0044 | 0.0443 | * |
| Barcelona | mid_high | ppo_coop_ideal | fixed_time_opt | 0.0083 | 0.0831 | ns |
| Barcelona | mid_high | ppo_coop_ideal | random | 0.0108 | 0.1076 | ns |
| Barcelona | mid_high | ppo_coop_chaos | ppo_chaos | 0.0021 | 0.0205 | * |
| Barcelona | mid_high | ppo_coop_chaos | fixed_time_opt | 0.0087 | 0.0868 | ns |
| Barcelona | mid_high | ppo_coop_chaos | random | 0.0026 | 0.0262 | * |
| Barcelona | mid_high | ppo_chaos | fixed_time_opt | 0.6414 | 1.0000 | ns |
| Barcelona | mid_high | ppo_chaos | random | 0.8418 | 1.0000 | ns |
| Barcelona | mid_high | fixed_time_opt | random | 0.7062 | 1.0000 | ns |
| Barcelona | high | ppo_coop_ideal | ppo_coop_chaos | 0.4643 | 1.0000 | ns |
| Barcelona | high | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | high | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0001 | *** |
| Barcelona | high | ppo_coop_ideal | random | 0.0053 | 0.0532 | ns |
| Barcelona | high | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | high | ppo_coop_chaos | fixed_time_opt | 0.0001 | 0.0007 | *** |
| Barcelona | high | ppo_coop_chaos | random | 0.0339 | 0.3387 | ns |
| Barcelona | high | ppo_chaos | fixed_time_opt | 0.0501 | 0.5012 | ns |
| Barcelona | high | ppo_chaos | random | 0.0002 | 0.0024 | ** |
| Barcelona | high | fixed_time_opt | random | 0.0679 | 0.6787 | ns |
| Barcelona | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.2772 | 1.0000 | ns |
| Barcelona | extreme | ppo_coop_ideal | ppo_chaos | 0.0008 | 0.0081 | ** |
| Barcelona | extreme | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0003 | *** |
| Barcelona | extreme | ppo_coop_ideal | random | 0.0281 | 0.2813 | ns |
| Barcelona | extreme | ppo_coop_chaos | ppo_chaos | 0.0207 | 0.2068 | ns |
| Barcelona | extreme | ppo_coop_chaos | fixed_time_opt | 0.0005 | 0.0047 | ** |
| Barcelona | extreme | ppo_coop_chaos | random | 0.2458 | 1.0000 | ns |
| Barcelona | extreme | ppo_chaos | fixed_time_opt | 0.0993 | 0.9926 | ns |
| Barcelona | extreme | ppo_chaos | random | 0.4204 | 1.0000 | ns |
| Barcelona | extreme | fixed_time_opt | random | 0.0378 | 0.3778 | ns |
| Quito | low | ppo_coop_ideal | ppo_coop_chaos | 0.0024 | 0.0238 | * |
| Quito | low | ppo_coop_ideal | ppo_chaos | 0.0679 | 0.6787 | ns |
| Quito | low | ppo_coop_ideal | fixed_time_opt | 0.0773 | 0.7727 | ns |
| Quito | low | ppo_coop_ideal | random | 0.0963 | 0.9626 | ns |
| Quito | low | ppo_coop_chaos | ppo_chaos | 0.7172 | 1.0000 | ns |
| Quito | low | ppo_coop_chaos | fixed_time_opt | 0.0001 | 0.0014 | ** |
| Quito | low | ppo_coop_chaos | random | 0.0000 | 0.0004 | *** |
| Quito | low | ppo_chaos | fixed_time_opt | 0.0013 | 0.0130 | * |
| Quito | low | ppo_chaos | random | 0.0012 | 0.0124 | * |
| Quito | low | fixed_time_opt | random | 0.7731 | 1.0000 | ns |
| Quito | mid | ppo_coop_ideal | ppo_coop_chaos | 0.0007 | 0.0073 | ** |
| Quito | mid | ppo_coop_ideal | ppo_chaos | 0.0002 | 0.0023 | ** |
| Quito | mid | ppo_coop_ideal | fixed_time_opt | 0.0657 | 0.6567 | ns |
| Quito | mid | ppo_coop_ideal | random | 0.4035 | 1.0000 | ns |
| Quito | mid | ppo_coop_chaos | ppo_chaos | 0.7958 | 1.0000 | ns |
| Quito | mid | ppo_coop_chaos | fixed_time_opt | 0.1087 | 1.0000 | ns |
| Quito | mid | ppo_coop_chaos | random | 0.0042 | 0.0423 | * |
| Quito | mid | ppo_chaos | fixed_time_opt | 0.0351 | 0.3514 | ns |
| Quito | mid | ppo_chaos | random | 0.0028 | 0.0275 | * |
| Quito | mid | fixed_time_opt | random | 0.3329 | 1.0000 | ns |
| Quito | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.0798 | 0.7978 | ns |
| Quito | mid_high | ppo_coop_ideal | ppo_chaos | 0.0032 | 0.0318 | * |
| Quito | mid_high | ppo_coop_ideal | fixed_time_opt | 0.0061 | 0.0610 | ns |
| Quito | mid_high | ppo_coop_ideal | random | 0.7394 | 1.0000 | ns |
| Quito | mid_high | ppo_coop_chaos | ppo_chaos | 0.1715 | 1.0000 | ns |
| Quito | mid_high | ppo_coop_chaos | fixed_time_opt | 0.5011 | 1.0000 | ns |
| Quito | mid_high | ppo_coop_chaos | random | 0.3329 | 1.0000 | ns |
| Quito | mid_high | ppo_chaos | fixed_time_opt | 0.4119 | 1.0000 | ns |
| Quito | mid_high | ppo_chaos | random | 0.0207 | 0.2068 | ns |
| Quito | mid_high | fixed_time_opt | random | 0.1055 | 1.0000 | ns |
| Quito | high | ppo_coop_ideal | ppo_coop_chaos | 0.1335 | 1.0000 | ns |
| Quito | high | ppo_coop_ideal | ppo_chaos | 0.0007 | 0.0069 | ** |
| Quito | high | ppo_coop_ideal | fixed_time_opt | 0.8073 | 1.0000 | ns |
| Quito | high | ppo_coop_ideal | random | 0.7283 | 1.0000 | ns |
| Quito | high | ppo_coop_chaos | ppo_chaos | 0.0468 | 0.4676 | ns |
| Quito | high | ppo_coop_chaos | fixed_time_opt | 0.0724 | 0.7245 | ns |
| Quito | high | ppo_coop_chaos | random | 0.0519 | 0.5188 | ns |
| Quito | high | ppo_chaos | fixed_time_opt | 0.0002 | 0.0023 | ** |
| Quito | high | ppo_chaos | random | 0.0002 | 0.0020 | ** |
| Quito | high | fixed_time_opt | random | 0.7958 | 1.0000 | ns |
| Quito | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.5011 | 1.0000 | ns |
| Quito | extreme | ppo_coop_ideal | ppo_chaos | 0.1120 | 1.0000 | ns |
| Quito | extreme | ppo_coop_ideal | fixed_time_opt | 0.4464 | 1.0000 | ns |
| Quito | extreme | ppo_coop_ideal | random | 0.2643 | 1.0000 | ns |
| Quito | extreme | ppo_coop_chaos | ppo_chaos | 0.2116 | 1.0000 | ns |
| Quito | extreme | ppo_coop_chaos | fixed_time_opt | 0.2519 | 1.0000 | ns |
| Quito | extreme | ppo_coop_chaos | random | 0.1260 | 1.0000 | ns |
| Quito | extreme | ppo_chaos | fixed_time_opt | 0.0615 | 0.6145 | ns |
| Quito | extreme | ppo_chaos | random | 0.0127 | 0.1273 | ns |
| Quito | extreme | fixed_time_opt | random | 0.8883 | 1.0000 | ns |
| Bogota | low | ppo_coop_ideal | ppo_coop_chaos | 0.0000 | 0.0001 | *** |
| Bogota | low | ppo_coop_ideal | ppo_chaos | 0.0003 | 0.0030 | ** |
| Bogota | low | ppo_coop_ideal | fixed_time_opt | 0.0001 | 0.0014 | ** |
| Bogota | low | ppo_coop_ideal | random | 0.0004 | 0.0040 | ** |
| Bogota | low | ppo_coop_chaos | ppo_chaos | 0.1297 | 1.0000 | ns |
| Bogota | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Bogota | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Bogota | low | ppo_chaos | fixed_time_opt | 0.0001 | 0.0007 | *** |
| Bogota | low | ppo_chaos | random | 0.0001 | 0.0007 | *** |
| Bogota | low | fixed_time_opt | random | 0.0000 | 0.0001 | *** |
| Bogota | mid | ppo_coop_ideal | ppo_coop_chaos | 0.3953 | 1.0000 | ns |
| Bogota | mid | ppo_coop_ideal | ppo_chaos | 0.8766 | 1.0000 | ns |
| Bogota | mid | ppo_coop_ideal | fixed_time_opt | 0.3790 | 1.0000 | ns |
| Bogota | mid | ppo_coop_ideal | random | 0.9117 | 1.0000 | ns |
| Bogota | mid | ppo_coop_chaos | ppo_chaos | 0.4464 | 1.0000 | ns |
| Bogota | mid | ppo_coop_chaos | fixed_time_opt | 0.9352 | 1.0000 | ns |
| Bogota | mid | ppo_coop_chaos | random | 0.4204 | 1.0000 | ns |
| Bogota | mid | ppo_chaos | fixed_time_opt | 0.6520 | 1.0000 | ns |
| Bogota | mid | ppo_chaos | random | 0.8534 | 1.0000 | ns |
| Bogota | mid | fixed_time_opt | random | 0.5298 | 1.0000 | ns |
| Bogota | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.6627 | 1.0000 | ns |
| Bogota | mid_high | ppo_coop_ideal | ppo_chaos | 0.2643 | 1.0000 | ns |
| Bogota | mid_high | ppo_coop_ideal | fixed_time_opt | 0.1958 | 1.0000 | ns |
| Bogota | mid_high | ppo_coop_ideal | random | 0.0014 | 0.0137 | * |
| Bogota | mid_high | ppo_coop_chaos | ppo_chaos | 0.6735 | 1.0000 | ns |
| Bogota | mid_high | ppo_coop_chaos | fixed_time_opt | 0.0635 | 0.6353 | ns |
| Bogota | mid_high | ppo_coop_chaos | random | 0.0001 | 0.0012 | ** |
| Bogota | mid_high | ppo_chaos | fixed_time_opt | 0.0156 | 0.1564 | ns |
| Bogota | mid_high | ppo_chaos | random | 0.0000 | 0.0003 | *** |
| Bogota | mid_high | fixed_time_opt | random | 0.0339 | 0.3387 | ns |
| Bogota | high | ppo_coop_ideal | ppo_coop_chaos | 0.2581 | 1.0000 | ns |
| Bogota | high | ppo_coop_ideal | ppo_chaos | 0.3112 | 1.0000 | ns |
| Bogota | high | ppo_coop_ideal | fixed_time_opt | 0.2340 | 1.0000 | ns |
| Bogota | high | ppo_coop_ideal | random | 0.4376 | 1.0000 | ns |
| Bogota | high | ppo_coop_chaos | ppo_chaos | 0.9352 | 1.0000 | ns |
| Bogota | high | ppo_coop_chaos | fixed_time_opt | 0.0315 | 0.3147 | ns |
| Bogota | high | ppo_coop_chaos | random | 0.5997 | 1.0000 | ns |
| Bogota | high | ppo_chaos | fixed_time_opt | 0.0156 | 0.1564 | ns |
| Bogota | high | ppo_chaos | random | 0.7506 | 1.0000 | ns |
| Bogota | high | fixed_time_opt | random | 0.0798 | 0.7978 | ns |
| Bogota | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.3329 | 1.0000 | ns |
| Bogota | extreme | ppo_coop_ideal | ppo_chaos | 0.0773 | 0.7727 | ns |
| Bogota | extreme | ppo_coop_ideal | fixed_time_opt | 0.3403 | 1.0000 | ns |
| Bogota | extreme | ppo_coop_ideal | random | 0.3871 | 1.0000 | ns |
| Bogota | extreme | ppo_coop_chaos | ppo_chaos | 0.3478 | 1.0000 | ns |
| Bogota | extreme | ppo_coop_chaos | fixed_time_opt | 0.0501 | 0.5012 | ns |
| Bogota | extreme | ppo_coop_chaos | random | 0.9823 | 1.0000 | ns |
| Bogota | extreme | ppo_chaos | fixed_time_opt | 0.0070 | 0.0697 | ns |
| Bogota | extreme | ppo_chaos | random | 0.3403 | 1.0000 | ns |
| Bogota | extreme | fixed_time_opt | random | 0.0351 | 0.3514 | ns |
| Berlin | low | ppo_coop_ideal | ppo_coop_chaos | 0.0138 | 0.1383 | ns |
| Berlin | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | low | fixed_time_opt | random | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_ideal | ppo_coop_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_ideal | fixed_time_opt | 0.7731 | 1.0000 | ns |
| Berlin | mid | ppo_coop_ideal | random | 0.0007 | 0.0065 | ** |
| Berlin | mid | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | mid | fixed_time_opt | random | 0.0000 | 0.0002 | *** |
| Berlin | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.0615 | 0.6145 | ns |
| Berlin | mid_high | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | ppo_coop_ideal | fixed_time_opt | 0.2458 | 1.0000 | ns |
| Berlin | mid_high | ppo_coop_ideal | random | 0.0004 | 0.0036 | ** |
| Berlin | mid_high | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | ppo_coop_chaos | fixed_time_opt | 0.0261 | 0.2608 | ns |
| Berlin | mid_high | ppo_coop_chaos | random | 0.0000 | 0.0003 | *** |
| Berlin | mid_high | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | fixed_time_opt | random | 0.0170 | 0.1695 | ns |
| Berlin | high | ppo_coop_ideal | ppo_coop_chaos | 0.4376 | 1.0000 | ns |
| Berlin | high | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | high | ppo_coop_ideal | fixed_time_opt | 0.6843 | 1.0000 | ns |
| Berlin | high | ppo_coop_ideal | random | 0.0292 | 0.2921 | ns |
| Berlin | high | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | high | ppo_coop_chaos | fixed_time_opt | 0.6414 | 1.0000 | ns |
| Berlin | high | ppo_coop_chaos | random | 0.0024 | 0.0238 | * |
| Berlin | high | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | high | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | high | fixed_time_opt | random | 0.0058 | 0.0583 | ns |
| Berlin | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.0010 | 0.0100 | * |
| Berlin | extreme | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | extreme | ppo_coop_ideal | fixed_time_opt | 0.0002 | 0.0016 | ** |
| Berlin | extreme | ppo_coop_ideal | random | 0.0003 | 0.0028 | ** |
| Berlin | extreme | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | extreme | ppo_coop_chaos | fixed_time_opt | 0.2398 | 1.0000 | ns |
| Berlin | extreme | ppo_coop_chaos | random | 0.2643 | 1.0000 | ns |
| Berlin | extreme | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | extreme | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | extreme | fixed_time_opt | random | 0.9000 | 1.0000 | ns |
| Madrid | low | ppo_coop_ideal | ppo_coop_chaos | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Madrid | low | fixed_time_opt | random | 0.0785 | 0.7851 | ns |
| Madrid | mid | ppo_coop_ideal | ppo_coop_chaos | 0.9587 | 1.0000 | ns |
| Madrid | mid | ppo_coop_ideal | ppo_chaos | 0.0006 | 0.0062 | ** |
| Madrid | mid | ppo_coop_ideal | fixed_time_opt | 0.0117 | 0.1171 | ns |
| Madrid | mid | ppo_coop_ideal | random | 0.1453 | 1.0000 | ns |
| Madrid | mid | ppo_coop_chaos | ppo_chaos | 0.0001 | 0.0009 | *** |
| Madrid | mid | ppo_coop_chaos | fixed_time_opt | 0.0040 | 0.0403 | * |
| Madrid | mid | ppo_coop_chaos | random | 0.0877 | 0.8771 | ns |
| Madrid | mid | ppo_chaos | fixed_time_opt | 0.6952 | 1.0000 | ns |
| Madrid | mid | ppo_chaos | random | 0.0339 | 0.3387 | ns |
| Madrid | mid | fixed_time_opt | random | 0.2282 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.7618 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_ideal | ppo_chaos | 0.7731 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_ideal | fixed_time_opt | 0.0406 | 0.4060 | ns |
| Madrid | mid_high | ppo_coop_ideal | random | 0.3953 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_chaos | ppo_chaos | 0.4290 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_chaos | fixed_time_opt | 0.0315 | 0.3147 | ns |
| Madrid | mid_high | ppo_coop_chaos | random | 0.3953 | 1.0000 | ns |
| Madrid | mid_high | ppo_chaos | fixed_time_opt | 0.1224 | 1.0000 | ns |
| Madrid | mid_high | ppo_chaos | random | 0.8187 | 1.0000 | ns |
| Madrid | mid_high | fixed_time_opt | random | 0.1188 | 1.0000 | ns |
| Madrid | high | ppo_coop_ideal | ppo_coop_chaos | 0.6843 | 1.0000 | ns |
| Madrid | high | ppo_coop_ideal | ppo_chaos | 0.0133 | 0.1327 | ns |
| Madrid | high | ppo_coop_ideal | fixed_time_opt | 0.8418 | 1.0000 | ns |
| Madrid | high | ppo_coop_ideal | random | 0.6843 | 1.0000 | ns |
| Madrid | high | ppo_coop_chaos | ppo_chaos | 0.0061 | 0.0610 | ns |
| Madrid | high | ppo_coop_chaos | fixed_time_opt | 0.5997 | 1.0000 | ns |
| Madrid | high | ppo_coop_chaos | random | 0.9823 | 1.0000 | ns |
| Madrid | high | ppo_chaos | fixed_time_opt | 0.0748 | 0.7483 | ns |
| Madrid | high | ppo_chaos | random | 0.0023 | 0.0227 | * |
| Madrid | high | fixed_time_opt | random | 0.5493 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.6414 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_ideal | ppo_chaos | 0.9941 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_ideal | fixed_time_opt | 0.6843 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_ideal | random | 0.1297 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_chaos | ppo_chaos | 0.5692 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_chaos | fixed_time_opt | 0.8534 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_chaos | random | 0.1624 | 1.0000 | ns |
| Madrid | extreme | ppo_chaos | fixed_time_opt | 0.6309 | 1.0000 | ns |
| Madrid | extreme | ppo_chaos | random | 0.1260 | 1.0000 | ns |
| Madrid | extreme | fixed_time_opt | random | 0.2116 | 1.0000 | ns |
| CDMX | low | ppo_coop_ideal | ppo_coop_chaos | 0.2519 | 1.0000 | ns |
| CDMX | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | low | fixed_time_opt | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_ideal | ppo_coop_chaos | 0.1137 | 1.0000 | ns |
| CDMX | mid | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | fixed_time_opt | random | 0.0000 | 0.0000 | *** |
| CDMX | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.5793 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_ideal | ppo_chaos | 0.0070 | 0.0697 | ns |
| CDMX | mid_high | ppo_coop_ideal | fixed_time_opt | 0.1373 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_ideal | random | 0.0002 | 0.0020 | ** |
| CDMX | mid_high | ppo_coop_chaos | ppo_chaos | 0.0436 | 0.4358 | ns |
| CDMX | mid_high | ppo_coop_chaos | fixed_time_opt | 0.0555 | 0.5555 | ns |
| CDMX | mid_high | ppo_coop_chaos | random | 0.0003 | 0.0027 | ** |
| CDMX | mid_high | ppo_chaos | fixed_time_opt | 0.0004 | 0.0042 | ** |
| CDMX | mid_high | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | mid_high | fixed_time_opt | random | 0.0933 | 0.9334 | ns |
| CDMX | high | ppo_coop_ideal | ppo_coop_chaos | 0.6735 | 1.0000 | ns |
| CDMX | high | ppo_coop_ideal | ppo_chaos | 0.5793 | 1.0000 | ns |
| CDMX | high | ppo_coop_ideal | fixed_time_opt | 0.2398 | 1.0000 | ns |
| CDMX | high | ppo_coop_ideal | random | 0.3790 | 1.0000 | ns |
| CDMX | high | ppo_coop_chaos | ppo_chaos | 0.8187 | 1.0000 | ns |
| CDMX | high | ppo_coop_chaos | fixed_time_opt | 0.1154 | 1.0000 | ns |
| CDMX | high | ppo_coop_chaos | random | 0.5493 | 1.0000 | ns |
| CDMX | high | ppo_chaos | fixed_time_opt | 0.0615 | 0.6145 | ns |
| CDMX | high | ppo_chaos | random | 0.8187 | 1.0000 | ns |
| CDMX | high | fixed_time_opt | random | 0.0163 | 0.1628 | ns |
| CDMX | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.1087 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_ideal | ppo_chaos | 0.0133 | 0.1327 | ns |
| CDMX | extreme | ppo_coop_ideal | fixed_time_opt | 0.0724 | 0.7245 | ns |
| CDMX | extreme | ppo_coop_ideal | random | 0.4464 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_chaos | ppo_chaos | 0.0877 | 0.8771 | ns |
| CDMX | extreme | ppo_coop_chaos | fixed_time_opt | 0.4376 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_chaos | random | 0.6204 | 1.0000 | ns |
| CDMX | extreme | ppo_chaos | fixed_time_opt | 0.4733 | 1.0000 | ns |
| CDMX | extreme | ppo_chaos | random | 0.0850 | 0.8500 | ns |
| CDMX | extreme | fixed_time_opt | random | 0.3042 | 1.0000 | ns |

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Barcelona | ppo_coop_ideal | 0.979 | 0.0000 | *** |
| Barcelona | ppo_coop_chaos | 0.979 | 0.0000 | *** |
| Barcelona | ppo_chaos | 0.980 | 0.0000 | *** |
| Barcelona | fixed_time_opt | 0.978 | 0.0000 | *** |
| Barcelona | random | 0.980 | 0.0000 | *** |
| Quito | ppo_coop_ideal | 0.965 | 0.0000 | *** |
| Quito | ppo_coop_chaos | 0.956 | 0.0000 | *** |
| Quito | ppo_chaos | 0.958 | 0.0000 | *** |
| Quito | fixed_time_opt | 0.961 | 0.0000 | *** |
| Quito | random | 0.948 | 0.0000 | *** |
| Bogota | ppo_coop_ideal | 0.975 | 0.0000 | *** |
| Bogota | ppo_coop_chaos | 0.978 | 0.0000 | *** |
| Bogota | ppo_chaos | 0.976 | 0.0000 | *** |
| Bogota | fixed_time_opt | 0.978 | 0.0000 | *** |
| Bogota | random | 0.976 | 0.0000 | *** |
| Berlin | ppo_coop_ideal | 0.979 | 0.0000 | *** |
| Berlin | ppo_coop_chaos | 0.979 | 0.0000 | *** |
| Berlin | ppo_chaos | 0.980 | 0.0000 | *** |
| Berlin | fixed_time_opt | 0.978 | 0.0000 | *** |
| Berlin | random | 0.973 | 0.0000 | *** |
| Madrid | ppo_coop_ideal | 0.980 | 0.0000 | *** |
| Madrid | ppo_coop_chaos | 0.980 | 0.0000 | *** |
| Madrid | ppo_chaos | 0.980 | 0.0000 | *** |
| Madrid | fixed_time_opt | 0.980 | 0.0000 | *** |
| Madrid | random | 0.980 | 0.0000 | *** |
| CDMX | ppo_coop_ideal | 0.980 | 0.0000 | *** |
| CDMX | ppo_coop_chaos | 0.977 | 0.0000 | *** |
| CDMX | ppo_chaos | 0.977 | 0.0000 | *** |
| CDMX | fixed_time_opt | 0.980 | 0.0000 | *** |
| CDMX | random | 0.973 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
