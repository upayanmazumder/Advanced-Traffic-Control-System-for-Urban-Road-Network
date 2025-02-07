import Signal from "../models/SignalData.js";

async function getTrafficData(req, res) {
    const { intersection } = req.body;

    try {
        var response;
        if (intersection) {
            response = await Signal.where("intersection").equals(intersection)
                .find()
                .select("intersection road cars signal -_id");
        } else {
            response = await Signal.find()
                .select("intersection road cars signal -_id");
        }
        if (response.length === 0) {
            return res.status(404).json({
                rows: 0,
                data: [],
            });
        } else {
            return res.json({
                rows: response.length,
                data: response,
            });
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
                filter: { intersection: signal.intersection, road: signal.road },
                update: { 
                    $set: { cars: signal.cars, signal: signal.signal } // Update both fields
                },
                upsert: true, // Insert if not found
            }
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