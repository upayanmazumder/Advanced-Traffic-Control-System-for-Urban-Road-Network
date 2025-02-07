import cv2

def draw_roi(frame, roi, inter_no, road_no, counts, signal):
    x, y, w, h = roi
    color = (0, 255, 0) if signal == "GREEN" else (0, 0, 255)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    text = f"I{inter_no} R{road_no}: C{counts['car']} S{counts['schoolbus']} | {signal}"
    text_y = max(y - 10, 20)
    cv2.putText(frame, text, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def draw_detections(frame, detections, color):
    for (x1, y1, x2, y2) in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
