import cv2 as cv
import numpy as np
import mediapipe as mp
import handtrackingmodule as htm
import time

ctime=0
pTime=0
cap = cv.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)
expression=""
tip=[4,8,12,16,20]
lastTime = time.time() 
delay = 2
result=0
resultTime = 0
displayDuration = 5
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        fingers=[]
        if(lmList[tip[0]][1]<lmList[tip[0]-1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        for i in range(1,5):
            if(lmList[tip[i]][2]<lmList[tip[i]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        

        currentTime = time.time()
        if currentTime - lastTime > delay: 
            if fingers == [0, 1, 0, 0, 0]:
                expression += "1"
            elif fingers == [0, 1, 1, 0, 0]:
                expression += "2"
            elif fingers == [0, 1, 1, 1, 0]:
                expression += "3"
            elif fingers == [0, 1, 1, 1, 1]:
                expression += "4"
            elif fingers == [1, 1, 1, 1, 1]:
                expression += "5"
            elif fingers == [1, 0, 0, 0, 0]:
                expression += "6"
            elif fingers == [1, 1, 0, 0, 0]:
                expression += "7"
            elif fingers == [1, 1, 1, 0, 0]:
                expression += "8"
            elif fingers == [1, 1, 1, 1, 0]:
                expression += "9"
            elif fingers == [0, 0, 0, 0, 1]:
                expression += "0"
            elif fingers == [0, 0, 1, 1, 0]:
                expression += "="
            elif fingers == [1, 1, 0, 0, 1]:
                expression += "+"
            elif fingers == [0, 1, 0, 0, 1]:
                expression += "-"
            elif fingers == [1, 0, 0, 0, 1]:
                expression += "/"
            elif fingers == [1, 0, 0, 1, 1]:
                expression += "*"
            
            lastTime = currentTime
        
    cv.putText(img,expression,(100,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)   
    if "=" in expression and resultTime is None:
        try:
            expression = expression.strip("=")
            result = eval(expression)  # Evaluate the expression
            resultTime = time.time()  # Start result display timer # Clear expression for next input
        except:
            result = "Error"
            resultTime = time.time()

    if resultTime is not None:
        cv.putText(img,f"Result:{str(result)}", (100,100), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        if time.time() - resultTime > displayDuration:
            result = None 
            resultTime = None
            expression = "" 



            
        


        


    
    ctime=time.time()
    fps=1/(ctime-pTime)
    pTime=ctime
    cv.putText(img,str(int(fps)),(10,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv.imshow("Image",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release() 
cv.destroyAllWindows()
