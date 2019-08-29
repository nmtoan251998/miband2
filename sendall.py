import sys
import time
import argparse
import requests
from datetime import datetime
from base import MiBand2
from constants import ALERT_TYPES

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--live',  action='store_true',help='Measures live heart rate')
parser.add_argument('-i', '--init',  action='store_true',help='Initializes the device')
parser.add_argument('-m', '--mac', required=True, help='Mac address of the device')

args = parser.parse_args()

MAC = args.mac # sys.argv[1]

band = MiBand2(MAC, debug=True)
band.setSecurityLevel(level="medium")

if  args.init:
    if band.initialize():
        print("Init OK")
    band.set_heart_monitor_sleep_support(enabled=False)
    band.disconnect()
    sys.exit(0)
else:
    band.authenticate()

def sendHeartrateDataToServer(heartrate):    
    data = {
        'heart_rate': heartrate,
        'steps': band.get_steps()['steps'],
        'fat_gramms': band.get_steps()['fat_gramms'],
        'meters': band.get_steps()['meters'],
        'callories': band.get_steps()['callories']
    }        
    serverURL = "http://localhost:5000/data/live"
    requests.post(serverURL, json = data)

def l(x):
    print ('Heart rate:', x)

def b(x):
    print ('Raw heart:', x)


def f(x):
    print ('Raw accel heart:', x)

if args.live:    
    band.send_alert(ALERT_TYPES.MESSAGE)
    
    band.start_raw_data_realtime(
            heart_measure_callback=sendHeartrateDataToServer,
            heart_raw_callback=b,
            accel_raw_callback=f)

band.disconnect()




POST /data/live 200 0.316 ms - 3
{ heart_rate: 119, steps: 1268, fat_gramms: 4, meters: 796, callories: 25 }

POST /data/live 200 0.935 ms - 3
{ heart_rate: 118, steps: 1279, fat_gramms: 4, meters: 796, callories: 25 }

POST /data/live 200 0.828 ms - 3
{ heart_rate: 116, steps: 1281, fat_gramms: 5, meters: 796, callories: 25 }

POST /data/live 200 0.821 ms - 3
{ heart_rate: 115, steps: 1285, fat_gramms: 5, meters: 833, callories: 26 }

POST /data/live 200 0.836 ms - 3
{ heart_rate: 114, steps: 1287, fat_gramms: 5, meters: 833, callories: 26 }

POST /data/live 200 0.297 ms - 3
{ heart_rate: 112, steps: 1288, fat_gramms: 5, meters: 833, callories: 26 }