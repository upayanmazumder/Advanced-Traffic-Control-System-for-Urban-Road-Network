import cv2
import os
from ultralytics import YOLO

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
                # Only consider detections with sufficient confidence (adjust threshold if needed)
                if conf < 0.3:
                    continue
                detections.append((x1, y1, x2, y2))
        return detections, len(detections)
