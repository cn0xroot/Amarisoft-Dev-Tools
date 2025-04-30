#!/usr/bin/env python3
import websocket
import json
import time
from datetime import datetime
import threading
import pandas as pd
import argparse

class UEMonitor:
    def __init__(self, ws_url, ue_id):
        self.ws_url = ws_url
        self.ue_id = ue_id
        self.data = []
        self.ws = None
        self.running = False
        self.last_bytes = 0
        self.last_time = None

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if 'ue_list' in data and len(data['ue_list']) > 0:
                ue = data['ue_list'][0]
                if 'cells' in ue and len(ue['cells']) > 0:
                    cell = ue['cells'][0]
                    
                    # 提取信号强度信息
                    signal_strength = {
                        'epre': cell.get('epre', 0),  # 参考信号接收功率
                        'ul_path_loss': cell.get('ul_path_loss', 0),  # 上行路径损耗
                        'p_ue': cell.get('p_ue', 0)  # UE发射功率
                    }
                    
                    # 提取信号质量信息
                    signal_quality = {
                        'pucch1_snr': cell.get('pucch1_snr', 0),  # PUCCH信噪比
                        'pusch_snr': cell.get('pusch_snr', 0),  # PUSCH信噪比
                        'cqi': cell.get('cqi', 0)  # 信道质量指示
                    }
                    
                    # 提取调制编码信息
                    modulation_coding = {
                        'dl_mcs': cell.get('dl_mcs', 0),  # 下行调制编码方案
                        'ul_mcs': cell.get('ul_mcs', 0),  # 上行调制编码方案
                        'ul_n_layer': cell.get('ul_n_layer', 0)  # 上行MIMO层数
                    }
                    
                    # 提取传输性能信息
                    dl_bitrate = cell.get('dl_bitrate', 0)
                    dl_bitrate_mbps = dl_bitrate / 1000000
                    
                    timestamp = datetime.now()
                    
                    if 'erab_list' in ue and len(ue['erab_list']) > 0:
                        erab = ue['erab_list'][0]
                        current_bytes = erab.get('dl_total_bytes', 0)
                        
                        if self.last_bytes > 0 and self.last_time:
                            time_diff = (timestamp - self.last_time).total_seconds()
                            if time_diff > 0:
                                bytes_diff = current_bytes - self.last_bytes
                                avg_rate = (bytes_diff * 8) / (time_diff * 1000000)
                            else:
                                avg_rate = 0
                        else:
                            avg_rate = 0
                            
                        self.last_bytes = current_bytes
                        self.last_time = timestamp
                        
                        # 打印所有关键信息
                        print(f"{timestamp.strftime('%H:%M:%S')}: UE[{self.ue_id}]")
                        print(f"  Instant Rate: {dl_bitrate_mbps:.2f} Mbps, Avg Rate: {avg_rate:.2f} Mbps, Total DL: {current_bytes/1024/1024:.2f} MB")
                        print(f"  Signal Strength: EPRE={signal_strength['epre']:.1f}dBm, Path Loss={signal_strength['ul_path_loss']:.1f}dB, P_UE={signal_strength['p_ue']:.1f}dBm")
                        print(f"  Signal Quality: PUCCH SNR={signal_quality['pucch1_snr']:.1f}dB, PUSCH SNR={signal_quality['pusch_snr']:.1f}dB, CQI={signal_quality['cqi']}")
                        print(f"  Modulation Coding: DL MCS={modulation_coding['dl_mcs']:.1f}, UL MCS={modulation_coding['ul_mcs']}, UL Layers={modulation_coding['ul_n_layer']}")
                        print("  " + "-"*50)
                        
                        # 保存数据
                        self.data.append({
                            'timestamp': timestamp,
                            'instant_rate': dl_bitrate_mbps,
                            'avg_rate': avg_rate,
                            'total_bytes': current_bytes,
                            **signal_strength,
                            **signal_quality,
                            **modulation_coding
                        })
                        
        except json.JSONDecodeError:
            print(f"Error decoding message: {message}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")

    def on_open(self, ws):
        request = {
            "ue_id": self.ue_id,
            "stats": True,
            "message": "ue_get",
            "message_id": "ENB_ue_get_"
        }
        ws.send(json.dumps(request))

    def start_monitoring(self):
        websocket.enableTrace(False)
        
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

        self.running = True
        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()

        try:
            while self.running:
                if self.ws and self.ws.sock and self.ws.sock.connected:
                    request = {
                        "ue_id": self.ue_id,
                        "stats": True,
                        "message": "ue_get",
                        "message_id": "ENB_ue_get_"
                    }
                    self.ws.send(json.dumps(request))
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping monitoring...")
            self.stop_monitoring()

    def stop_monitoring(self):
        self.running = False
        if self.ws:
            self.ws.close()
        self.save_data()

    def save_data(self):
        if self.data:
            df = pd.DataFrame(self.data)
            filename = f'ue_{self.ue_id}_monitor.csv'
            df.to_csv(filename, index=False)
            print(f"\nData saved to {filename}")
            
            if len(df) > 0:
                print(f"\nStatistics for UE[{self.ue_id}]:")
                print(f"Average Rate: {df['instant_rate'].mean():.2f} Mbps")
                print(f"Max Rate: {df['instant_rate'].max():.2f} Mbps")
                print(f"Min Rate: {df['instant_rate'].min():.2f} Mbps")
                print(f"Total Data: {df['total_bytes'].iloc[-1]/1024/1024:.2f} MB")
                print("\nSignal Statistics:")
                print(f"Average EPRE: {df['epre'].mean():.1f}dBm")
                print(f"Average Path Loss: {df['ul_path_loss'].mean():.1f}dB")
                print(f"Average CQI: {df['cqi'].mean():.1f}")
                print(f"Average DL MCS: {df['dl_mcs'].mean():.1f}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitor UE throughput and signal parameters via WebSocket')
    parser.add_argument('--ue-id', type=int, required=True, help='UE ID to monitor')
    parser.add_argument('--ws-url', type=str, default="ws://127.0.0.1:9001/",
                      help='WebSocket server URL (default: ws://127.0.0.1:9001/)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    monitor = UEMonitor(args.ws_url, args.ue_id)
    
    try:
        print(f"Starting UE[{args.ue_id}] monitoring...")
        print("Press Ctrl+C to stop")
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()
