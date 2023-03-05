import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key,Controller


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?']]
finalText = ""

keyboard = Controller()


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        if text=="<-":
            self.pos = pos
            self.size = [120,85]
            self.text = text
        elif text == "CapsLk":
            self.pos = pos
            self.size = [250, 85]
            self.text = text
        elif text == "enter":
            self.pos = pos
            self.size = [225, 85]
            self.text = text
        elif text == "":
            self.pos = pos
            self.size = [340, 85]
            self.text = text
        else:
            self.pos = pos
            self.size = size
            self.text = text



buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

buttonList.append(Button([50, 450], "<-"))
buttonList.append(Button([785, 450], "CapsLk"))
buttonList.append(Button([50, 550], "enter"))
buttonList.append(Button([700, 550], ""))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                # when clicked
                if l < 30:
                    if (button.text == "<-"):
                        keyboard.press(Key.backspace)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        keyboard.release(Key.backspace)
                        time.sleep(0.75)
                    elif (button.text == "CapsLk"):
                        keyboard.press(Key.caps_lock)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        keyboard.release(Key.caps_lock)
                        time.sleep(0.75)
                    elif (button.text == "enter"):
                        keyboard.press(Key.enter)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        keyboard.release(Key.enter)
                        time.sleep(0.75)
                    elif (button.text == ""):
                        keyboard.press(Key.space)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        keyboard.release(Key.space)
                        time.sleep(0.75)
                    else:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        time.sleep(0.75)

    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)
