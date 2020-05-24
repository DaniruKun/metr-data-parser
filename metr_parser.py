#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone
from dateutil.tz import tzlocal
import json
import os
import subprocess as s
import sys


if len(sys.argv) > 3:
    print('You have specified too many arguments')
    sys.exit()

if len(sys.argv) < 3:
    print('You need to specify the output file path')
    sys.exit()

input_path = sys.argv[1]
output_path = sys.argv[2]

# If remote location, like metr record e.g. https://metr.at/r/abcdef12 , fetch json automatically
if 'http' in input_path:
    resource = input_path if 'metr' not in input_path else input_path + '?format=json'
    s.run(['curl', resource, '--output', 'metr_raw_data.json'])
    print('Downloaded json data from remote.')
    input_path = 'metr_raw_data.json'


print(f"Loading data from file: {input_path}")

# Load input data from Metr
with open(input_path, 'r') as input_f:
    data = json.load(input_f)

print(f"Metr app version: {data['appver']} ")
print(f"Firmware version: {data['fw']}")

record_count = len(data['elapsed'])

new_data = []

start_time_utc = datetime.fromtimestamp(data['start'] // 1000, tz=timezone.utc)
start_time_local = datetime.fromtimestamp(data['start'] // 1000, tz=tzlocal())

for i in range(0, record_count):
    elapsed_delta = timedelta(days=0, hours=0, minutes=0, microseconds=data['elapsed'][i])
    current_time_utc = start_time_utc + elapsed_delta

    record = {
        'consumption': data['consumption'][i],
        'current': data['current'][i],
        'duty': data['duty'][i],
        'elapsed': data['elapsed'][i],
        'elapsedAh': data['elapsedAh'][i],
        'elapsedAhRegen': data['elapsedAhRegen'][i],
        'elapsedDistance': data['elapsedDistance'][i],
        'elapsedWh': data['elapsedWh'][i],
        "elapsedWhRegen": data['elapsedWhRegen'][i],
        'faultCode': data['faultCode'][i],
        'latitude': data['latitude'][i],
        'longitude': data['longitude'][i],
        'motorCurrent': data['motorCurrent'][i],
        'motorTemperature': data['motorTemperature'][i],
        'ppm': data['ppm'][i],
        'rpm': data['rpm'][i],
        'speed': data['speed'][i],
        'temperature': data['temperature'][i],
        'voltage': data['voltage'][i],
        'timestampUTC': current_time_utc.isoformat(),
        # Constants
        'ah': data['ah'],
        'ahRegen': data['ahRegen'],
        'distance': data['distance'],
        'duration': data['duration'],
        'os': data['os'],
        'wh': data['wh'],
        'whRegen': data['whRegen'],
    }
    # Optional data items
    if len(data['motorCurrent2']) > 0:
        record['motorCurrent2'] = data['motorCurrent2'][i]
    if len(data['motorCurrent3']) > 0:
        record['motorCurrent3'] = data['motorCurrent3'][i]
    if len(data['motorCurrent4']) > 0:
        record['motorCurrent4'] = data['motorCurrent4'][i]
    
    if len(data['motorTemperature2']) > 0:
        record['motorTemperature2'] = data['motorTemperature2'][i]
    if len(data['motorTemperature3']) > 0:
        record['motorTemperature3'] = data['motorTemperature3'][i]
    if len(data['motorTemperature4']) > 0:
        record['motorTemperature4'] = data['motorTemperature4'][i]
    
    if len(data['temperature2']) > 0:
        record['temperature2'] = data['temperature2'][i]
    if len(data['temperature3']) > 0:
        record['temperature3'] = data['temperature3'][i]
    if len(data['temperature4']) > 0:
        record['temperature4'] = data['temperature4'][i]
    
    if len(data['altitude']) > 0:
        record['altitude'] = data['altitude'][i]

    new_data.append(record)


with open(output_path, 'w') as out_f:
    out_f.write(json.dumps(new_data))
