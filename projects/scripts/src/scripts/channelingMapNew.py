import math
from typing import List
from datetime import datetime
import requests
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import shutil
import pathlib

rangeDeg=4
#pPA must be odd (1<)
pixelPerAxis=41
degPerMove=rangeDeg/(pixelPerAxis-1)
i=0
j=0
k=0
l=1
runTime=20
moveSleep=5
chnlMinA=155
chnlMaxA=165
chnlMinB=300
chnlMaxB=450
PulserMinA=1500
PulserMaxA=1600
PulserMinB=1500
PulserMaxB=1650
maxCharge=100

now = datetime.now()
dateTime=str(now.strftime("%Y-%m-%d_%H-%M-%S"))


def degAxis(x):
    if x==1:
        return(16000,"D")
    elif x==3:
        return(-16000,"D")
    elif x==0:
        return(-48470,"E")
    elif x==2:
        return(48470,"E")
    else:
        return("error not a valid argument",str(x))
        
def get_json(url):
    return requests.get(url, timeout=10).json()


def post_dictionary(url, data):
    response = requests.post(url, json=data, timeout=10)
    return response.status_code, response.text


def wait_for_request_done(url, request):
    while True:
        time.sleep(0.2)
        response = get_json(url)
        error_message = response["error"]
        if error_message == "Success" or error_message == "No error" or error_message == "The operation completed successfully":
            #if response['request_finished'] and response["request_id"] == str(request["request_id"]):
            if response['request_finished']:
                break
        else:
            print(error_message)
            raise ValueError('error_message')


def post_request(url, request):
    post_dictionary(url, request)
    wait_for_request_done(url, request)


def convert_string_to_list(raw_data: str):
    raw_data = raw_data.split(";")
    raw_data.pop()
    data = [int(x) for x in raw_data]
    return data


def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data
    
def waitForCharge(maxCharge):
    post_request("http://127.0.0.1:22200/api/latest", {"clear_accumulated_charge": True})
    currCharge=0
    start_time = time.time()
    while currCharge<maxCharge:
        time.sleep(2)
        response = requests.get("http://127.0.0.1:22200/api/latest").json()
        currCharge= float(response["accumulated_charge(nC)"])
        print(currCharge)   
    end_time = time.time()
    timeElapsed=end_time-start_time
    return currCharge, timeElapsed

class Graph:
    def __init__(self):
        title_string = "My histogram"
        self.fig = plt.figure(title_string)
        self.title_text = plt.figtext(0.20, 0.94, title_string, size='x-large', color='blue')
        ax_size = [0.11, 0.20, 1-0.140, 1-0.27] # [left, bottom, width, height] as fractions of figure width and height.
        self.axes = self.fig.add_axes(ax_size)
        self.reset_axes()
        self.pause = False

    def set_play_pause(self, animation):
        self.pause = not self.pause
        if self.pause:
            animation.pause()
        else:
            animation.resume()

    def reset_axes(self):
        self.axes.clear()
        self.axes.set_xlabel("Energy Level")
        self.axes.set_ylabel("Occurrence")
        self.axes.grid(which='both')
        self.axes.yaxis.set_ticks_position('left')
        self.axes.xaxis.set_ticks_position('bottom')
        # self.axes.xaxis_date()
        # self.axes.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        # self.axes.xaxis.set_major_locator(ticker.AutoLocator())

    def consume_data(self, data):
        self.reset_axes()
        self.axes.plot(data)

    def get_data(self):
        while True:
            histogram = requests.get("http://127.0.0.1:22300/api/latest/histogram/218/0").text
            histogram_list = convert_string_to_list(histogram)
            packed_list = pack(histogram_list, 0, 8192, 2048)
            yield packed_list
            yield packed_list




maxMoves=(pixelPerAxis**2)-1

moves=[]

while len(moves)<maxMoves:
    

    for x in range(l):
        if len(moves)>=maxMoves:
            break
        moves.append(k)
        print(k)
    k+=1
    
    for x in range(l):
        if len(moves)>=maxMoves:
            break
        moves.append(k)
        print(k)
    k+=1
    
    if k==4:
        k=0
    l+=1
print(len(moves))
print(maxMoves)

