import Signal from "../models/SignalData.js";

async function addSignal(req, res) {
    const { intersection, latitude, longitude } = req.body;
    if (!intersection || !latitude || !longitude) {
        return res.status(400).json({
            error: "Missing request parameters",
        });
    }

    try {
        const signals = [];
        const location = { latitude, longitude };
        const roads = ['north', 'south', 'east', 'west'];
        roads.forEach((road) => {
            signals.push({ intersection, location, road });
        });

        await Signal.insertMany(signals);

        return res.sendStatus(204);
    } catch (error) {
        if (error.message === `E11000 duplicate key error collection: test.signals index: intersection_1_road_1 dup key: { intersection: ${intersection}, road: \"north\" }`) {
            res.status(400).json({
                error: "Intersection number must be unique",
            });
        } else {
            res.status(500).json({
                error: error.message,
            });
        }
    }
}

async function setSignalData(req, res) {
    const { intersection, direction, light } = req.body;
    const oppLight = (light === 'GREEN')?'RED':'GREEN';
    if (!intersection || !direction || !light) {
        return res.status(400).json({
            error: "Missing request parameters",
        });
    }
    if ((direction != 'n-s' && direction != 'e-w') || (light != 'GREEN' && light != 'RED')) {
        return res.status(400).json({
            error: "Invalid request parameters",
        });
    }

    try {
        const road1 = (direction === 'n-s')?"north":"east";
        const road2 = (direction === 'n-s')?"south":"west";

        const signals = await Signal.where("intersection").equals(intersection)
            .find();
        signals.forEach((signal) => {
            signal.signal = (signal.road === road1 || signal.road === road2)?light:oppLight;
        });

        const bulkOps = signals.map(signal => ({
            updateOne: {
                filter: { intersection: signal.intersection, road: signal.road },
                update: {
                    $set: { signal: signal.signal, manuallyOverridden: true },
                },
                upsert: false, //donot insert a new record if match is not found
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

async function unsetSignalData(req, res) {
    const { intersection } = req.body;
    if (!intersection) {
        return res.status(400).json({
            error: "Missing request parameters",
        });
    }

    try {
        await Signal.updateMany(
            { intersection, manuallyOverridden: true },
            { $set: { manuallyOverridden: false } },
            { upsert: false },
        );

        res.sendStatus(204);
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

export {
    addSignal,
    setSignalData,
    unsetSignalData,
}