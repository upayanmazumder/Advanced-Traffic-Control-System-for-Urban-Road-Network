import Signal from "../models/SignalData.js";

function transformData(data) {
    let result = {};
    let count = 0;

    data.forEach(({ intersection, location, road, cars, ambulances, schoolbuses, accidents, signal }) => {
        if (!result[intersection]) {
            count++;
            result[intersection] = {
                location,
                vehicles: {}
            };
        }

        if (!result[intersection].green && signal) {
            if (road === "north" || road === "south") {
                result[intersection].green = (signal === "GREEN")?'n-s':'e-w';
            } else if (road === "east" || road === "west") {
                result[intersection].green = (signal === "GREEN")?'e-w':'n-s';
            }
        }
        
        result[intersection].vehicles[road] = { cars, ambulances, schoolbuses, accidents };
    });
    
    return {
        intersections: count,
        data: result,
    };
}

async function getTrafficData(req, res) {
    const { intersection } = req.query;

    try {
        var response;
        if (intersection) {
            response = await Signal.where("intersection").equals(intersection)
                .find()
                .select("intersection location road cars ambulances schoolbuses accidents signal -_id");
        } else {
            response = await Signal.find()
                .select("intersection location road cars ambulances schoolbuses accidents signal -_id");
        }
        if (response.length === 0) {
            return res.status(404).json({
                intersections: 0,
            });
        } else {
            return res.json(transformData(response));
        }
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

async function setTrafficData(req, res) {
    const { data } = req.body;
    if (!data || !Array.isArray(data)) {
        return res.status(400).json({
            error: "array argument expected",
        });
    }
    if (data.length === 0) {
        return res.sendStatus(204);
    }

    try {
        const bulkOps = data.map(signal => ({
            updateOne: {
                filter: { intersection: signal.intersection, road: signal.road, manuallyOverridden: false },
                update: { 
                    $set: { cars: signal.cars, ambulances: signal.ambulances, schoolbuses: signal.schoolbuses, accidents: signal.accidents, signal: signal.signal } // Update all fields
                },
                upsert: false, //donot insert if not found
            },
        }));
        await Signal.bulkWrite(bulkOps);

        return res.sendStatus(204);
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

export {
    getTrafficData,
    setTrafficData,
}