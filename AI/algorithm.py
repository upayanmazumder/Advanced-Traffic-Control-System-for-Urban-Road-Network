import datetime

def optimize_intersections(traffic_data, config, current_time):
    results = {}
    school_bus_time = config.get("school_bus_time", "15:00")  # Default school bus time
    school_bus_duration = config.get("school_bus_duration", 60)  # Default duration: 10 minutes
    school_intersection = config.get("school_intersection", "1")  # Default school intersection

    for inter_no, roads in traffic_data.items():
        count_A = sum(roads.get(road, {}).get("car", 0) for road in ["north", "south"])
        count_B = sum(roads.get(road, {}).get("car", 0) for road in ["east", "west"])

        # Check for ambulances
        ambulance_A = sum(roads.get(road, {}).get("ambulance", 0) for road in ["north", "south"])
        ambulance_B = sum(roads.get(road, {}).get("ambulance", 0) for road in ["east", "west"])

        # Check for school buses at specific time
        current_time_str = current_time.strftime("%H:%M")
        is_school_bus_time = current_time_str == school_bus_time and inter_no == school_intersection

        # Prioritize ambulances
        if ambulance_A > 0:
            chosen_phase = "A"
        elif ambulance_B > 0:
            chosen_phase = "B"
        # Prioritize school buses at the specified time
        elif is_school_bus_time:
            schoolbus_A = sum(roads.get(road, {}).get("schoolbus", 0) for road in ["north", "south"])
            schoolbus_B = sum(roads.get(road, {}).get("schoolbus", 0) for road in ["east", "west"])
            if schoolbus_A > schoolbus_B:
                chosen_phase = "A"
            else:
                chosen_phase = "B"
        # Otherwise, base decision on car count
        else:
            chosen_phase = "A" if count_A >= count_B else "B"

        results[inter_no] = {"phase": chosen_phase, "roads": roads}

    # The rest of the function (adjacency logic) remains unchanged

    output = []
    for inter_no, data in results.items():
        phase = data["phase"]
        roads = data["roads"]
        for road_no, counts in roads.items():
            if phase == "A" and road_no in ["north", "south"]:
                signal = "GREEN"
            elif phase == "B" and road_no in ["east", "west"]:
                signal = "GREEN"
            else:
                signal = "RED"
            output.append({
                "intersection": inter_no,
                "road": road_no,
                "cars": counts.get("car", 0),
                "ambulances": counts.get("ambulance", 0),
                "schoolbuses": counts.get("schoolbus", 0),
                "signal": signal
            })
            if counts.get("accident", 0) > 0:
                print(f"ALERT: Accident detected at Intersection {inter_no}, Road {road_no}")

    return output, {k: v["phase"] for k, v in results.items()}
