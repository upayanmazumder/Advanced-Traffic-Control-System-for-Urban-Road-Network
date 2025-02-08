import express from "express";
import { config } from "dotenv";
import morgan from "morgan";
import mongoose from "mongoose";
import cors from "cors";

import trafficRoutes from "./routes/traffic.js";
import adminRoutes from "./routes/admin.js";

config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('tiny'));

app.get("/", (req, res) => {
    res.send("Hello World");
});

app.use("/traffic", trafficRoutes);
app.use("/admin", adminRoutes);
// app.use("/auth", authRoutes);

mongoose
  .connect(process.env.MONGO_URL)
  .then(() => {
    app.listen(port, () => {
      console.log(`Server running at http://localhost:${port}`);
    });
  })
  .catch((error) => console.log(error.message));