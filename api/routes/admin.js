import express from "express";

import { verifyToken } from "../middleware/verification.js";
import { addSignal, setSignalData, unsetSignalData } from "../controllers/signalOps.js";
import { getTrafficData } from "../controllers/trafficData.js";
import { getAccidentData } from "../controllers/accidentData.js";

const router = express.Router();

router.get("/signal-data", verifyToken, getTrafficData);
router.get("/accident-data", verifyToken, getAccidentData);

router.post("/signal", verifyToken, addSignal);
router.post("/set-signal-data", verifyToken, setSignalData);
router.post("/unset-signal-data", verifyToken, unsetSignalData);

export default router;