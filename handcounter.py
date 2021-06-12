import cv2
import time
import os
import handtrackingmodule as htm

Wcam,hcam = 640,480
cap  = cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,hcam)
folder = 'fing'
mylist = os.listdir(folder)
print(mylist)
overlayList = []
pTime =0


# for imgpath in mylist:
#     image = cv2.imread(f'{folder}/{imgpath}')
#     image = cv2.resize(image,(200,200))
#     overlayList.append(image)
# print(len(overlayList))

detector = htm.handDetector(detectionCon=0.8)
tipIds = [4,8,12,16,20]

while True:
    Success,img = cap.read()
    img = detector.findhands(img,draw=False)
    lmlist = detector.findposition(img,draw=False)
    # print(lmlist)
    if len(lmlist) !=0:
        finger = []
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0]-1][1]:
            finger.append(1)
        else:
            finger.append(0)
        # if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1] and lmlist[tipIds[4]][2] > lmlist[tipIds[4] - 2][2] :
        #     finger.append(1)
        # else:
        #     finger.append(0)

        for i in range(1,5):
            if lmlist[tipIds[i]][2] < lmlist[tipIds[i]-2][2]: # lmlist contain 20 points of fingers, tipId
                finger.append(1)
            else:
                finger.append(0)
        print(finger)

        totalFinger = finger.count(1)
        # print(totalFinger)
        cv2.rectangle(img,(20,320),(100,400),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFinger),(45,375),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),5)

        # h,w,c = overlayList[totalFinger-1].shape
        # img[0:h,0:w] = overlayList[totalFinger-1]
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS : {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
    cv2.imshow("Image",img)
    cv2.waitKey(1)

