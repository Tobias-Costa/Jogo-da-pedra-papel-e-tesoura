import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import random

def ensure_alpha_channel(img):
    if img.shape[2] == 3:  # Se a imagem tiver apenas 3 canais (RGB)
        alpha_channel = np.ones((img.shape[0], img.shape[1]), dtype=np.uint8) * 255  # Canal alfa totalmente opaco
        img = cv2.merge([img, alpha_channel])
    return img

detector = HandDetector(maxHands=1)
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

timer = 0
stateResult = False
startGame = False
scores = [0,0]

while True:
    imgBG = cv2.imread("assets/tigre_arena.png")
    sucess, img = cap.read()

    imgScaled = cv2.resize(img, (0,0), None, 0.8125, 0.8125)
    imgScaled = imgScaled[:,120:480]


    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (610,645), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,255), 3)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = "pedra"
                    if fingers == [1,1,1,1,1]:
                        playerMove = "papel"
                    if fingers == [0,1,1,0,0]:
                        playerMove = "tesoura"
                    
                    randomChoice = random.choice(['pedra', 'papel', 'tesoura'])
                    imgAI =  cv2.imread(f'assets/{randomChoice}.png', cv2.IMREAD_UNCHANGED)
                    imgAI = ensure_alpha_channel(imgAI)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (130,384))
                    
                    if (playerMove == 'pedra' and randomChoice == 'tesoura') or \
                            (playerMove == 'papel' and randomChoice == 'pedra') or \
                            (playerMove == 'tesoura' and randomChoice == 'papel'):
                        scores[1] += 1

                    if (playerMove == 'tesoura' and randomChoice == 'pedra') or \
                            (playerMove == 'pedra' and randomChoice == 'papel') or \
                            (playerMove == 'papel' and randomChoice == 'tesoura'):
                        scores[0] += 1


    imgBG[298:688,847:1207] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (130,384))

    cv2.putText(imgBG, str(scores[0]), (330,297), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 4)
    cv2.putText(imgBG, str(scores[1]), (1113,297), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 4)

    cv2.imshow("Pedra Papel Tesoura Fortune", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    if key==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
