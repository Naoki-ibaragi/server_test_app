import random
from datetime import datetime

SERIAL_MAX=10

def prepare_ld_tr(serial,unique):
    dict={}
    arm=["oku","temae"]
    dict["serial"]=serial
    dict["wano"]=random.randint(1,25)
    dict["wax"]=random.randint(1,30)
    dict["way"]=random.randint(1,30)
    dict["trayid"]="LD"+unique
    dict["trayarm"]=arm[random.randint(0,1)]
    dict["px"]=random.randint(1,18)
    dict["py"]=random.randint(1,18)
    dict["pax"]=random.randint(-99999,99999)
    dict["pay"]=random.randint(-99999,99999)
    dict["date"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return dict

def prepare_arm_count(serial):
    dict={}
    dict["serial"]=serial
    dict["count"]=random.randint(1,200000)

    return dict

def prepare_ph(serial):
    dict={}
    dict["serial"]=serial
    dict["ax"]=random.randint(-99999,99999)
    dict["ay"]=random.randint(-99999,99999)
    dict["at"]=random.randint(-99999,99999)

    return dict

def prepare_ts_pass(serial):
    dict={}
    dict["serial"]=serial
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

def prepare_ts_fail(serial):
    dict={}
    dict["serial"]=serial
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

def prepare_ts_ip(serial):
    dict={}
    dict["serial"]=serial
    dict["stage_count"]=random.randint(-99999,99999)

    return dict

def prepare_t1_ip(serial):
    dict={}
    dict["serial"]=serial
    dict["bin"]=random.randint(0,8)

    return dict

def prepare_t2_ip(serial):
    dict={}
    dict["serial"]=serial
    dict["bin"]=random.randint(0,8)

    return dict

def prepare_uld_pi(serial,unique):
    dict={}
    dict["serial"]=serial
    dict["trayid"]="ULD"+unique
    dict["px"]=random.randint(1,18)
    dict["py"]=random.randint(1,18)
    dict["pax"]=random.randint(-99999,99999)
    dict["pay"]=random.randint(-99999,99999)

    return dict
 
def prepare_uld_ci(serial):
    dict={}
    dict["serial"]=serial
    dict["px"]=random.randint(1,18)
    dict["py"]=random.randint(1,18)
    dict["cax"]=random.randint(-99999,99999)
    dict["cay"]=random.randint(-99999,99999)
    dict["date"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return dict

def prepare_alarm(serial):
    dict={}
    dict["alarm_num"]=random.randint(1,2)
    dict["serial"]=[serial]

    return dict