from ultralytics import YOLO

model = YOLO("yolo11n.pt")
print("Abriendo la cámara... cierra la ventana o presiona 'q' para terminar.")

# IDs de clases: car=2, motorcycle=3, bus=5, truck=7
traffic_classes_id = [2, 3, 5, 7]

traffic_status : dict = {
    0: "No hay tráfico",
    1: "Tráfico ligero",
    2: "Tráfico moderado",
    3: "Tráfico pesado",
}

traffic_light_thresholds : dict = {
    0: 0,
    1: 5,
    2: 15,
    3: 30,
}

cars_count: int = 0

# Detección en vivo usando la webcam
model.track(
    source=0,
    show=True,
    save=False,
    verbose=False,
    classes=traffic_classes_id,
)
