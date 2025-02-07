import cv2

def draw_roi(frame, roi, inter_no, road_no, count, signal):
    """
    Draws the region of interest (ROI) and annotates it with the intersection and road information,
    vehicle count, and proposed signal state.
    """
    x, y, w, h = roi
    color = (0, 255, 0) if signal == "GREEN" else (0, 0, 255)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    text = f"I{inter_no} R{road_no}: {count} | {signal}"
    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def draw_detections(frame, detections):
    """
    Draws bounding boxes for the vehicle detections.
    """
    for (x1, y1, x2, y2) in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
