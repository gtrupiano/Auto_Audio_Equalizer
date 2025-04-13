from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import mediapipe as mp
import numpy as np
import math
import time
import msvcrt  # Windows-specific module to capture key events

# Global variables
cap = None
mpHands = None
hands = None
mpDraw = None
volume = None
imageRGB = None

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
    return current_volume_scalar

def Set_Audio_Levels(volume_level):
    # Set the master volume to a specific level (0.0 to 1.0)
    volume.SetMasterVolumeLevelScalar(volume_level, None)

def Get_Finger_Distance():
    global imageRGB
    success, image = cap.read()
    
    if not success:
        return None

    # Convert image for processing: flip and convert color space
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imageRGB = cv2.flip(imageRGB, 1)

    resultsHands = hands.process(imageRGB)

    # Convert imageRGB back to BGR for display
    imageRGB = cv2.cvtColor(imageRGB, cv2.COLOR_RGB2BGR)

    if resultsHands.multi_hand_landmarks:
        for handLms in resultsHands.multi_hand_landmarks:
            mpDraw.draw_landmarks(imageRGB, handLms, mpHands.HAND_CONNECTIONS)

            # Get the coordinates of the thumb tip (landmark 4) and index finger tip (landmark 8)
            thumb_tip = handLms.landmark[4]
            index_tip = handLms.landmark[8]

            # Calculate the Euclidean distance between the thumb and index finger tips
            distance = math.dist((thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y))

            # Map the distance from the range 0.01-0.4 to a volume level between 0 and 1.0
            volume_level = ((distance - 0.01) * (1.0 - 0)) / (0.4 - 0.01)
            # Clamp the volume level between 0 and 1
            volume_level = max(0, min(volume_level, 1))
            return volume_level

    return None

def Main():
    Initialization()

    # Main loop for hand detection and volume control
    while True:
        volume_level = Get_Finger_Distance()

        if volume_level is not None:
            #print(f"Calculated Volume Level: {volume_level:.2f}")
            Set_Audio_Levels(volume_level)
            current_volume = Get_Audio_Levels()
            print(f"Actual Volume Level: {current_volume:.2f}")
        else:
            print("No hand detected.")

        cv2.imshow("Hand Connections", imageRGB)
        if cv2.waitKey(20) == 27:  # ESC key to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    Main()
