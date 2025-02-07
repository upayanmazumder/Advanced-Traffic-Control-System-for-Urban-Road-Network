import express from "express";
import { getTrafficData, setTrafficData } from "../controllers/trafficData.js";

const router = express.Router();

/**
 * @swagger
 * /traffic/signal-data:
 *   get:
 *     summary: Get traffic data
 *     description: Retrieves traffic signal data. Optionally, filter by intersection. The response will include data for all roads (north, south, east, west) at the given intersection.
 *     tags:
 *       - Traffic
 *     operationId: getTrafficData
 *     parameters:
 *       - in: query
 *         name: intersection
 *         schema:
 *           type: number
 *           example: 2
 *         description: Intersection to filter traffic data.
 *     responses:
 *       200:
 *         description: Successfully retrieved traffic data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 rows:
 *                   type: integer
 *                   example: 4
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/SignalData'
 *             example:
 *               rows: 4
 *               data:
 *                 - intersection: 2
 *                   road: "north"
 *                   cars: 12
 *                   signal: "green"
 *                 - intersection: 2
 *                   road: "south"
 *                   cars: 8
 *                   signal: "red"
 *                 - intersection: 2
 *                   road: "east"
 *                   cars: 5
 *                   signal: "yellow"
 *                 - intersection: 2
 *                   road: "west"
 *                   cars: 3
 *                   signal: "green"
 *       404:
 *         description: No traffic data found for the given intersection
 *       500:
 *         description: Internal server error
 */
router.get("/signal-data", getTrafficData);

/**
 * @swagger
 * /traffic/signal-data:
 *   post:
 *     summary: Update or insert traffic data
 *     description: Updates traffic signal data or inserts new data if not found.
 *     tags:
 *       - Traffic
 *     operationId: setTrafficData
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               data:
 *                 type: array
 *                 items:
 *                   $ref: '#/components/schemas/SignalData'
 *             example:
 *               data: [
 *                 {
 *                   intersection: 2,
 *                   road: "north",
 *                   cars: 12,
 *                   signal: "green"
 *                 }
 *               ]
 *     responses:
 *       204:
 *         description: Traffic data successfully updated or inserted
 *       400:
 *         description: Invalid request, expected an array
 *       500:
 *         description: Internal server error
 */
router.post("/signal-data", setTrafficData);

export default router;