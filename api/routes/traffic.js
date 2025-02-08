import express from "express";
import { getTrafficData, setTrafficData } from "../controllers/trafficData.js";

const router = express.Router();

router.get("/signal-data", getTrafficData);
router.post("/signal-data", setTrafficData);

export default router;