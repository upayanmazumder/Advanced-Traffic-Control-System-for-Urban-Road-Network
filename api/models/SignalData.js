import mongoose from "mongoose";

const coordinateSchema = new mongoose.Schema({
    direction: {
      type: String,
      enum: ['N', 'S', 'E', 'W'],
      required: true,
    },
    degrees: {
      type: Number,
      required: true,
      validate: {
        validator: function (value) {
          return (this.direction === 'N' || this.direction === 'S')
            ? value >= 0 && value <= 90
            : value >= 0 && value <= 180;
        },
        message: props => `${props.value} is out of range for degrees.`,
      },
    },
    minutes: {
      type: Number,
      required: true,
      min: 0,
      max: 59,
    },
    seconds: {
      type: Number,
      required: true,
      min: 0,
      max: 59.999,
    },
});

const locationSchema = new mongoose.Schema({
    latitude: {
        type: coordinateSchema,
        required: true,
        validate: {
            validator: function(value) {
                return (value.direction === 'N' || value.direction === 'S');
            },
        },
    },
    longitude: {
        type: coordinateSchema,
        required: true,
        validate: {
            validator: function(value) {
                return (value.direction === 'E' || value.direction === 'W');
            },
        },
    },
});

const SignalSchema = new mongoose.Schema(
    {
        intersection: {
            type: Number,
            min: 1,
            required: true,
        },
        location: {
            type: locationSchema,
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
            required: false,
        },
        ambulances: {
            type: Number,
            min: 0,
            required: false,
        },
        schoolbuses: {
            type: Number,
            min: 0,
            required: false,
        },
        accidents: {
            type: Number,
            min: 0,
            required: false,
        },
        signal: {
            type: String,
            enum: ['green', 'yellow', 'red'],
            required: false,
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