import random
from datetime import datetime

SERIAL_MAX=10

def prepare_ld_tr():
    dict={}
    arm=["oku","temae"]
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["wano"]=random.randint(1,25)
    dict["wax"]=random.randint(1,30)
    dict["way"]=random.randint(1,30)
    dict["trayid"]="tray"+str(random.randint(1000000000,9999999999))
    dict["trayarm"]=arm[random.randint(0,1)]
    dict["px"]=random.randint(1,18)
    dict["py"]=random.randint(1,18)
    dict["pax"]=random.randint(-99999,99999)
    dict["pay"]=random.randint(-99999,99999)
    dict["date"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return dict

def prepare_arm_count():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["count"]=random.randint(1,200000)

    return dict

def prepare_ph():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["ax"]=random.randint(-99999,99999)
    dict["ay"]=random.randint(-99999,99999)
    dict["at"]=random.randint(-99999,99999)

    return dict

def prepare_ts_pass():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["probe_serial"]="PROBE_"+"%2d"%random.randint(1,100)
    dict["probe_count"]=random.randint(1,10000)
    dict["probe_x1"]=random.randint(0,1000000)
    dict["probe_y1"]=random.randint(0,1000000)
    dict["probe_x2"]=random.randint(0,1000000)
    dict["probe_y2"]=random.randint(0,1000000)
    dict["stage_serial"]="STAGE_"+"%2d"%random.randint(1,100)
    dict["stage_count"]=random.randint(1,10000)
    dict["stage_z"]=random.randint(0,1000000)
    dict["pin_z"]=random.randint(0,1000000)
    dict["ax"]=random.randint(-99999,99999)
    dict["ay"]=random.randint(-99999,99999)
    dict["at"]=random.randint(-99999,99999)
    dict["bin"]=random.randint(0,8)

    return dict

def prepare_ts_fail():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["probe_serial"]=None
    dict["probe_count"]=None
    dict["probe_x1"]=None
    dict["probe_y1"]=None
    dict["probe_x2"]=None
    dict["probe_y2"]=None
    dict["stage_serial"]=None
    dict["stage_count"]=None
    dict["stage_z"]=None
    dict["pin_z"]=None
    dict["ax"]=random.randint(-99999,99999)
    dict["ay"]=random.randint(-99999,99999)
    dict["at"]=random.randint(-99999,99999)
    dict["bin"]=None

    return dict

def prepare_ts_ip():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["stage_count"]=random.randint(-99999,99999)

    return dict

def prepare_t1_ip():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["bin"]=random.randint(0,8)

    return dict

def prepare_t2_ip():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["bin"]=random.randint(0,8)

    return dict

def prepare_uld_pi():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["trayid"]="tray"+str(random.randint(1000000000,9999999999))
    dict["px"]=random.randint(1,18)
    dict["py"]=random.randint(1,18)
    dict["pax"]=random.randint(-99999,99999)
    dict["pay"]=random.randint(-99999,99999)

    return dict
 
def prepare_uld_ci():
    dict={}
    dict["serial"]=random.randint(1,SERIAL_MAX)
    dict["px"]=random.randint(1,18)
    dict["py"]=random.randint(1,18)
    dict["cax"]=random.randint(-99999,99999)
    dict["cay"]=random.randint(-99999,99999)
    dict["date"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return dict

def prepare_alarm():
    dict={}
    dict["alarm_num"]=random.randint(400,800)
    dict["serial"]=make_serial_list(6)

    return dict

def make_serial_list(num):
    lis=[]
    for i in range(num):
        n=random.randint(0,1)
        serial=n*random.randint(1,SERIAL_MAX)
        lis.append(serial)
    return lis