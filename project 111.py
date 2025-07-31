import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np
import cvzone
from pynput.keyboard import Key, Controller
 
time1 = time.time()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)
 
detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Space", "Backspace"]]
finalText = ""
 
keyboard = Controller()
 
 
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
 
 
#def drawAll(img, buttonList):
#    imgNew = np.zeros_like(img, np.uint8)
#    for button in buttonList:
#        x, y = button.pos
#        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                          20, rt=0)
#        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                      (255, 0, 255), cv2.FILLED)
#        cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#    out = img.copy()
#    alpha = 0.5
#    mask = imgNew.astype(bool)
#    print(mask.shape)
#    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#    return out
 
 
class Button():
    def __init__(self, pos, text, size):
        self.pos = pos
        self.size = size
        self.text = text
 
 
buttonList = []
for i in range(len(keys)):
    marge = 0
    for j, key in enumerate(keys[i]):
        if key == 'Space':
            buttonList.append(Button([100 * j + 50+marge, 100 * i + 50], key, [225,85]))
            marge = 140
        elif key == 'Backspace':
            buttonList.append(Button([100 * j + 50+marge, 100 * i + 50], key, [375,85]))
        else:
            buttonList.append(Button([100 * j + 50+marge, 100 * i + 50], key, [85,85]))
 
while True:
    time2=time.time()

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
 
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
 
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)
 
                ## when clicked
                if l < 70 and time2-time1>0.3:
                    time1=time2
                    txt = button.text 
                    if button.text == "Space":
                        keyboard.press(' ')
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        finalText += ' '
                        keyboard.release(' ')
                        
                    elif button.text == "Backspace":
                
                        keyboard.press(Key.backspace)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        finalText = finalText[:-1]
                        keyboard.release(Key.backspace)
                        
                    else:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        finalText += button.text
                        keyboard.release(button.text)

 
    cv2.rectangle(img, (50, 350+100), (985+50, 450+100), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430+100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    
    if cv2.waitKey(1) & 0xFF == ord('c'):
        finalText = ''


    
    cv2.imshow("Image", img)
    cv2.waitKey(1)