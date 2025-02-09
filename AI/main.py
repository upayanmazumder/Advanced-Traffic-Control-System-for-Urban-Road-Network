import cv2
import json
import time
import datetime
import asyncio
import aiohttp
import shutil
from model import VehicleDetector
from algorithm import optimize_intersections
from utils import draw_roi, draw_detections, log_congestion
from rl_agent import RLAgent
from ml_predictor import MLModel

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def compute_intersections_from_grid(grid_config, frame_width, frame_height):
    """
    Computes intersection ROIs given grid parameters.
    Each intersection has four road ROIs (north, south, east, west).
    """
    intersections = {}
    rows = grid_config["rows"]
    cols = grid_config["cols"]
    roi_width = grid_config["roi_width"]
    roi_height = grid_config["roi_height"]

    cell_width = frame_width / cols
    cell_height = frame_height / rows
    inter_id = 1
    for row in range(rows):
        for col in range(cols):
            base_x = col * cell_width
            base_y = row * cell_height
            intersections[str(inter_id)] = {
                "roads": {
                    "north": [int(base_x + cell_width/2 - roi_width/2), int(base_y + cell_height/4 - roi_height/2), roi_width, roi_height],
                    "south": [int(base_x + cell_width/2 - roi_width/2), int(base_y + 3*cell_height/4 - roi_height/2), roi_width, roi_height],
                    "east":  [int(base_x + 3*cell_width/4 - roi_width/2), int(base_y + cell_height/2 - roi_height/2), roi_width, roi_height],
                    "west":  [int(base_x + cell_width/4 - roi_width/2), int(base_y + cell_height/2 - roi_height/2), roi_width, roi_height]
                }
            }
            inter_id += 1
    return intersections

async def send_data(session, url, data):
    try:
        async with session.post(url + "traffic/signal-data", json={"data": data}, timeout=5) as response:
            if response.status == 204:
                print("Data sent successfully")
            else:
                print(f"Failed to send data. Status code: {response.status}")
                print(f"Response text: {await response.text()}")
    except aiohttp.ClientConnectorError as e:
        print(f"Connection error: {e}")
    except asyncio.TimeoutError:
        print("Request timed out")
    except Exception as e:
        print(f"An error occurred while sending data: {e}")

