import requests
import datetime
import time

while True:
    value1 = requests.get("http://169.254.150.150/hive/api/rbs/caen/histogram/10664-0/pack-2400-2801-1").json()
    value2 = requests.get("http://169.254.150.150/hive/api/rbs/caen/histogram/10664-0/pack-3600-4401-1").json()
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    logline = timestamp + ", " + str(value1[0]) + ", " + str(value2[0]) + "\n"
    time.sleep(1)
    with open("data.txt", 'a') as f:
        f.write(logline)
