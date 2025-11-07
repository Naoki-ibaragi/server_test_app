import socket
import threading
import time
import json

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
TYPE_NAME="MH15376WJCCRB"

ALL_UNIT_LIST=["U1","U2","U3","U4","U5","U6","U7"]

def int_plus(num):
    try:
        return int(num)
    except:
        return 0

#ユニットデータをdictに追加する
def add_data_to_dict(unit_data,result_dict,item_num):
    if unit_data[0]=="U1" and unit_data[1]=="PH": #LDトレイ
        pf=unit_data[2]
        sreial=unit_data[4]
        arm_pos=unit_data[5]
        tray_pocket_x=unit_data[6]
        tray_pocket_y=unit_data[7]
        tray_pocket_align_x=unit_data[8]
        tray_pocket_align_y=unit_data[9]
        key_name=f"U1_PH_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "serial":int_plus(sreial),
            "arm_pos":arm_pos,
            "tpx":int_plus(tray_pocket_x),
            "tpy":int_plus(tray_pocket_y),
            "tpax":int_plus(tray_pocket_align_x),
            "tpay":int_plus(tray_pocket_align_y),
        }
    elif unit_data[0] in ALL_UNIT_LIST and unit_data[1]=="A1": #各ユニットの上流アーム
        pf=unit_data[2]
        sreial=unit_data[4]
        count=unit_data[5]
        key_name=f"{unit_data[0]}_A1_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "serial":int_plus(sreial),
            "count":int_plus(count),
        }
    elif unit_data[0] in ALL_UNIT_LIST and unit_data[1]=="A2": #各ユニットの下流アーム
        pf=unit_data[2]
        sreial=unit_data[4]
        count=unit_data[5]
        key_name=f"{unit_data[0]}_A1_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "serial":int_plus(sreial),
            "count":int_plus(count),
        }
    elif unit_data[0] in ["U2","U7"] and unit_data[1]=="PH": #DC1とULDの予熱テーブル
        pf=unit_data[2]
        sreial=unit_data[4]
        align_x=unit_data[5]
        align_y=unit_data[6]
        align_t=unit_data[7]
        key_name=f"{unit_data[0]}_PH_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "serial":int_plus(sreial),
            "ax":int_plus(align_x),
            "ay":int_plus(align_y),
            "at":int_plus(align_t),
        }
    elif unit_data[0] in ["U2","U3","U4","U5"] and unit_data[1]=="TS": #測定テーブル
        pf=unit_data[2]
        sreial=unit_data[4]
        stage_serial=unit_data[5]
        stage_count=unit_data[6]
        probe_serial=unit_data[7]
        probe_count=unit_data[8]
        probe_x1=unit_data[9]
        probe_y1=unit_data[10]
        probe_x2=unit_data[11]
        probe_y2=unit_data[12]
        chip_align_x=unit_data[13]
        chip_align_y=unit_data[14]
        chip_align_t=unit_data[15]
        key_name=f"{unit_data[0]}_TS_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "serial":int_plus(sreial),
            "st_serial":stage_serial,
            "st_count":int_plus(stage_count),
            "pr_serial":probe_serial,
            "pr_count":int_plus(probe_count),
            "prx1":int_plus(probe_x1),
            "pry1":int_plus(probe_y1),
            "prx2":int_plus(probe_x2),
            "pry2":int_plus(probe_y2),
            "cx":int_plus(chip_align_x),
            "cy":int_plus(chip_align_y),
            "ct":int_plus(chip_align_t),
        }
    elif unit_data[0]=="U6" and unit_data[1]=="TS": #外観テーブル
        pf=unit_data[2]
        sreial=unit_data[4]
        count=unit_data[5]
 
        key_name=f"{unit_data[0]}_TS_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "serial":int_plus(sreial),
            "st_count":int_plus(count),
        }
    elif unit_data[0]=="U7" and (unit_data[1]=="PI" or unit_data[1]=="CI"): #ULD ポケットインスペ
        pf=unit_data[2]
        sreial=unit_data[4]
        px=unit_data[5]
        py=unit_data[6]
        ax=unit_data[7]
        ay=unit_data[8]
 
        key_name=f"{unit_data[0]}_PI_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "serial":int_plus(sreial),
            "px":int_plus(px),
            "py":int_plus(py),
            "ax":int_plus(ax),
            "ax":int_plus(ay),
        }
    elif unit_data[0] in ALL_UNIT_LIST and unit_data[1]=="AL": #各ユニットのアラーム情報
        al_num=unit_data[2]
        #serialはlist
        serial_list=unit_data[4:]
        serial_list=[ int_plus(s) for s in serial_list]

        key_name=f"{unit_data[0]}_AL_{item_num}"
        result_dict[key_name]={
            "pf":pf,
            "al_num":int_plus(al_num),
            "serial_list":serial_list
        }
    else:
        raise ValueError(f"データ形式が不明です:{unit_data}")
    
#カンマ区切り形式をjson形式に変更する
def data_arrange(data):
    result_dict={}
    item_num=0
    item_list=data.split(",")
    for idx,item in enumerate(item_list):
        unit_data=[]
        if item in ["U1","U2","U3","U4","U5","U6","U7"]:
            unit_data.append(item)
            idx_2=1
            while idx+idx_2 < len(item_list) and item_list[idx+idx_2] not in ["U1","U2","U3","U4","U5","U6","U7"]:
                unit_data.append(item_list[idx+idx_2])
                idx_2+=1
        else:
            continue

        try:    
            add_data_to_dict(unit_data,result_dict,item_num)
            item_num+=1
        except Exception as e:
            print("data変換でエラーが発生")
            print(f"データ内容:{unit_data}")
            print(f"エラー内容:{e}")

    return result_dict


# txtファイルを読み込んで一定間隔でデータを送り続ける
def send_data(conn, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            all_lines = f.read().splitlines()  # ✅ 修正：split("\n") ではなく read().splitlines() を使用

        for send_data in all_lines:
            if not send_data:
                continue  # 空行はスキップ
            else:
                send_dict=data_arrange(send_data) #dataをdict形式(json形式)に変換
            conn.sendall(json.dumps(send_dict).encode('utf-8'))  # ✅ 修正：str → bytes に変換
            print(f"[送信] {file_path}: {send_dict}")
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

