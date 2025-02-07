import express from "express";
import morgan from "morgan";

import trafficRoutes from "./routes/traffic.js";

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('tiny'));

app.get("/", (req, res) => {
    res.send("Hello World");
});

app.use("/traffic", trafficRoutes);

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});