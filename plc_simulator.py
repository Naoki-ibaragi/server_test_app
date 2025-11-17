import socket
import threading
import random
import time
import json
import components.prepare_json as pj

# サーバー設定
HOST = '0.0.0.0'  # すべてのインターフェースで接続待ち
PORT_LIST = [20000, 20001, 20002, 20003]  # クライアントと一致させる
MACHINE_LIST = ["CLT_1","CLT_2","CLT_3","CLT_4"]
LOTNAME_LIST = ["2025A1114","2025B1114","2025C1114","2025D1114"]
INTERVAL = 2  # sec
SEND_NUM=100
NUM_PER_SEND=10 #1回の送信で何個分の情報を送るか
TYPE_NAME="MH15376WJCCRB"

UNIT_DICT={
    "U1_TR":[pj.prepare_ld_tr()],
    "U1_A1":[pj.prepare_arm_count()],
    "U2_PH":[pj.prepare_ph()],
    "U2_A1":[pj.prepare_arm_count()],
    "U2_TS":[pj.prepare_ts_pass(),pj.prepare_ts_fail()],
    "U2_A2":[pj.prepare_arm_count()],
    "U3_A1":[pj.prepare_arm_count()],
    "U3_TS":[pj.prepare_ts_pass(),pj.prepare_ts_fail()],
    "U3_A2":[pj.prepare_arm_count()],
    "U4_A1":[pj.prepare_arm_count()],
    "U4_TS":[pj.prepare_ts_pass(),pj.prepare_ts_fail()],
    "U4_A2":[pj.prepare_arm_count()],
    "U5_A1":[pj.prepare_arm_count()],
    "U5_TS":[pj.prepare_ts_pass(),pj.prepare_ts_fail()],
    "U5_A2":[pj.prepare_arm_count()],
    "U6_A1":[pj.prepare_arm_count()],
    "U6_TS":[pj.prepare_ts_ip()],
    "U6_A2":[pj.prepare_arm_count()],
    "U6_T1":[pj.prepare_t1_ip()],
    "U6_T2":[pj.prepare_t2_ip()],
    "U7_PH":[pj.prepare_ph()],
    "U7_PI":[pj.prepare_uld_pi()],
    "U7_CI":[pj.prepare_uld_ci()],
    "U7_A1":[pj.prepare_arm_count()],
    "U1_AL":[pj.prepare_alarm()],
    "U2_AL":[pj.prepare_alarm()],
    "U3_AL":[pj.prepare_alarm()],
    "U4_AL":[pj.prepare_alarm()],
    "U5_AL":[pj.prepare_alarm()],
    "U6_AL":[pj.prepare_alarm()],
    "U7_AL":[pj.prepare_alarm()],
}

UNIT_KEY_LIST=list(UNIT_DICT.keys())

# txtファイルを読み込んで一定間隔でデータを送り続ける
def send_data(conn, machine,lot_name):
    try:
        for i in range(SEND_NUM):
            print(i)
            send_dict={}
            send_dict["LOT"]=lot_name
            send_dict["TYPE"]=TYPE_NAME
            send_dict["MACHINE"]=machine
            count=0
            for j in range(NUM_PER_SEND):
                key_num=random.randint(0,len(UNIT_KEY_LIST)-1)
                key_name=UNIT_KEY_LIST[key_num]
                func_num=random.randint(0,len(UNIT_DICT[key_name])-1)

                send_dict[f"{key_name}_{count}"]=UNIT_DICT[key_name][func_num]
                count+=1

            conn.sendall(json.dumps(send_dict).encode('utf-8'))  # ✅ 修正：str → bytes に変換
            print(f"[送信] {machine}: {send_dict}")
            time.sleep(INTERVAL)

    except Exception as e:
        print(f"[エラー] 送信中に問題が発生しました: {e}")
    finally:
        conn.close()
        print(f"[切断] {machine} のクライアント接続を閉じました")

# 各ポートでサーバーを起動
def start_server(host_ip, host_port, machine,lot_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host_ip, host_port))
        server_sock.listen()
        print(f"[待機中] {host_ip}:{host_port} で接続待機中...")

        while True:
            conn, addr = server_sock.accept()
            print(f"[接続] クライアント: {addr}")
            thread = threading.Thread(target=send_data, args=(conn, machine,lot_name), daemon=True)
            thread.start()  # ✅ 修正: join()は不要。接続ごとに独立スレッドで並行処理


if __name__ == "__main__":
    threads = []
    for i,port in enumerate(PORT_LIST):
        thread = threading.Thread(target=start_server, args=(HOST, port, MACHINE_LIST[i],LOTNAME_LIST[i]), daemon=True)
        thread.start()
        threads.append(thread)

    print("[起動完了] 全サーバースレッドが稼働中です。Ctrl+Cで終了。")

    # メインスレッドを維持
    for t in threads:
        t.join()

