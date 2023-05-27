import cv2
import  time
import HandTrckingModule as htm
import numpy as np
import pysine
import asyncio


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def main():
    ##############

    wCam , hCam = 640, 480
    ###############
###################à audio OUT
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
    ################
    ############### audio in


    ###############à

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)


    detector = htm.handDetector( detectionCon=0.7)


    #volume.SetMasterVolumeLevel(-20.0, None)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainLoop(cap, detector, volume, minVol, maxVol))




async def mainLoop(cap, detector, volume, minVol, maxVol):
    pTime = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img, draw=False)
        lmList0 = detector.findPosition(img, draw=False, handNo=0)
        length0 = lengthMeasuere(img, lmList0, 0)
        volumeControl(length0, volume, minVol, maxVol)

        lmList1 = detector.findPosition(img, draw=False, handNo=1)
        length1 = lengthMeasuere(img, lmList1, 1)
        freq = length1*5
        if length1==-1:
            freq = 0
        await ring(freq)
        # task = asyncio.create_task(ring(freq))
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1,
                    (255, 0,0), 3)


        cv2.imshow('Img', img)
        cv2.waitKey(1)


async def ring(freq):
    #print(freq)
    pysine.sine(freq, 0.05)


def lengthMeasuere(img, lmList, handNo):
    if handNo==0:
        color = (255, 0, 0)
    else: color = (0, 255, 0)
    if len(lmList)!=0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), color, 5)
        cv2.circle(img, (cx, cy), 8, (255, 255, 255), cv2.FILLED)
        length= np.hypot(x2-x1, y2-y1)
        if length<50:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)
        return length
    else: return -1


def volumeControl(length, volume, minVol, maxVol):
    if length!=-1:
        vol=np.interp(length, [50, 230], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

if __name__ =="__main__":
    main()