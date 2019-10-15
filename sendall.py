import sys
import time
import argparse
import json
from datetime import datetime
from time import sleep
from base import MiBand2
from constants import ALERT_TYPES

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--diagnose',  action='store_true', help='Diagnose heart rate with AI')
parser.add_argument('-l', '--live',  action='store_true', help='Measures live heart rate')
parser.add_argument('-i', '--init',  action='store_true', help='Initializes the device')
parser.add_argument('-m', '--mac', required=True, help='Mac address of the device')

args = parser.parse_args()

MAC = args.mac # sys.argv[1]

band = MiBand2(MAC, debug=True)
band.setSecurityLevel(level="medium")

fitness_data = []

is_request_sent_once = False

path_to_file = '../../assets/data/'
file_name_to_save_to_db = MAC + time.strftime("_%d_%m_%Y")

cal_avg_heart_rate = []
cal_avg_steps = []
cal_avg_callories = []
cal_avg_meters = []
cal_avg_fat_grams = []

if  args.init:
    if band.initialize():
        print("Init OK")
    band.set_heart_monitor_sleep_support(enabled=False)
    band.disconnect()
    sys.exit(0)
else:
    band.authenticate()

def writeConnectingDeviceInfo():
    device_info = {
        'mac': MAC,
        'serial': str(band.get_serial()),
        'software_revision': str(band.get_revision()),
        'hardware_revision': str(band.get_hrdw_revision()),
        'connection_time': time.strftime("%d/%m/%Y, %H:%M:%S"),
    }

    with open(path_to_file + MAC +'_device_data.json', 'w') as json_file:
        json.dump(device_info, json_file, indent=4)


def withDiagnose(heartrate):
    global is_request_sent_once
    global cal_avg_heart_rate
    global cal_avg_steps
    global cal_avg_callories
    global cal_avg_meters
    global cal_avg_fat_grams    

    # if request is not sent any time before, save the BLE device information to file for further purpose
    if is_request_sent_once == False:
        writeConnectingDeviceInfo()
        is_request_sent_once = True    
    
    # this is useful for diagnosing heart rate status
    data = {
        'heart_rate': heartrate,
        'steps': band.get_steps()['steps'],
        'fat_gramms': band.get_steps()['fat_gramms'],
        'meters': band.get_steps()['meters'],
        'callories': band.get_steps()['callories'],
        'time': time.strftime("%H:%M:%S"),
    }
    
    # append exist data from file if exist
    fitness_data.append(data)  
    with open(path_to_file +'diagnose/' +file_name_to_save_to_db +'.json', 'w') as json_file:
        json.dump(fitness_data, json_file, indent=4)        
                    
    current_milli_time = lambda: int(round(time.time() * 1000))
    realtime_data = {
        'heart_rate': heartrate,
        'steps': band.get_steps()['steps'],
        'fat_gramms': band.get_steps()['fat_gramms'],
        'meters': band.get_steps()['meters'],
        'callories': band.get_steps()['callories'],
        'time': current_milli_time(),
        'battery_level': band.get_battery_info()['level'],
        'battery_status': band.get_battery_info()['status'],
    }
    # flush data out to nodejs pipe
    print (realtime_data)

def withoutDiagnose(heartrate):
    global is_request_sent_once
    global cal_avg_heart_rate
    global cal_avg_steps
    global cal_avg_callories
    global cal_avg_meters
    global cal_avg_fat_grams    

    # if request is not sent any time before, save the BLE device information to file for further purpose
    if is_request_sent_once == False:
        writeConnectingDeviceInfo()
        is_request_sent_once = True    
    
    current_milli_time = lambda: int(round(time.time() * 1000))
    realtime_data = {
        'heart_rate': heartrate,
        'steps': band.get_steps()['steps'],
        'fat_gramms': band.get_steps()['fat_gramms'],
        'meters': band.get_steps()['meters'],
        'callories': band.get_steps()['callories'],
        'time': current_milli_time(),
        'battery_level': band.get_battery_info()['level'],
        'battery_status': band.get_battery_info()['status'],
    }
    # flush data out to nodejs pipe
    print (realtime_data)

def l(x):
    print ('Heart rate:', x)

def b(x):
    print ('Raw heart:', x)
    
def f(x):
    print ('Raw accel heart:', x)

if args.live:
    band.send_alert(ALERT_TYPES.MESSAGE)
    
    # read exist data from file, pass to a global array if data exist
    try:
        f = open(path_to_file +'diagnose/' +file_name_to_save_to_db + '.json', 'r+')        
        old_data = json.loads(f.read())
        fitness_data = old_data        
        f.close()
    except IOError:        
        print (IOError)
        pass
            
    if args.diagnose:
        band.start_raw_data_realtime(
                heart_measure_callback=withDiagnose,
                heart_raw_callback=b,
                accel_raw_callback=f)
    else:
        band.start_raw_data_realtime(
                heart_measure_callback=withoutDiagnose,
                heart_raw_callback=b,
                accel_raw_callback=f)


band.disconnect()
