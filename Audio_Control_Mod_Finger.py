from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import msvcrt  # Windows-specific module to capture key events
import cv2
import mediapipe as mp
import numpy as np
import math

# Get the current master volume as a scalar (0.0 to 1.0)
#current_volume_scalar = volume.GetMasterVolumeLevelScalar()
#print(f"Current Volume (Scalar): {current_volume_scalar:.2f}")


def Initialization():
    global cap, mpHands, hands, mpDraw, volume
    # Initialize hand detection and pose estimation
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    # Initialize the audio volume control
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

def Get_Audio_Levels():
    # Get the current master volume as a scalar (0.0 to 1.0)
    current_volume_scalar = volume.GetMasterVolumeLevelScalar()
    print(f"Current Volume (Scalar): {current_volume_scalar:.2f}")

def Set_Audio_Levels(volume_level):

    # Set the master volume to a specific level (0.0 to 1.0)
    volume.SetMasterVolumeLevelScalar(volume_level, None)
        
def Get_Finger_Distance():
    global imageRGB
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imageRGB = cv2.flip(imageRGB,1)

    resultsHands = hands.process(imageRGB)

    imageRGB = cv2.cvtColor(imageRGB, cv2.COLOR_RGB2BGR)

    if resultsHands.multi_hand_landmarks:
        for handLms in resultsHands.multi_hand_landmarks:
            mpDraw.draw_landmarks(imageRGB, handLms, mpHands.HAND_CONNECTIONS)

            # Get the coordinates of the thumb and index finger tips
            thumb_tip = handLms.landmark[4]
            index_tip = handLms.landmark[8]

            # Calculate the pixel distance between the thumb and index finger tips
            distance = math.dist((thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y))
            
            # Convert distance to volume level (0.0 to 1.0)
            volume_level = 0 + ((distance - 0.01) * (1.0 - 0)) / (0.4 - 0.01)

            return volume_level


def Main():
    # Initialize hand detection and pose estimation
    Initialization()

    # Main loop for hand detection and volume control
    while True:
        volume_level = Get_Finger_Distance()

        if volume_level is not None:
            Set_Audio_Levels(volume_level)
            print(f"Calculated Volume Level: {volume_level:.2f}")

        #Acutal_Volume_Level = Get_Audio_Levels()
        #print(f"Acutal Volume Level: {Acutal_Volume_Level:.2f}")

        cv2.imshow("Hand Connections", imageRGB)
        if cv2.waitKey(20) == 27: # ESC key
            break
    cap.release()
    cv2.destroyAllWindows()

Main()