#送信伝文自動生成
import socket
import threading
import random
import time
from datetime import datetime
import json
import components.prepare_json as pj

# サーバー設定
HOST = '127.0.0.1'  # すべてのインターフェースで接続待ち
PORT_LIST = [20000, 20001, 20002, 20003]  # クライアントと一致させる
MACHINE_LIST = [1,2,3,4]
INTERVAL = 1.5  # sec
SEND_NUM_PER_LOT=20
LOT_NUM=5

UNIT_DICT={
    "U1_TR":[pj.prepare_ld_tr],
    "U1_A1":[pj.prepare_arm_count],
    "U2_PH":[pj.prepare_ph],
    "U2_A1":[pj.prepare_arm_count],
    "U2_TS":[pj.prepare_ts_pass],
    "U2_A2":[pj.prepare_arm_count],
    "U3_A1":[pj.prepare_arm_count],
    "U3_TS":[pj.prepare_ts_pass],
    "U3_A2":[pj.prepare_arm_count],
    "U4_A1":[pj.prepare_arm_count],
    "U4_TS":[pj.prepare_ts_pass],
    "U4_A2":[pj.prepare_arm_count],
    "U5_A1":[pj.prepare_arm_count],
    "U5_TS":[pj.prepare_ts_pass],
    "U5_A2":[pj.prepare_arm_count],
    "U6_A1":[pj.prepare_arm_count],
    "U6_TS":[pj.prepare_ts_ip],
    "U6_A2":[pj.prepare_arm_count],
    "U6_T1":[pj.prepare_t1_ip],
    "U6_T2":[pj.prepare_t2_ip],
    "U7_PH":[pj.prepare_ph],
    "U7_PI":[pj.prepare_uld_pi],
    "U7_CI":[pj.prepare_uld_ci],
    "U7_A1":[pj.prepare_arm_count],
}

# txtファイルを読み込んで一定間隔でデータを送り続ける
def send_data(conn, machine_no):
    try:
        for i in range(LOT_NUM):
            machine_name=MACHINE_LIST[machine_no]
            unique_str=datetime.now().strftime("%m%d%H%S%f")
            lot_name=f"LOT{unique_str}"
            type_name=f"TYPE{unique_str}"
            serial=1
            for j in range(SEND_NUM_PER_LOT):
                newSendFlag=True
                for idx,key in enumerate(UNIT_DICT): 
                    if newSendFlag:
                        send_dict={}
                        send_dict["LOT"]=lot_name
                        send_dict["TYPE"]=type_name
                        send_dict["MACHINE"]=machine_name
                        count=0
                        newSendFlag=False

                    if key=="U1_TR" or key=="U7_PI":
                        send_dict[f"{key}_{count}"]=UNIT_DICT[key][0](serial,unique_str)
                        count+=1
                    else:
                        send_dict[f"{key}_{count}"]=UNIT_DICT[key][0](serial)
                        count+=1

                    if idx==len(list(UNIT_DICT.keys()))-1: #100回に1回どこかのユニットのアラーム送信
                        if serial%100==0: #100回に1回どこかのユニットのアラーム送信
                            alarm_unit_no=random.randint(1,7)
                            key_name=f"U{alarm_unit_no}_AL"
                            send_dict[f"{key_name}_{count}"]=pj.prepare_alarm(serial)
                            count+=1

                    #3回に1回もしくは最後に送信してdictをリセット
                    if idx%7==0 or idx==len(list(UNIT_DICT.keys()))-1:
                        encoded_data=json.dumps(send_dict).encode('utf-8')
                        conn.sendall(encoded_data)
                        print(f"[送信_{idx}] {machine_name}: {len(encoded_data)}byte")
                        time.sleep(INTERVAL)
                        newSendFlag=True

                serial+=1

    except Exception as e:
        print(f"[エラー] 送信中に問題が発生しました: {e}")
    finally:
        conn.close()
        print(f"[切断] {machine_name} のクライアント接続を閉じました")

# 各ポートでサーバーを起動
def start_server(host_ip, host_port, machine_no):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host_ip, host_port))
        server_sock.listen()
        print(f"[待機中] {host_ip}:{host_port} で接続待機中...")

        while True:
            conn, addr = server_sock.accept()
            print(f"[接続] クライアント: {addr}")
            thread = threading.Thread(target=send_data, args=(conn, machine_no), daemon=True)
            thread.start()  # ✅ 修正: join()は不要。接続ごとに独立スレッドで並行処理


if __name__ == "__main__":
    threads = []
    for i,port in enumerate(PORT_LIST):
        thread = threading.Thread(target=start_server, args=(HOST, port, i), daemon=True)
        thread.start()
        threads.append(thread)

    print("[起動完了] 全サーバースレッドが稼働中です。Ctrl+Cで終了。")

    # メインスレッドを維持
    for t in threads:
        t.join()

