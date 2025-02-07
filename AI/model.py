import cv2
import os
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path='models/best.pt'):
        self.model_path = os.path.join(os.getcwd(), model_path)
        self.model = YOLO(self.model_path)
        
    def detect_vehicles(self, frame):
        results = self.model(frame)
        detections = {'car': [], 'schoolbus': []}
        counts = {'car': 0, 'schoolbus': 0}
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                if conf < 0.3:
                    continue
                category = 'car' if cls == 0 else 'schoolbus'
                detections[category].append((x1, y1, x2, y2))
                counts[category] += 1
        return detections, counts
