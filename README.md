# Amarisoft-Dev-Tools
基于Amarisoft API 进行二次开发的实用工具、脚本。

实时监控UE的信号状态、网速吞吐率；
分析信号质量变化；
评估调制编码方案的效果；
保存历史数据供后续分析；


```bash
python3 ue-info.py --ue-id 3
Starting UE[3] monitoring...
Press Ctrl+C to stop
14:08:38: UE[3]
  Instant Rate: 14.46 Mbps, Avg Rate: 0.00 Mbps, Total DL: 12.27 MB
  Signal Strength: EPRE=-65.1dBm, Path Loss=20.3dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.9dB, PUSCH SNR=24.8dB, CQI=14
  Modulation Coding: DL MCS=24.5, UL MCS=25.2, UL Layers=1
  --------------------------------------------------
14:08:39: UE[3]
  Instant Rate: 18.42 Mbps, Avg Rate: 16.95 Mbps, Total DL: 14.29 MB
  Signal Strength: EPRE=-71.5dBm, Path Loss=20.6dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.8dB, PUSCH SNR=18.6dB, CQI=15
  Modulation Coding: DL MCS=23.6, UL MCS=24.6, UL Layers=1
  --------------------------------------------------
14:08:40: UE[3]
  Instant Rate: 17.62 Mbps, Avg Rate: 14.37 Mbps, Total DL: 16.01 MB
  Signal Strength: EPRE=-69.5dBm, Path Loss=21.0dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=28.0dB, PUSCH SNR=17.5dB, CQI=15
  Modulation Coding: DL MCS=23.1, UL MCS=26.2, UL Layers=1
  --------------------------------------------------
14:08:41: UE[3]
  Instant Rate: 23.54 Mbps, Avg Rate: 17.78 Mbps, Total DL: 18.14 MB
  Signal Strength: EPRE=-65.7dBm, Path Loss=21.3dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=28.0dB, PUSCH SNR=23.1dB, CQI=13
  Modulation Coding: DL MCS=22.0, UL MCS=26.2, UL Layers=1
  --------------------------------------------------
14:08:42: UE[3]
  Instant Rate: 20.46 Mbps, Avg Rate: 14.70 Mbps, Total DL: 19.87 MB
  Signal Strength: EPRE=-65.1dBm, Path Loss=21.4dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.7dB, PUSCH SNR=23.4dB, CQI=12
  Modulation Coding: DL MCS=23.0, UL MCS=26.8, UL Layers=1
  --------------------------------------------------
14:08:43: UE[3]
  Instant Rate: 20.96 Mbps, Avg Rate: 12.54 Mbps, Total DL: 21.38 MB
  Signal Strength: EPRE=-69.2dBm, Path Loss=21.4dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.9dB, PUSCH SNR=16.2dB, CQI=14
  Modulation Coding: DL MCS=25.1, UL MCS=26, UL Layers=1
  --------------------------------------------------
14:08:44: UE[3]
  Instant Rate: 22.06 Mbps, Avg Rate: 12.34 Mbps, Total DL: 22.85 MB
  Signal Strength: EPRE=-69.3dBm, Path Loss=21.6dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.3dB, PUSCH SNR=16.1dB, CQI=14
  Modulation Coding: DL MCS=24.4, UL MCS=26.7, UL Layers=1
  --------------------------------------------------
14:08:45: UE[3]
  Instant Rate: 19.50 Mbps, Avg Rate: 12.20 Mbps, Total DL: 24.31 MB
  Signal Strength: EPRE=-69.0dBm, Path Loss=21.5dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.6dB, PUSCH SNR=15.9dB, CQI=14
  Modulation Coding: DL MCS=24.5, UL MCS=27.1, UL Layers=1
  --------------------------------------------------
14:08:46: UE[3]
  Instant Rate: 21.10 Mbps, Avg Rate: 16.06 Mbps, Total DL: 26.20 MB
  Signal Strength: EPRE=-43.5dBm, Path Loss=21.4dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.8dB, PUSCH SNR=-3.2dB, CQI=15
  Modulation Coding: DL MCS=23.2, UL MCS=27.1, UL Layers=1
  --------------------------------------------------
14:08:47: UE[3]
  Instant Rate: 19.43 Mbps, Avg Rate: 11.72 Mbps, Total DL: 27.61 MB
  Signal Strength: EPRE=-69.4dBm, Path Loss=21.4dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=28.0dB, PUSCH SNR=15.8dB, CQI=15
  Modulation Coding: DL MCS=24.2, UL MCS=27.8, UL Layers=1
  --------------------------------------------------
14:08:48: UE[3]
  Instant Rate: 18.63 Mbps, Avg Rate: 9.69 Mbps, Total DL: 28.76 MB
  Signal Strength: EPRE=-69.6dBm, Path Loss=21.5dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.7dB, PUSCH SNR=14.3dB, CQI=14
  Modulation Coding: DL MCS=24.1, UL MCS=27.2, UL Layers=1
  --------------------------------------------------
14:08:49: UE[3]
  Instant Rate: 19.38 Mbps, Avg Rate: 11.39 Mbps, Total DL: 30.13 MB
  Signal Strength: EPRE=-68.7dBm, Path Loss=21.6dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=28.2dB, PUSCH SNR=15.2dB, CQI=14
  Modulation Coding: DL MCS=24.1, UL MCS=27.1, UL Layers=1
  --------------------------------------------------
14:08:50: UE[3]
  Instant Rate: 11.70 Mbps, Avg Rate: 13.00 Mbps, Total DL: 31.67 MB
  Signal Strength: EPRE=-43.6dBm, Path Loss=21.6dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.7dB, PUSCH SNR=-3.1dB, CQI=14
  Modulation Coding: DL MCS=25.0, UL MCS=27.1, UL Layers=1
  --------------------------------------------------
14:08:51: UE[3]
  Instant Rate: 13.97 Mbps, Avg Rate: 12.15 Mbps, Total DL: 33.13 MB
  Signal Strength: EPRE=-69.6dBm, Path Loss=21.5dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=28.3dB, PUSCH SNR=15.8dB, CQI=14
  Modulation Coding: DL MCS=24.7, UL MCS=27.1, UL Layers=1
  --------------------------------------------------
14:08:52: UE[3]
  Instant Rate: 23.03 Mbps, Avg Rate: 12.84 Mbps, Total DL: 34.68 MB
  Signal Strength: EPRE=-69.3dBm, Path Loss=21.6dB, P_UE=-30.0dBm
  Signal Quality: PUCCH SNR=27.8dB, PUSCH SNR=14.8dB, CQI=14
  Modulation Coding: DL MCS=24.5, UL MCS=27, UL Layers=1

```