async def main():
    url = "https://api.ibreakstuff.upayan.dev/"
    config = load_config("config.json")
    # Uncomment the following two lines if you want to use a video file.
    video_path = "data/sample_video8.mp4"
    cap = cv2.VideoCapture(video_path)
    # cap = cv2.VideoCapture(1)  # using the default camera
    # cap.set(cv2.CAP_PROP_FOCUS, 60)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if "grid" in config:
        intersections_config = compute_intersections_from_grid(config["grid"], frame_width, frame_height)
    else:
        intersections_config = config.get("intersections", {})

    detector = VehicleDetector()
    scale_factor = 1.5
    min_phase_duration = config.get("min_phase_duration", 5)  # minimum wait of 5 sec
    last_phase_state = {}
    last_phase_switch_time = {}
    config["last_school_bus_green"] = config.get("last_school_bus_green", datetime.datetime.now())

    # Initialize prediction data for each intersection.
    prediction_data = {}
    for inter_no, inter_data in intersections_config.items():
        prediction_data[inter_no] = {}
        for road_no in inter_data.get("roads", {}).keys():
            prediction_data[inter_no][road_no] = {"car": 0, "ambulance": 0, "schoolbus": 0, "accident": 0}
    alpha = config.get("prediction_alpha", 0.7)

    # Instantiate and (optionally) train the DRL agent.
    rl_agent = RLAgent()
    if config.get("train_rl_agent", False):
        print("Training DRL Agent ...")
        rl_agent.train_agent(episodes=config.get("rl_training_episodes", 1000))
        print("DRL Training complete.")

    # Instantiate and train the ML predictor.
    ml_model = MLModel()
    ml_model.train_model()

    # Define available modes and set the initial mode.
    modes = ["normal", "ml", "rl"]
    operation_mode = config.get("operation_mode", "normal")
    mode_index = modes.index(operation_mode)

    async with aiohttp.ClientSession() as session:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video stream.")
                break
            frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

            # Gather traffic counts from each ROI.
            traffic_data = {}
            for inter_no, inter_data in intersections_config.items():
                traffic_data[inter_no] = {}
                for road_no, roi in inter_data.get("roads", {}).items():
                    x, y, w, h = [int(coord * scale_factor) for coord in roi]
                    if w <= 0 or h <= 0 or y < 0 or x < 0 or y+h > frame.shape[0] or x+w > frame.shape[1]:
                        print(f"Skipping invalid ROI for Intersection {inter_no}, Road {road_no}")
                        traffic_data[inter_no][road_no] = {"car": 0, "ambulance": 0, "schoolbus": 0, "accident": 0}
                        continue
                    roi_frame = frame[y:y+h, x:x+w]
                    if roi_frame.size == 0:
                        print(f"Empty ROI for Intersection {inter_no}, Road {road_no}")
                        traffic_data[inter_no][road_no] = {"car": 0, "ambulance": 0, "schoolbus": 0, "accident": 0}
                        continue
                    detections = detector.detect_vehicles(roi_frame)
                    counts = {"car": 0, "ambulance": 0, "schoolbus": 0, "accident": 0}
                    for detection in detections:
                        if detection['class'] in counts:
                            counts[detection['class']] += 1
                    traffic_data[inter_no][road_no] = counts
                    draw_detections(roi_frame, detections)
                    frame[y:y+h, x:x+w] = roi_frame

                    # Update prediction data using an exponential moving average.
                    prev_pred = prediction_data[inter_no][road_no]["car"]
                    current_count = counts["car"]
                    new_pred = alpha * current_count + (1 - alpha) * prev_pred
                    prediction_data[inter_no][road_no]["car"] = new_pred

            current_time = datetime.datetime.now()
            # Call the optimization algorithm. Pass ml_model or rl_agent based on the current mode.
            output_signals, computed_phases = optimize_intersections(
                traffic_data, prediction_data, config, current_time,
                rl_agent if operation_mode == "rl" else None,
                ml_model if operation_mode == "ml" else None
            )
            current_time_sec = time.time()
            final_phases = {}
            for inter_no, new_phase in computed_phases.items():
                if inter_no not in last_phase_state:
                    last_phase_state[inter_no] = new_phase
                    last_phase_switch_time[inter_no] = current_time_sec
                    final_phases[inter_no] = new_phase
                else:
                    prev_phase = last_phase_state[inter_no]
                    if new_phase != prev_phase:
                        if current_time_sec - last_phase_switch_time[inter_no] >= min_phase_duration:
                            last_phase_state[inter_no] = new_phase
                            last_phase_switch_time[inter_no] = current_time_sec
                            final_phases[inter_no] = new_phase
                        else:
                            final_phases[inter_no] = prev_phase
                    else:
                        final_phases[inter_no] = prev_phase

            # Append the current mode to each output.
            for signal in output_signals:
                signal["mode"] = ( "DRL Optimized" if operation_mode == "rl"
                                   else ("ML Predictive" if operation_mode == "ml" else "Normal") )

            # Log congestion history every cycle.
            log_congestion(traffic_data, current_time)
            print(json.dumps(output_signals, indent=2))
            asyncio.create_task(send_data(session, url, output_signals))

            for inter_no, inter_data in intersections_config.items():
                for road_no, roi in inter_data.get("roads", {}).items():
                    x, y, w, h = [int(coord * scale_factor) for coord in roi]
                    decision = next((item for item in output_signals if item["intersection"] == inter_no and item["road"] == road_no), None)
                    signal = decision["signal"] if decision else "UNKNOWN"
                    dynamic_duration = decision.get("dynamic_green_duration") if decision else None
                    counts = traffic_data[inter_no].get(road_no, {"car": 0, "ambulance": 0, "schoolbus": 0, "accident": 0})
                    mode = decision.get("mode", "Normal") if decision else "Normal"
                    draw_roi(frame, (x, y, w, h), inter_no, road_no, counts, signal, dynamic_duration, mode)

            cv2.imshow("Intelligent Traffic Management System", frame)
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break
            # Press 't' to cycle through the modes.
            if key == ord('t'):
                mode_index = (mode_index + 1) % len(modes)
                operation_mode = modes[mode_index]
                config["operation_mode"] = operation_mode  # update config for consistency
                print(f"Operation Mode switched to {operation_mode}")
            await asyncio.sleep(0)

        # At session end, save a copy of the congestion log.
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy("congestion_log.txt", f"session_log_{timestamp}.txt")
        print(f"Session log saved as session_log_{timestamp}.txt")
    await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
