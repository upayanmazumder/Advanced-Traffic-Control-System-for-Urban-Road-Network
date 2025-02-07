import express from "express";
import { getTrafficData } from "../controllers/aiTrafficData.js";

const router = express.Router();

router.get("/signal-data", getTrafficData);

export default router;