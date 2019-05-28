import subprocess
import time
import math
import os
import datetime
import numpy as np 
#stores bssid and signal information
wifiDict={}
import json
import requests

#stores bssid and corresponding channels
channeldict={}

#dict for channel to freq conversion
Channels={1: 2412,2: 2417,3: 2422,4: 2427,5: 2432,6: 2437,7: 2442,
          8: 2447,9: 2452,10: 2457,11: 2462,12: 2467,13: 2472,14: 2484,
          131: 3657.5,133: 3665.0,134: 3670.0,135: 3677.0,137: 3687.5,
          138: 3690.0,36: 5180,40: 5200,44: 5220,48: 5240,52: 5260,56: 5280,
          60: 5300,64: 5320,100: 5500,104: 5520,108: 5540,112: 5560,116: 5580,
          120: 5600,124: 5620,128: 5640,132: 5660,136: 5680,140: 5700,149: 5745,
          153: 5765,157: 5785,161: 5805,165: 5825}


#scans all access points
def scanwifi():
    results = subprocess.check_output(["netsh", "wlan", "show", "network","mode=BSSID"])
    results = results.decode("utf-8") # needed in python 3
    results = results.replace("\r","")
    ls = results.split("\n")
    ls = ls[3:]
    return ls

#function to turn signal strength to dbm reading
def dbmcalc(quality):
    if type(quality)==str:
        print(quality)
        quality=float(quality.replace('%',''))
    dbm=(139.86-quality)*(58/79)
    print(dbm)
    if quality>=95:
        dbm+=1
    elif quality>=90:
        dbm+=2
    return dbm*-1
 
#loop through AP list only use certain ssidd details
def scanthem(ls,friendlywifi=''):
    for i in range(len(ls)):
        #print(i)
        detail=ls[i].strip()
        if detail=="" or detail=='':
            #print("Skip")
            pass
        elif detail[:4]=='SSID':
            try:
                ssid=detail.split(" : ")[1]
            except Exception as e:
                ssid="HIDDEN"#used in the case where the ssid name is hidden
            if ssid==friendlywifi or friendlywifi=='':
                sidchk=True
            else:
                sidchk=False
            #print("SSID",ssid)
        elif detail[:4]=='BSSI':
            bssid=detail.split(" : ")[1]
            
            #print("BSSID",bssid)
        elif detail[:4]=='Sign':
            signal=detail.split(" : ")[1]
            if bssid in wifiDict.keys() and sidchk==True:
                signal=signal.replace('%','')
                wifiDict[bssid].append(float(signal))
            elif sidchk==False:
                pass
            else:
                signal=signal.replace('%','')
                wifiDict[bssid]=[float(signal)]
            #print("Signal",signal)
        elif detail[:4]=='Chan':
            channel=detail.split(" : ")[1]
            if bssid in channeldict.keys() and sidchk==True:
                channeldict[bssid]=channel
            elif sidchk==False:
                pass
            else:
                channeldict[bssid]=channel
                
def Average(lst): 
    return sum(lst) / len(lst)

#path loss formula to calc dist(needs improvement)
def dist(freq,RSSI):
    exp=(27.55-(20*math.log10(freq)-math.fabs(RSSI)))/20.0
    distance= math.pow(10.0,exp)
    distance=str(round(distance,3))
    return distance

#prints details as string
def toString(distance,freq,RSSI):
    return " Distance %sm  with Frequency %d Mhz and RSSI %d dBm" %(distance,freq,RSSI)

def makedata():#calculates distances to each AP saved in dictionary
    JSONLIST=[]
    for wifi,signal in wifiDict.items():#try catch
        freq=Channels[int(channeldict[wifi])]
        percentsignal=Average(signal[1:])
        wifiDict[wifi]=[100]
        rssi=round(dbmcalc(percentsignal))
        distance=dist(freq,rssi)
        #make into json/ send to server
        details=toString(distance,freq,rssi)
        print(details)
        detailList=[wifi,freq,rssi,percentsignal]#could change to dict/json etc
        #print(detailList)
        jsondict={'mac':wifi,'frequency':freq,'rssi':rssi,'distance':distance,'percentage':percentsignal}
        print(jsondict)
        JSONLIST.append(jsondict)
    
    return JSONLIST
        
def run(friendlywifi):
    if friendlywifi=='':
        print("Using all available wifi")
    '''else:
        try:
            output = subprocess.check_output(["netsh", "wlan", "connect", friendlywifi])
            print(output)
        except Exception as e:
            print ("Wifi AP not found, or error connecting to AP",e)
       '''     #friendlywifi=''#implement loop to try again
    #input friendly wifi ssid name
    #scan,calculate distances and send to server
    delay=time.time()+10#runs scan for +x seconds to get average wifi strength
    while time.time()<delay:
        print("Scanning APs, please wait")
        ls=scanwifi()
        #print(ls)
        scanthem(ls,friendlywifi)
        time.sleep(2)#infinite while loop until variable from server is true, then scan instantly, otherwise sleep for set time
        #waits for (x) seconds before running again
    #print(wifiDict)
    #print(channeldict)
    
    jsondata=makedata()
    print(jsondata)
    #wifiDict={}
    #print(json.dump(jsondata))
    send(jsondata)
    #time.sleep(20)

def send(dat):
    scantime=datetime.datetime.now().strftime('%H:%M:%S')
    
    datatosend={'scantime':scantime,'data':str(dat)}
    que=str(datatosend)
    print(que)
    r = requests.get("https://andoird-device-locator-tigerflower.c9users.io/api/data", data=datatosend)
    print(r.status_code, r.reason)


    
if __name__=="__main__":
    friendlywifi=input("Please enter friendly wifi name\n")
    startscan=True
    try:
        while startscan:
            run(friendlywifi)
    #run(friendlywifi)
    #wifiDict={}
    except KeyboardInterrupt:
        startscan=False
    
            
