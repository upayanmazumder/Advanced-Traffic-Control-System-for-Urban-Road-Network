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
                url: 'api.ibreakstuff.uayan.dev',
            }
        ],
        components: {
            schemas: {
                SignalData: {
                    type: "object",
                    properties: {
                        intersection: {
                            type: "integer",
                            example: 2,
                        },
                        road: {
                            type: "string",
                            enum: ["north", "south", "east", "west"],
                            example: "north",
                        },
                        cars: {
                            type: "integer",
                            example: 12,
                        },
                        ambulances: {
                            type: "integer",
                            example: 2,
                        },
                        schoolbuses: {
                            type: "integer",
                            example: 1,
                        },
                        accidents: {
                            type: "integer",
                            example: 0,
                        },
                        signal: {
                            type: "string",
                            enum: ["green", "yellow", "red"],
                            example: "green",
                        },
                    },
                    required: ["intersection", "road", "cars", "signal", "ambulances", "schoolbuses", "accidents"],
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
};