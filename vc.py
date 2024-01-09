import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

cap = cv2.VideoCapture(1)  # Checks for camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

mpHands = mp.solutions.hands  # detects hand/finger
hands = mpHands.Hands()  # complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils

# To access the speaker through the pycaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)  # Corrected access to 'iid'
volume = cast(interface, POINTER(IAudioEndpointVolume))
volbar = 400
volper = 0

volMin, volMax = volume.GetVolumeRange()[:2]

while True:
    success, img = cap.read()  # If the camera works, capture an image

    if not success:
        print("Error: Could not read a frame from the camera.")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Collection of gesture information
    results = hands.process(imgRGB)  # completes the image processing.

    lmList = []  # empty list
    if results.multi_hand_landmarks:  # list of all hands detected.
        # By accessing the list, we can get the information of each hand's corresponding flag bit
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):  # adding counter and returning it
                # Get finger joint points
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])  # adding to the empty list 'lmList'
            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    if lmList != []:
        # getting the value at a point
        # x      #y
        x1, y1 = lmList[4][1], lmList[4][2]  # thumb
        x2, y2 = lmList[8][1], lmList[8][2]  # index finger
        # creating a circle at the tips of the thumb and index finger
        cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)  # image #fingers #radius #rgb
        cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)  # image #fingers #radius #rgb
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # create a line between the tips of the index finger and thumb

        length = hypot(x2 - x1, y2 - y1)  # distance between the tips using hypotenuse
        # from numpy, we find our length, by converting hand range in terms of volume range (between -63.5 to 0)
        vol = np.interp(length, [30, 350], [volMin, volMax])
        volbar = np.interp(length, [30, 350], [400, 150])
        volper = np.interp(length, [30, 350], [0, 100])

        print(vol, int(length))
        volume.SetMasterVolumeLevel(vol, None)

        # Hand range 30 - 350
        # Volume range -63.5 - 0.0
        # creating a volume bar for the volume level
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255),
                      4)  # vid ,initial position ,ending position ,rgb ,thickness
        cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)
        # tell the volume percentage ,location, font of text, length, rgb color, thickness
    cv2.imshow('Image', img)  # Show the video
    if cv2.waitKey(1) & 0xff == ord('q'):  # By using the spacebar delay will stop
        break

cap.release()  # stop the camera
cv2.destroyAllWindows()  # close the window
