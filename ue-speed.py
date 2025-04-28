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
                    dl_bitrate = cell.get('dl_bitrate', 0)
                    
                    # 转换为 Mbps (dl_bitrate 是 bits/s)
                    dl_bitrate_mbps = dl_bitrate / 1000000
                    
                    # 获取当前时间
                    timestamp = datetime.now()
                    
                    # 计算累计流量
                    if 'erab_list' in ue and len(ue['erab_list']) > 0:
                        erab = ue['erab_list'][0]
                        current_bytes = erab.get('dl_total_bytes', 0)
                        
                        if self.last_bytes > 0 and self.last_time:
                            time_diff = (timestamp - self.last_time).total_seconds()
                            if time_diff > 0:
                                bytes_diff = current_bytes - self.last_bytes
                                avg_rate = (bytes_diff * 8) / (time_diff * 1000000)  # 转换为 Mbps
                            else:
                                avg_rate = 0
                        else:
                            avg_rate = 0
                            
                        self.last_bytes = current_bytes
                        self.last_time = timestamp
                        
                        # 只打印关键速率信息
                        print(f"{timestamp.strftime('%H:%M:%S')}: UE[{self.ue_id}] Instant Rate: {dl_bitrate_mbps:.2f} Mbps, Avg Rate: {avg_rate:.2f} Mbps, Total DL: {current_bytes/1024/1024:.2f} MB")
                        
                        # 保存数据
                        self.data.append({
                            'timestamp': timestamp,
                            'instant_rate': dl_bitrate_mbps,
                            'avg_rate': avg_rate,
                            'total_bytes': current_bytes
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
        # 发送初始请求
        request = {
            "ue_id": self.ue_id,
            "stats": True,
            "message": "ue_get",
            "message_id": "ENB_ue_get_"
        }
        ws.send(json.dumps(request))

    def start_monitoring(self):
        # 禁用 WebSocket 调试输出
        websocket.enableTrace(False)
        
        # 创建 WebSocket 连接
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

        # 在新线程中运行 WebSocket
        self.running = True
        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()

        try:
            while self.running:
                # 每秒发送一次请求
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
            filename = f'ue_{self.ue_id}_throughput.csv'
            df.to_csv(filename, index=False)
            print(f"\nData saved to {filename}")
            
            # 计算统计信息
            if len(df) > 0:
                print(f"\nStatistics for UE[{self.ue_id}]:")
                print(f"Average Rate: {df['instant_rate'].mean():.2f} Mbps")
                print(f"Max Rate: {df['instant_rate'].max():.2f} Mbps")
                print(f"Min Rate: {df['instant_rate'].min():.2f} Mbps")
                print(f"Total Data: {df['total_bytes'].iloc[-1]/1024/1024:.2f} MB")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitor UE throughput via WebSocket')
    parser.add_argument('--ue-id', type=int, required=True, help='UE ID to monitor')
    parser.add_argument('--ws-url', type=str, default="ws://127.0.0.1:9001/",
                      help='WebSocket server URL (default: ws://127.0.0.1:9001/)')
    return parser.parse_args()

def main():
    # 解析命令行参数
    args = parse_arguments()

    # 创建监控实例
    monitor = UEMonitor(args.ws_url, args.ue_id)
    
    try:
        print(f"Starting UE[{args.ue_id}] throughput monitoring...")
        print("Press Ctrl+C to stop")
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()
