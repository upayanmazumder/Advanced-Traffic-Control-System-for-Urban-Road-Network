import cv2
import os
from ultralytics import YOLO
import random

class VehicleDetector:
    def __init__(self, model_path='models/best.pt'):
        self.model_path = os.path.join(os.getcwd(), model_path)
        self.model = YOLO(self.model_path)
    def detect_vehicles(self, frame):
        results = self.model(frame)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                class_names = {0: 'accident', 1: 'ambulance', 2: 'car', 3: 'schoolbus'}
                class_name = class_names.get(cls, 'unknown')
                if conf < 0.7:
                    continue
                detection = {'bbox': (x1, y1, x2, y2), 'confidence': conf, 'class': class_name}
                if class_name == "ambulance":
                    detection["speed"] = random.uniform(40, 80)
                detections.append(detection)
        return detections
