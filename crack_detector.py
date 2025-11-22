# Ce code a pour but de détecter les "fissures" d'un béton. 
# Il va en fait détecter le changement de couleur du cristal liquide et afficher un message 
# lorsqu'il y a une fissure. 
# Un téléphone va faire office de caméra en envoyer un flux vidéo à cet ordinateur 
# par le biais de DroidCam.

import cv2
import numpy as np
import time

#URL a MODIFIER !
url = "http://xxx.xxx.xxx.xx:4747/video"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Erreur : Impossible d’ouvrir la caméra.")
    exit()

start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur de lecture vidéo.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    alert_message = "Pas de danger"
    alert_color = (0, 255, 0)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)

            padding = 10
            x -= padding
            y -= padding
            w += 2 * padding
            h += 2 * padding

            # Couleur orange (couleur indiquant les dangers : la fissure)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)

            alert_message = "   /!\ Attention : Fissure détectée /!\ "
            print(f"Danger ! Coordonnées : x={x}, y={y}, w={w}, h={h}")
            alert_color = (0, 0, 255)
            break

    cv2.putText(frame, alert_message, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, alert_color, 2)

    elapsed_time = int(time.time() - start_time)
    timer_text = f"{elapsed_time // 3600:02}:{(elapsed_time % 3600) // 60:02}:{elapsed_time % 60:02}"
    height, width, _ = frame.shape
    text_size, _ = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    text_x = width - text_size[0] - 10
    text_y = height - 10
    cv2.putText(frame, timer_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Détection Rouge - Caméra", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
