import cv2
import os

# Mappa létrehozása, ha nem létezik
output_dir = "GESZTUS_NEVE"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Kamera inicializálása
url = "http://192.168.193.124:8080/video"
cap = cv2.VideoCapture(0)

width = 500
height = 500

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nem sikerült képet rögzíteni a kamerából")
        break

    # Kép közepének kivágása (320x240 pixel)
    y, x, _ = frame.shape
    start_x = x // 2 - 160
    start_y = y // 2 - 120
    end_x = start_x + width
    end_y = start_y + height
    cropped_frame = frame[start_y:end_y, start_x:end_x]

    cv2.imshow("Kamera", cropped_frame)

    key = cv2.waitKey(1)
    if key % 256 == 27:  # ESC billentyű
        print("Kilépés...")
        break
    elif key % 256 == 32:  # Space billentyű
        img_name = os.path.join(output_dir, f"kamera_kep2_{img_counter}.png")
        cv2.imwrite(img_name, cropped_frame)
        print(f"{img_name} elmentve!")
        img_counter += 1

cap.release()
cv2.destroyAllWindows()