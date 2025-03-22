import cv2 as cv
import mediapipe as mp
import time

class handDetector:
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplexity,self.detectionCon, self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for self.handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, self.handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=False):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                #prining the landmarks pixel values(at waht position on the screen they are located)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if(draw):
                    cv.circle(img,(cx,cy),15,(255,0,255),cv.FILLED)
        return lmList
#helps to draw landmarks lines on the hand
def main():
    pTime=0
    cTime=0
    cap = cv.VideoCapture(0)
    detector=handDetector()
    while True:
        success, img = cap.read()
        img=detector.findHands(img)
        lmlist=detector.findPosition(img,draw=False)
        if(len(lmlist)!=0):
            print(lmlist)
        #gives the x,y,z coordinates of the hand
        #draws lines between landmarks
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv.putText(img,str(int(fps)),(10,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)       
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        cv.imshow("Image", img)

if __name__ == "__main__":
    main()

