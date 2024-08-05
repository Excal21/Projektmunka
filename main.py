
import cv2 
import mediapipe as mp 
from google.protobuf.json_format import MessageToDict 
import warnings
import requests 
import numpy as np 
import imutils 
  

warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf.symbol_database')
  
mpHands = mp.solutions.hands 
hands = mpHands.Hands( 
    static_image_mode=False, 
    model_complexity=1, 
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75, 
    max_num_hands=2) 
  
#Telefonról is tud, ha itt link van, ha beépített kamera kell, akkor numerikusan 0 értéket kell ide írni
url = "http://192.168.1.12:8080/shot.jpg"
  
while True: 
    img_resp = requests.get(url) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=1000, height=1800) 
  


    img = cv2.flip(img, 1) 

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    results = hands.process(imgRGB) 
  

    # Ha van objektum, akkor van kéz
    if results.multi_hand_landmarks: 
  

        if len(results.multi_handedness) == 2: 
                
            cv2.putText(img, 'Both Hands', (250, 50), 
                        cv2.FONT_HERSHEY_COMPLEX, 
                        0.9, (0, 255, 0), 2) 
  
        else: 
            for i in results.multi_handedness: 
                
                #Ágyazott dicionary, a fa label címkéjű ága adja vissza, hogy melyik kezet látja a mediapipe
                label = MessageToDict(i)['classification'][0]['label'] 
  
                if label == 'Left': 
                    
                    cv2.putText(img, label+' Hand', 
                                (20, 50), 
                                cv2.FONT_HERSHEY_COMPLEX,  
                                0.9, (0, 255, 0), 2) 
  
                if label == 'Right': 
                      
                    #Kép feliratozása
                    cv2.putText(img, label+' Hand', (460, 50), 
                                cv2.FONT_HERSHEY_COMPLEX, 
                                0.9, (0, 255, 0), 2) 
  
    #ESC kilépés
    if cv2.waitKey(1) == 27: 
        break
  
    cv2.imshow("Android_cam", img) 
cv2.destroyAllWindows() 
