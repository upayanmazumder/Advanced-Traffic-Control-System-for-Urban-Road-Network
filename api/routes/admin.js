import express from "express";

// import { verifyToken } from "../middleware/verification.js";
import { addSignal, setSignalData, unsetSignalData } from "../controllers/signalOps.js";
import { getTrafficData } from "../controllers/trafficData.js";
import { getAccidentData } from "../controllers/accidentData.js";

const router = express.Router();

router.get("/signal-data", getTrafficData);
router.get("/accident-data", getAccidentData);

router.post("/signal", addSignal);
router.post("/set-signal-data", setSignalData);
router.post("/unset-signal-data", unsetSignalData);

export default router;