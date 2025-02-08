import mongoose from "mongoose";

const SignalSchema = new mongoose.Schema(
    {
        intersection: {
            type: Number,
            min: 1,
            required: true,
        },
        road: {
            type: String,
            enum: ['north', 'south', 'east', 'west'],
            required: true,
        },
        cars: {
            type: Number,
            min: 0,
            required: true,
        },
        ambulances: {
            type: Number,
            min: 0,
            required: true,
        },
        schoolbuses: {
            type: Number,
            min: 0,
            required: true,
        },
        accidents: {
            type: Number,
            min: 0,
            required: true,
        },
        signal: {
            type: String,
            enum: ['green', 'yellow', 'red'],
            required: true,
        },
        manuallyOverridden: {
            type: Boolean,
            default: false,
            required: true,
        },
    },
);

SignalSchema.index({ intersection: 1, road: 1 }, { unique: true }); //unique intersection and road combination

const Signal = mongoose.model("Signal", SignalSchema);

export default Signal;