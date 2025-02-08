import Signal from "../models/SignalData.js";

async function getAccidentData(req, res) {
    try {
        const response = await Signal.where("accidents").gte(1)
            .find()
            .select("intersection location road accidents -_id");

        if (response.length === 0) {
            return res.status(404).json({
                count: 0,
                accidents: [],
            });
        }
        
        res.json({
            count: response.length,
            accidents: response,
        });
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

export {
    getAccidentData,
}