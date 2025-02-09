import cv2
import json
import datetime

def draw_roi(frame, roi, inter_no, road_no, counts, signal, dynamic_duration=None, mode="Normal"):
    x, y, w, h = roi
    if mode == "DRL_Optimized":
        if signal == "GREEN":
            color = (255, 0, 0)       # Blue
        elif signal == "RED":
            color = (0, 255, 255)     # Yellow
        else:
            color = (255, 0, 255)     # Purple (fallback)
    else:
        if signal == "GREEN":
            color = (0, 255, 0)       # Green
        else:
            color = (0, 0, 255)       # Red
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    text = f"I{inter_no} R{road_no}: C{counts['car']} A{counts['ambulance']} S{counts['schoolbus']} Acc{counts['accident']} | {signal} | {mode}"
    if dynamic_duration is not None:
        text += f" DG:{dynamic_duration}s"
    text_y = max(y - 10, 20)
    cv2.putText(frame, text, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def draw_detections(frame, detections):
    for detection in detections:
        x1, y1, x2, y2 = detection['bbox']
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

def log_congestion(traffic_data, current_time):
    log_entry = {
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "traffic_data": traffic_data
    }
    with open("congestion_log.txt", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
