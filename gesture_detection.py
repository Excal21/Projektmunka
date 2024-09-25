# A projekt a Google MediaPipe moduljára és a hozzá tartozó példakódok egyes elemeire épül.
# Bővebb információ Google MediaPiperól az alábbi linken érhető el:
# https://ai.google.dev/edge/mediapipe 

import cv2
import mediapipe as mp
from time import sleep
from matplotlib import pyplot as plt
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
import requests
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image


#Modelfájl betöltése és beállítása
model_file = open('gesture_recognizer.task', "rb")
model_data = model_file.read()
model_file.close()
base_options = python.BaseOptions(model_asset_buffer=model_data)
options = vision.GestureRecognizerOptions(
    base_options=base_options,
    min_tracking_confidence=0.5,
    num_hands=2

    )

recognizer = vision.GestureRecognizer.create_from_options(options)

url = "http://192.168.193.124:8080/shot.jpg" #Telefon kamera
cap = cv2.VideoCapture(0)    #Beépített kamera

while True: 
    #Beépített kamera
    ret, img = cap.read()
    img = cv2.flip(img, 1)


    #Telefon kamera
    # img_resp = requests.get(url)
    # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    # img = cv2.imdecode(img_arr, -1)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    
    
    #Kilépés ESC gombra
    if cv2.waitKey(1) == 27: 
        break
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
    result = recognizer.recognize(mp_image)

    #0-ás index a bal kéz, 1 a jobb
    if len(result.gestures) == 1 and result.gestures[0][0].category_name != 'None':
        print('Egy kezes gesztus: ' + result.gestures[0][0].category_name)
        sleep(0.01)
    elif len(result.gestures) == 2 and result.gestures[0][0].category_name != 'None' and result.gestures[1][0].category_name != 'None':
        print('Bal kéz: ' + ' ' + result.gestures[0][0].category_name + ' ' +
              'Jobb kéz: ' + ' ' + result.gestures[1][0].category_name)
    
    #sleep(0.01)
    

    annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), result)

    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    cv2.imshow('Annotated Image', annotated_image)

cv2.destroyAllWindows() 
