import cv2
import json
import time
import argparse
from model import VehicleDetector
from algorithm import optimize_intersections
from utils import draw_roi, draw_detections


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def compute_intersections_from_grid(grid_config, frame_width, frame_height):
    """
    Given grid parameters and frame dimensions, compute a dictionary for intersections.
    Each intersection has four road ROIs (North, South, East, West) computed relative
    to its cell's base position. The image is equally divided into six intersections.
    """
    intersections = {}
    rows = grid_config["rows"]
    cols = grid_config["cols"]
    roi_width = grid_config["roi_width"]
    roi_height = grid_config["roi_height"]
    start_x = grid_config["start_x"]
    start_y = grid_config["start_y"]

    # Calculate cell dimensions to equally divide the frame
    cell_width = frame_width / cols
    cell_height = frame_height / rows

    inter_id = 1
    for row in range(rows):
        for col in range(cols):
            base_x = col * cell_width
            base_y = row * cell_height
            intersections[str(inter_id)] = {
                "roads": {
                    "north": [int(base_x + cell_width / 2 - roi_width / 2),
                              int(base_y + cell_height / 4 - roi_height / 2), roi_width, roi_height],
                    "south": [int(base_x + cell_width / 2 - roi_width / 2),
                              int(base_y + 3 * cell_height / 4 - roi_height / 2), roi_width, roi_height],
                    "east": [int(base_x + 3 * cell_width / 4 - roi_width / 2),
                             int(base_y + cell_height / 2 - roi_height / 2), roi_width, roi_height],
                    "west": [int(base_x + cell_width / 4 - roi_width / 2),
                             int(base_y + cell_height / 2 - roi_height / 2), roi_width, roi_height]
                }
            }
            inter_id += 1
    return intersections


def main():
    parser = argparse.ArgumentParser(description="Smart Traffic Management System")
    parser.add_argument("--output", choices=["video", "console"], default="video",
                        help="Output method: 'video' for displaying video output, 'console' for console output only")
    args = parser.parse_args()

    config = load_config("config.json")
    cap = cv2.VideoCapture(1)  # Changed from video path to default camera
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Compute intersections based on grid configuration and frame dimensions
    if "grid" in config:
        intersections_config = compute_intersections_from_grid(config["grid"], frame_width, frame_height)
    else:
        intersections_config = config.get("intersections", {})

    detector = VehicleDetector()

    # Option to upscale the frame:
    scale_factor = 2  # Adjust as needed based on your video resolution.

    # For minimum phase duration logic:
    min_phase_duration = config.get("min_phase_duration", 5)  # seconds
    last_phase_state = {}  # intersection -> phase ("A" or "B")
    last_phase_switch_time = {}  # intersection -> timestamp of last change

    # Create a full screen window only if video output is selected
    if args.output == "video":
        cv2.namedWindow("Smart Traffic Management System", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Smart Traffic Management System", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream.")
            break

        # Upscale the frame to improve detection resolution.
        frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

        # Process each ROI for intersections.
        traffic_data = {}
        for inter_no, inter_data in intersections_config.items():
            roads_config = inter_data.get("roads", {})
            traffic_data[inter_no] = {}
            for road_no, roi in roads_config.items():
                # Scale ROI coordinates if defined for the original resolution.
                x, y, w, h = [int(coord * scale_factor) for coord in roi]

                # Ensure the ROI coordinates are within the frame dimensions.
                # Also, check that width and height are non-zero.
                if w <= 0 or h <= 0 or y < 0 or x < 0 or y + h > frame.shape[0] or x + w > frame.shape[1]:
                    print(f"Skipping invalid ROI for Intersection {inter_no}, Road {road_no}")
                    traffic_data[inter_no][road_no] = 0
                    continue

                roi_frame = frame[y:y + h, x:x + w]

                # Additionally check if the ROI frame is empty.
                if roi_frame.size == 0:
                    print(f"Empty ROI for Intersection {inter_no}, Road {road_no}")
                    traffic_data[inter_no][road_no] = 0
                    continue

                detections, count = detector.detect_vehicles(roi_frame)
                traffic_data[inter_no][road_no] = count
                # draw_detections(roi_frame, detections)  # Commented out draw_detections

                # Replace the processed ROI in the full frame.
                frame[y:y + h, x:x + w] = roi_frame

        # Compute optimization from traffic data.
        output_signals, computed_phases = optimize_intersections(traffic_data, config)

        # Get current time.
        current_time = time.time()
        # For each intersection, enforce the minimum phase duration.
        final_phases = {}
        for inter_no, new_phase in computed_phases.items():
            # If no previous phase recorded, set it now.
            if inter_no not in last_phase_state:
                last_phase_state[inter_no] = new_phase
                last_phase_switch_time[inter_no] = current_time
                final_phases[inter_no] = new_phase
            else:
                prev_phase = last_phase_state[inter_no]
                # If the phase has changed...
                if new_phase != prev_phase:
                    # Only allow change if sufficient time has passed.
                    if current_time - last_phase_switch_time[inter_no] >= min_phase_duration:
                        last_phase_state[inter_no] = new_phase
                        last_phase_switch_time[inter_no] = current_time
                        final_phases[inter_no] = new_phase
                    else:
                        # Otherwise, continue using the previous phase.
                        final_phases[inter_no] = prev_phase
                else:
                    final_phases[inter_no] = prev_phase

        # Recompute the per-road signals based on the final phases.
        final_output_signals = []
        for inter_no, inter_data in intersections_config.items():
            phase = final_phases.get(inter_no, "A")  # default to "A" if missing
            roads_config = inter_data.get("roads", {})
            for road_no, roi in roads_config.items():
                count = traffic_data[inter_no].get(road_no, 0)
                if phase == "A" and road_no in ["north", "south"]:
                    signal = "GREEN"
                elif phase == "B" and road_no in ["east", "west"]:
                    signal = "GREEN"
                else:
                    signal = "RED"
                final_output_signals.append({
                    "intersection": inter_no,
                    "road": road_no,
                    "cars": count,
                    "signal": signal
                })

        if args.output == "console":
            print(final_output_signals)  # Print to console
        elif args.output == "video":
            # Draw the ROIs and the traffic signal status.
            for inter_no, inter_data in intersections_config.items():
                roads_config = inter_data.get("roads", {})
                for road_no, roi in roads_config.items():
                    x, y, w, h = [int(coord * scale_factor) for coord in roi]
                    count = traffic_data[inter_no].get(road_no, 0)
                    # Find the corresponding signal decision.
                    decision = next((item for item in final_output_signals
                                     if item["intersection"] == inter_no and item["road"] == road_no), None)
                    signal = decision["signal"] if decision else "UNKNOWN"
                    draw_roi(frame, (x, y, w, h), inter_no, road_no, count, signal)

            cv2.imshow("Smart Traffic Management System", frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

    cap.release()
    if args.output == "video":
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
