import express from "express";
import { config } from "dotenv";
import morgan from "morgan";
import mongoose from "mongoose";

import { setupSwagger } from "./swagger.js";
import trafficRoutes from "./routes/traffic.js";

config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('tiny'));

setupSwagger(app);

app.get("/", (req, res) => {
    res.send("Hello World");
});

app.use("/traffic", trafficRoutes);

mongoose
  .connect(process.env.MONGO_URL)
  .then(() => {
    app.listen(port, () => {
      console.log(`Server running at http://localhost:${port}`);
    });
  })
  .catch((error) => console.log(error.message));