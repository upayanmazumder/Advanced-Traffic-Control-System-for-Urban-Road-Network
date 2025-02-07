import cv2
import json
import time
from model import VehicleDetector
from algorithm import optimize_intersections
from utils import draw_roi, draw_detections

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)
    
def compute_intersections_from_grid(grid_config):
    """
    Given grid parameters, compute a dictionary for intersections.
    Each intersection has four road ROIs computed relative to its cell’s base position.
    """
    intersections = {}
    rows = grid_config["rows"]
    cols = grid_config["cols"]
    roi_width = grid_config["roi_width"]
    roi_height = grid_config["roi_height"]
    # For positioning the roads inside each intersection cell:
    road_offset_x = grid_config["spacing_x"]
    road_offset_y = grid_config["spacing_y"]
    start_x = grid_config["start_x"]
    start_y = grid_config["start_y"]
    # Gaps between intersections (to avoid overlap)
    gap_x = grid_config.get("intersection_gap_x", 50)
    gap_y = grid_config.get("intersection_gap_y", 50)
    
    # Each intersection cell will span two road ROIs in width and height.
    cell_width = roi_width * 2
    cell_height = roi_height * 2

    inter_id = 1
    for row in range(rows):
        for col in range(cols):
            base_x = start_x + col * (cell_width + gap_x)
            base_y = start_y + row * (cell_height + gap_y)
            intersections[str(inter_id)] = {
                "roads": {
                    "1": [base_x, base_y, roi_width, roi_height],
                    "2": [base_x + road_offset_x, base_y, roi_width, roi_height],
                    "3": [base_x, base_y + road_offset_y, roi_width, roi_height],
                    "4": [base_x + road_offset_x, base_y + road_offset_y, roi_width, roi_height]
                }
            }
            inter_id += 1
    return intersections

def preprocess_frame(frame):
    # Apply contrast enhancement
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return enhanced

def main():
    config = load_config("config.json")
    if "grid" in config:
        intersections_config = compute_intersections_from_grid(config["grid"])
    else:
        intersections_config = config.get("intersections", {})

    cap = cv2.VideoCapture(1)  # 0 for default webcam, 1 or 2 for external cameras

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    cv2.namedWindow("Smart Traffic Management System", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Smart Traffic Management System", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    detector = VehicleDetector()

    scale_factor = 4
    min_phase_duration = config.get("min_phase_duration", 5)
    last_phase_state = {}
    last_phase_switch_time = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream.")
            break

        frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

        traffic_data = {}
        for inter_no, inter_data in intersections_config.items():
            roads_config = inter_data.get("roads", {})
            traffic_data[inter_no] = {}
            for road_no, roi in roads_config.items():
                x, y, w, h = [int(coord * scale_factor) for coord in roi]
                
                if w <= 0 or h <= 0 or y < 0 or x < 0 or y+h > frame.shape[0] or x+w > frame.shape[1]:
                    print(f"Skipping invalid ROI for Intersection {inter_no}, Road {road_no}")
                    traffic_data[inter_no][road_no] = {'car': 0, 'schoolbus': 0}
                    continue

                roi_frame = frame[y:y+h, x:x+w]
                
                if roi_frame.size == 0:
                    print(f"Empty ROI for Intersection {inter_no}, Road {road_no}")
                    traffic_data[inter_no][road_no] = {'car': 0, 'schoolbus': 0}
                    continue

                detections, counts = detector.detect_vehicles(roi_frame)
                traffic_data[inter_no][road_no] = counts
                draw_detections(roi_frame, detections['car'], (0, 255, 0))
                draw_detections(roi_frame, detections['schoolbus'], (0, 0, 255))
                frame[y:y+h, x:x+w] = roi_frame

        output_signals, computed_phases = optimize_intersections(traffic_data, config)

        current_time = time.time()
        final_phases = {}
        for inter_no, new_phase in computed_phases.items():
            if inter_no not in last_phase_state:
                last_phase_state[inter_no] = new_phase
                last_phase_switch_time[inter_no] = current_time
                final_phases[inter_no] = new_phase
            else:
                prev_phase = last_phase_state[inter_no]
                if new_phase != prev_phase:
                    if current_time - last_phase_switch_time[inter_no] >= min_phase_duration:
                        last_phase_state[inter_no] = new_phase
                        last_phase_switch_time[inter_no] = current_time
                        final_phases[inter_no] = new_phase
                    else:
                        final_phases[inter_no] = prev_phase
                else:
                    final_phases[inter_no] = prev_phase

        final_output_signals = []
        for inter_no, inter_data in intersections_config.items():
            phase = final_phases.get(inter_no, "A")
            roads_config = inter_data.get("roads", {})
            for road_no, roi in roads_config.items():
                counts = traffic_data[inter_no].get(road_no, {'car': 0, 'schoolbus': 0})
                if phase == "A" and road_no in ["1", "3"]:
                    signal = "GREEN"
                elif phase == "B" and road_no in ["2", "4"]:
                    signal = "GREEN"
                else:
                    signal = "RED"
                final_output_signals.append({
                    "intersection": inter_no,
                    "road": road_no,
                    "cars": counts['car'],
                    "schoolbuses": counts['schoolbus'],
                    "signal": signal
                })

        print(final_output_signals)

        for inter_no, inter_data in intersections_config.items():
            roads_config = inter_data.get("roads", {})
            for road_no, roi in roads_config.items():
                x, y, w, h = [int(coord * scale_factor) for coord in roi]
                counts = traffic_data[inter_no].get(road_no, {'car': 0, 'schoolbus': 0})
                decision = next((item for item in final_output_signals
                                 if item["intersection"] == inter_no and item["road"] == road_no), None)
                signal = decision["signal"] if decision else "UNKNOWN"
                draw_roi(frame, (x, y, w, h), inter_no, road_no, counts, signal)

        cv2.imshow("Smart Traffic Management System", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()