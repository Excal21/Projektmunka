# A projekt a Google MediaPipe moduljára és a hozzá tartozó példakódok egyes elemeire épül.
# Bővebb információ Google MediaPiperól az alábbi linken érhető el:
# https://ai.google.dev/edge/mediapipe 

import os
import cv2
import mediapipe as mp
from time import sleep
from matplotlib import pyplot as plt
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from datetime import datetime
import shutil
import json


class Recognition:
  def __init__(self, task_file_path: str):
      self.MARGIN = 10  # pixels
      self.FONT_SIZE = 1
      self.FONT_THICKNESS = 1
      self.HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green

      self.mp_hands = mp.solutions.hands
      self.mp_drawing = mp.solutions.drawing_utils
      self.mp_drawing_styles = mp.solutions.drawing_styles

      #Modelfájl betöltése és beállítása
      self.model_file = open(task_file_path, "rb")
      self.model_data = self.model_file.read()
      self.model_file.close()
      self.base_options = python.BaseOptions(model_asset_buffer=self.model_data)

      self.options = vision.GestureRecognizerOptions(
          base_options=self.base_options,
          min_tracking_confidence=0.7,
          
          num_hands=4
          )
      self.recognizer = vision.GestureRecognizer.create_from_options(self.options)

      self.__camera = 0
      self.__labels = self.__extract_labels(task_file_path)
      self.__labels_with_alias = self.__alias_labels(self.__labels)
      self.confidence = 0.9

  @property
  def camera(self):
    return self.__camera
  
  @camera.setter
  def camera(self, value):
    if type(value) is str:
      self.__camera = value + '/video'
    else:
      self.__camera = value

  @property
  def labels(self):
    return self.__labels

  @property
  def labels_with_alias(self):
    return self.__labels_with_alias

  def __extract_labels(self, path):
    # A kibontási könyvtár neve
    extract_to = 'extracted_files'

    # Ellenőrizd, hogy a kibontási könyvtár létezik-e, ha nem, hozd létre
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)


    archive_file = path
    shutil.unpack_archive(archive_file, extract_to, 'zip')

    archive_file = extract_to + '\\hand_gesture_recognizer.task'
    shutil.unpack_archive(archive_file, extract_to, 'zip')

    try:
      archive_file = extract_to + '\\canned_gesture_classifier.tflite'
      shutil.unpack_archive(archive_file, extract_to, 'zip')
    except shutil.ReadError:
      archive_file = extract_to + '\\custom_gesture_classifier.tflite'
      shutil.unpack_archive(archive_file, extract_to, 'zip')

    retlist = []
    with open('extracted_files\\labels.txt', 'r') as file:
      for line in file.readlines():
        if not 'NONE' in line:
          retlist.append(line.replace('\n', ''))

    shutil.rmtree(extract_to)
    return retlist

  def __alias_labels(self, labels):
    readable = {
        "None": "",
        "2up": "mutatás felfelé két ujjal",
        "2down": "mutatás lefelé két ujjal",
        "2left": "mutatás balra két ujjal",
        "2right": "mutatás jobbra két ujjal",
        "drei_glaser": "három",
        "peace": "csao",
        "2Metal": "metálvilla",
        "long_life": "hosszú élet",
        "fist": "ökölpacsi",
        "like": "tetszik",
        "perfect": "tökéletes",
        "middle_finger": "középső ujj",
        "fityisz": "fityisz",
        "F": "F",
        "CLOSEDPALM" : "Zárt tenyér",
        "OPENPALM" : "Nyitott tenyér",
        "THUMBSUP" : "Hüvelykujj fel",
        "THUMBSDOWN" : "Hüvelykujj le",
        "PEACE": "Béke",
        "OK": "OK",
        "LONGLIVE": "Hosszú élet (STAR TREK)"

    }

    gest_dict = {}
    for label in labels:
        if label in readable:
            gest_dict[label] = readable[label]
        else:
            gest_dict[label] = label

    return gest_dict

  def draw_landmarks_on_image(self, rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    for idx in range(len(hand_landmarks_list)):
      hand_landmarks = hand_landmarks_list[idx]
      handedness = handedness_list[idx]

      #Érzékelt pontok megrajzolása
      hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
      hand_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
      ])
      solutions.drawing_utils.draw_landmarks(
        annotated_image,
        hand_landmarks_proto,
        solutions.hands.HAND_CONNECTIONS,
        solutions.drawing_utils.DrawingSpec(color=(33, 43, 53), thickness=2, circle_radius=4),
        solutions.drawing_utils.DrawingSpec(color=(156, 220, 254), thickness=2))

      height, width, _ = annotated_image.shape
      x_coordinates = [landmark.x for landmark in hand_landmarks]
      y_coordinates = [landmark.y for landmark in hand_landmarks]
      text_x = int(min(x_coordinates) * width)
      text_y = int(min(y_coordinates) * height) - self.MARGIN

      # Draw handedness (left or right hand) on the image.
      # cv2.putText(annotated_image, f"{handedness[0].category_name}",
      #             (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
      #             self.FONT_SIZE, (0, 0, 0), self.FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image

  def Run(self):
    cap = cv2.VideoCapture(self.__camera)
    last_gestures = []
    last_gesture_time = datetime.now()


    while True: 
      #Beépített kamera
      ret, img = cap.read()
      img = cv2.flip(img, 1)

      img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
      
      
      
      #Kilépés ESC gombra
      if cv2.waitKey(1) == 27: 
          break
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

      result = self.recognizer.recognize(mp_image)
      if len(result.gestures) >= 1:
        for gesture in result.gestures:
            if gesture[0].category_name != 'NONE' and gesture[0].category_name != '':
              if gesture[0].score > self.confidence:
                print(f"{gesture[0].category_name} Confidence: {gesture[0].score:.2f}")
                last_gestures.append(gesture[0].category_name)

      if len(last_gestures) >= 7:
        if all(gesture == last_gestures[0] for gesture in last_gestures) and (datetime.now() - last_gesture_time).total_seconds() > 1 and last_gestures[0]  != '':
          print(last_gestures[0])
          last_gesture_time = datetime.now()
        last_gestures = []
          

      annotated_image = self.draw_landmarks_on_image(mp_image.numpy_view(), result)

      annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
      cv2.imshow('Annotated Image', annotated_image)

    cv2.destroyAllWindows() 
  

if __name__ == '__main__':
  taskFile = "gesture_recognizer.task"
  recognizer = Recognition("gesture_recognizer.task", "gesture_recognition.config")
  #print(recognizer.camera)
  #print(recognizer.labels)
  print(recognizer.labels_with_alias)
  recognizer.confidence = 0.7
  #recognizer.Run()


  