import cv2
from cvzone.HandTrackingModule import HandDetector
import pydirectinput as pyd

detector = HandDetector(detectionCon = 0.8, maxHands=2)
video = cv2.VideoCapture(0)

while True:
    # open the web cam
    ret, frame = video.read()

    # find hand on the screen
    hands, image = detector.findHands(frame)
    # declare a rentagle on the screen
    cv2.rectangle(image, (0,480), (300,425), (96, 130, 182), -2)

    if hands:
        hand0 = hands[0]
        center = hand0["center"]
        # figure up information
        fingerUp = detector.fingersUp(hand0)
        print(center)

        # zero figures
        if fingerUp == [0, 0, 0, 0, 0]:
            cv2.putText(frame, 'Down', (110, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

        # three figures
        if fingerUp == [0, 1, 1, 1, 0]:
            cv2.putText(frame, 'Quit', (110, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            # quit
            pyd.press('esc')

        # five figures
        if fingerUp == [1, 1, 1, 1, 1]:
            cv2.putText(frame, 'Start or Jump', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            # jump
            pyd.press('SPACE')



    cv2.imshow("Frame", frame)

    # press q to close the window
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destoryAllWindows()
