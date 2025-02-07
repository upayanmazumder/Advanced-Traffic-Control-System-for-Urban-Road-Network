def optimize_intersections(traffic_data, config):
    results = {}
    for inter_no, roads in traffic_data.items():
        count_A = (roads.get("1", {}).get("car", 0) + roads.get("1", {}).get("schoolbus", 0) * 2 +
                   roads.get("3", {}).get("car", 0) + roads.get("3", {}).get("schoolbus", 0) * 2)
        count_B = (roads.get("2", {}).get("car", 0) + roads.get("2", {}).get("schoolbus", 0) * 2 +
                   roads.get("4", {}).get("car", 0) + roads.get("4", {}).get("schoolbus", 0) * 2)
        chosen_phase = "A" if count_A >= count_B else "B"
        results[inter_no] = {"phase": chosen_phase, "roads": roads}
    
    adjacency = config.get("adjacency", {})
    for inter_no, adj_inter_no in adjacency.items():
        if inter_no not in results or adj_inter_no not in results:
            continue
        phase1 = results[inter_no]["phase"]
        phase2 = results[adj_inter_no]["phase"]
        if phase1 != phase2:
            roads1 = results[inter_no]["roads"]
            roads2 = results[adj_inter_no]["roads"]
            count_A_1 = (roads1.get("1", {}).get("car", 0) + roads1.get("1", {}).get("schoolbus", 0) * 2 +
                         roads1.get("3", {}).get("car", 0) + roads1.get("3", {}).get("schoolbus", 0) * 2)
            count_B_1 = (roads1.get("2", {}).get("car", 0) + roads1.get("2", {}).get("schoolbus", 0) * 2 +
                         roads1.get("4", {}).get("car", 0) + roads1.get("4", {}).get("schoolbus", 0) * 2)
            count_A_2 = (roads2.get("1", {}).get("car", 0) + roads2.get("1", {}).get("schoolbus", 0) * 2 +
                         roads2.get("3", {}).get("car", 0) + roads2.get("3", {}).get("schoolbus", 0) * 2)
            count_B_2 = (roads2.get("2", {}).get("car", 0) + roads2.get("2", {}).get("schoolbus", 0) * 2 +
                         roads2.get("4", {}).get("car", 0) + roads2.get("4", {}).get("schoolbus", 0) * 2)
            overall_A = count_A_1 + count_A_2
            overall_B = count_B_1 + count_B_2
            new_phase = "A" if overall_A >= overall_B else "B"
            results[inter_no]["phase"] = new_phase
            results[adj_inter_no]["phase"] = new_phase

    output = []
    for inter_no, data in results.items():
        phase = data["phase"]
        roads = data["roads"]
        for road_no, counts in roads.items():
            if phase == "A" and road_no in ["1", "3"]:
                signal = "GREEN"
            elif phase == "B" and road_no in ["2", "4"]:
                signal = "GREEN"
            else:
                signal = "RED"
            output.append({
                "intersection": inter_no,
                "road": road_no,
                "cars": counts.get("car", 0),
                "schoolbuses": counts.get("schoolbus", 0),
                "signal": signal
            })
    return output, {k: v["phase"] for k, v in results.items()}
