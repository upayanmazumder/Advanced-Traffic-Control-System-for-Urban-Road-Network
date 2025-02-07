import swaggerJsdoc from "swagger-jsdoc";
import swaggerUi from "swagger-ui-express";
import { config } from "dotenv";

config();

const options = {
    definition: {
        openapi: "3.0.0",
        info: {
            title: "Traffic API",
            version: "1.0.0",
            description: "API for traffic signal data",
        },
        servers: [
            {
                url: `http://localhost:${process.env.PORT || 3000}`,
            },
            {
                url: 'https://api.ibreakstuff.upayan.dev',
            }
        ],
        components: {
            schemas: {
                SignalData: {
                    type: "object",
                    properties: {
                        intersection: {
                            type: "integer",
                            example: 101,
                        },
                        road: {
                            type: "string",
                            enum: ["north", "south", "east", "west"],
                            example: "north",
                        },
                        cars: {
                            type: "integer",
                            example: 10,
                        },
                        signal: {
                            type: "string",
                            enum: ["green", "yellow", "red"],
                            example: "green",
                        },
                    },
                    required: ["intersection", "road", "cars", "signal"],
                },
            },
        },
    },
    apis: ["./routes/*.js"],
};
const swaggerSpec = swaggerJsdoc(options);

function setupSwagger(app) {
    app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
}

export {
    setupSwagger,
}