import cv2

print("Buscando cámaras disponibles...\n")

for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✔ Cámara detectada en índice {i}")
        cap.release()
    else:
        print(f"❌ Sin cámara en índice {i}")