f = open("Map.dat", "w+")
f.write("X Y DetA DetB ElapsedTime(s) PulserA PulserB NormalisedA NormalisedB Charge(nC)")
f.write("\n")

#Turn on Current measurements
post_request("http://127.0.0.1:22200/api/latest", {"measure_current": True})
time.sleep(0.5)

post_request("http://127.0.0.1:22300/api/latest", {"request_id": "clear", "clear": True})
time.sleep(1)
post_request("http://127.0.0.1:22300/api/latest", {"request_id": "start", "start": True})
print("collect first point")

startTime=time.time()

chargeInfo=waitForCharge(maxCharge)
    
requests.post("http://127.0.0.1:22300/api/latest", json={"stop": True})

endTime=time.time()
elapsedTime=endTime-startTime

#Turn off Current measurements
time.sleep(0.5)
post_request("http://127.0.0.1:22200/api/latest", {"measure_current": False})

histogramA = requests.get("http://127.0.0.1:22300/api/latest/histogram/218/0").text
histogram_listA = convert_string_to_list(histogramA)
#packed_listA = pack(histogram_listA, 0, 8192, 1024)

histogramB = requests.get("http://127.0.0.1:22300/api/latest/histogram/218/1").text
histogram_listB = convert_string_to_list(histogramB)
#packed_listB = pack(histogram_listB, 0, 8192, 1024)

currPos=[0,0]

totalA=0
totalB=0
channel=0
PulserTotalA=0
PulserTotalB=0
for item in histogram_listA:
    if chnlMinA<channel and chnlMaxA>channel:
        #print(item)
        totalA+=item
    elif PulserMinA<channel and PulserMaxA>channel:
        PulserTotalA+=item
    channel+=1
channel=0
for item in histogram_listB:
    if chnlMinB<channel and chnlMaxB>channel:
        #print(item)
        totalB+=item
    elif PulserMinB<channel and PulserMaxB>channel:
        PulserTotalB+=item
    channel+=1
    
    
pulserFreqA=PulserTotalA/elapsedTime
pulserFreqB=PulserTotalB/elapsedTime

if pulserFreqA==0:
    normalisedA=0
else:
    normalisedA=(495*totalA)/(pulserFreqA*chargeInfo[0])
if pulserFreqB==0:
    normalisedB=0
else:
    normalisedB=(495*totalB)/(pulserFreqB*chargeInfo[0])
    
f.write(str(currPos[0])+" "+str(currPos[1])+" "+str(totalA)+" "+str(totalB)+" "+str(elapsedTime))
f.write(" "+str(PulserTotalA)+" "+str(PulserTotalB)+" "+str(normalisedA)+" "+str(normalisedB)+" "+str(chargeInfo[0]))
f.write("\n")

f.close()

filepath=pathlib.Path().resolve()
newpath=str(filepath)+"\Spectra"+str(dateTime)

if not os.path.exists(newpath):
    os.makedirs(newpath)

fa = open(newpath+"\\"+"DetA"+str(currPos[0])+"_"+str(currPos[1])+".dat", "w+")


i=0
for item in histogram_listA:
    fa.write(str(i)+" "+str(item))
    fa.write("\n")
    i+=1
    if i>16384:
        break
 
fa.close()
fb = open(newpath+"\\"+"DetB"+str(currPos[0])+"_"+str(currPos[1])+".dat", "w+")   
i=0
for item in histogram_listB:
    fb.write(str(i)+" "+str(item))
    fb.write("\n")
    i+=1
    if i>16384:
        break
fb.close()

counter=1

