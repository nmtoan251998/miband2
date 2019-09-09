import sys
import time
import argparse
import requests
import json
import csv
from pathlib import Path
from datetime import datetime
from time import sleep
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

fitness_data = []
path_to_file = '../../assets/data/'
file_name_to_save_to_db = MAC + time.strftime("_%d_%m_%Y")

if  args.init:
    if band.initialize():
        print("Init OK")
    band.set_heart_monitor_sleep_support(enabled=False)
    band.disconnect()
    sys.exit(0)
else:
    band.authenticate()

def writeRealtimeData(heartrate):    

    data = {
        'heart_rate': heartrate,
        'steps': band.get_steps()['steps'],
        'fat_gramms': band.get_steps()['fat_gramms'],
        'meters': band.get_steps()['meters'],
        'callories': band.get_steps()['callories'],
        'time': time.strftime("%H:%M:%S")    
    }            

    with open(path_to_file + 'python_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    # data to backup and saved to database later
    fitness_data.append(data)
    with open(path_to_file + file_name_to_save_to_db + '.json', 'w') as json_file:
        json.dump(fitness_data, json_file, indent=4)    

    # this print is required to flush data to nodejs server
    print(data)

def l(x):
    print ('Heart rate:', x)

def b(x):
    print ('Raw heart:', x)
    
def f(x):
    print ('Raw accel heart:', x)

if args.live:
    band.send_alert(ALERT_TYPES.MESSAGE)

    # read old data
    try:
        f = open(path_to_file + file_name_to_save_to_db + '.json', 'r')
        old_data = json.loads(f.read())
        fitness_data = old_data
        f.close()
    except IOError:
        print('Created new data file')
    
    band.start_raw_data_realtime(
            heart_measure_callback=writeRealtimeData,
            heart_raw_callback=b,
            accel_raw_callback=f)

band.disconnect()
