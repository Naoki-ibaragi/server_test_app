import socket
import threading
import time
import os

# サーバー設定
HOST = '0.0.0.0'  # すべてのインターフェースで接続待ち
PORT_LIST = [20000, 20001, 20002, 20003]  # クライアントと一致させる
TXT_LIST = [
    "2533F0686J_PLC_1.txt",
    "2533F0688J_PLC_2.txt",
    "2533F07C9J_PLC_3.txt",
    "2531F0230J_PLC_4.txt"
]
INTERVAL = 3  # sec


# txtファイルを読み込んで一定間隔でデータを送り続ける
def send_data(conn, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            all_lines = f.read().splitlines()  # ✅ 修正：split("\n") ではなく read().splitlines() を使用

        for send_data in all_lines:
            if not send_data:
                continue  # 空行はスキップ
            conn.sendall(send_data.encode('utf-8'))  # ✅ 修正：str → bytes に変換
            print(f"[送信] {file_path}: {send_data}")
            time.sleep(INTERVAL)
    except Exception as e:
        print(f"[エラー] {file_path} の送信中に問題が発生しました: {e}")
    finally:
        conn.close()
        print(f"[切断] {file_path} のクライアント接続を閉じました")


# 各ポートでサーバーを起動
def start_server(host_ip, host_port, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host_ip, host_port))
        server_sock.listen()
        print(f"[待機中] {host_ip}:{host_port} で接続待機中...")

        while True:
            conn, addr = server_sock.accept()
            print(f"[接続] クライアント: {addr}")
            thread = threading.Thread(target=send_data, args=(conn, file_path), daemon=True)
            thread.start()  # ✅ 修正: join()は不要。接続ごとに独立スレッドで並行処理


if __name__ == "__main__":
    threads = []
    for port, file_path in zip(PORT_LIST, TXT_LIST):
        thread = threading.Thread(target=start_server, args=(HOST, port, file_path), daemon=True)
        thread.start()
        threads.append(thread)

    print("[起動完了] 全サーバースレッドが稼働中です。Ctrl+Cで終了。")

    # メインスレッドを維持
    for t in threads:
        t.join()