for moveCode in moves:
    
    counter+=1

    if moveCode==0:
        currPos[1]+=degPerMove
    elif moveCode==1:
        currPos[0]+=degPerMove
    elif moveCode==2:
        currPos[1]+=-degPerMove
    elif moveCode==3:
        currPos[0]+=-degPerMove
    else:
        print("error not a valid argument :"+str(moveCode))
        break
             
    #Move
    print("Next Move")
    response = requests.get("http://127.0.0.1:22100/api/latest").json()
    print(response["axes"][degAxis(moveCode)[1]]["step_counter"])

    nextMove=degPerMove*degAxis(moveCode)[0]
    
    print(degAxis(moveCode)[1])
    print("moving "+str(nextMove)+" steps")

    request={"request_id" : "move_motor", "move_motor_relative" : {"axis":degAxis(moveCode)[1], "value": nextMove}}
    post_request("http://127.0.0.1:22100/api/latest", request)
    time.sleep(moveSleep)

    print("move complete")
    response = requests.get("http://127.0.0.1:22100/api/latest").json()
    print(response["axes"][degAxis(moveCode)[1]]["step_counter"])
    
    #Turn on Current measurements
    post_request("http://127.0.0.1:22200/api/latest", {"measure_current": True})
    time.sleep(0.5)
    
    #Collect
    post_request("http://127.0.0.1:22300/api/latest", {"request_id": "clear", "clear": True})
    time.sleep(1)
    post_request("http://127.0.0.1:22300/api/latest", {"request_id": "start", "start": True})
    print("collect next point")

    startTime=time.time()
    
    

    chargeInfo=waitForCharge(maxCharge)
        
    requests.post("http://127.0.0.1:22300/api/latest", json={"stop": True})
    

    endTime=time.time()
    elapsedTime=endTime-startTime
    
    #Turn off Current measurements
    time.sleep(0.5)
    post_request("http://127.0.0.1:22200/api/latest", {"measure_current": False})
    
    #Obtain data
    histogramA = requests.get("http://127.0.0.1:22300/api/latest/histogram/218/0").text
    histogram_listA = convert_string_to_list(histogramA)
    #packed_listA = pack(histogram_listA, 0, 8192, 1024)
    
    histogramB = requests.get("http://127.0.0.1:22300/api/latest/histogram/218/1").text
    histogram_listB = convert_string_to_list(histogramB)
    #packed_listB = pack(histogram_listB, 0, 8192, 1024)
    
    totalA=0
    totalB=0
    channel=0
    PulserTotalA=0
    PulserTotalB=0
    for item in histogram_listA:
        if chnlMinA<channel and chnlMaxA>channel:
            #print(item)
            totalA+=item
        elif PulserMinA<channel and PulserMaxA>channel:
            PulserTotalA+=item
            
        channel+=1
    channel=0
    for item in histogram_listB:
        if chnlMinB<channel and chnlMaxB>channel:
            #print(item)
            totalB+=item
        elif PulserMinB<channel and PulserMaxB>channel:
            PulserTotalB+=item
        channel+=1
    
    
    #Saving data to file
    f = open("Map.dat", "a")
    
    pulserFreqA=PulserTotalA/elapsedTime
    pulserFreqB=PulserTotalB/elapsedTime
    
    if pulserFreqA==0:
        normalisedA=0
    else:
        normalisedA=(495*totalA)/(pulserFreqA*chargeInfo[0])
    if pulserFreqB==0:
        normalisedB=0
    else:
        normalisedB=(495*totalB)/(pulserFreqB*chargeInfo[0])
    
    f.write(str(currPos[0])+" "+str(currPos[1])+" "+str(totalA)+" "+str(totalB)+" "+str(elapsedTime))
    f.write(" "+str(PulserTotalA)+" "+str(PulserTotalB)+" "+str(normalisedA)+" "+str(normalisedB)+" "+str(chargeInfo[0]))
    f.write("\n")
    
    f.close()
    
    fa = open(newpath+"\\"+"DetA"+str(currPos[0])+"_"+str(currPos[1])+".dat", "w+")
    
    
    i=0
    for item in histogram_listA:
        fa.write(str(i)+" "+str(item))
        fa.write("\n")
        i+=1
        if i>16384:
            break
     
    fa.close()
    fb = open(newpath+"\\"+"DetB"+str(currPos[0])+"_"+str(currPos[1])+".dat", "w+")   
    i=0
    for item in histogram_listB:
        fb.write(str(i)+" "+str(item))
        fb.write("\n")
        i+=1
        if i>16384:
            break
    fb.close()
    
    timeLeft=((moveSleep+runTime)/60)*((len(moves)+1)-counter)
    
    timeLeft=round(timeLeft,1)
    
    print(str(counter)+"/"+str(len(moves)+1)+" pixels completed")
    print("~ "+str(timeLeft)+" mins remaining")






