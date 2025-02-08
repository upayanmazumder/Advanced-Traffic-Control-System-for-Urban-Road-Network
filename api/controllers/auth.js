import User from "../models/User.js";
import jwt from "jsonwebtoken";
import bcrypt from "bcrypt";
import { config } from "dotenv";

config();

async function register(req, res) {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).json({
            error: 'Missing request parameters',
        });
    }

    try {
        const response = await User.where("username").equals(username)
            .countDocuments();
        if (response === 1) {
            return res.status(403).json({
                error: "Username already taken",
            });
        }
        const hashedPassword = await bcrypt.hash(password, 10);

        const user = new User({ username, password: hashedPassword });
        await user.save();

        const accessToken = jwt.sign({ username }, process.env.JWT_ACCESSTOKEN_SECRET, { expiresIn: '1d'});
        res.json({
            accessToken,
        });
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

async function login(req, res) {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).json({
            error: "Missing request parameters",
        });
    }

    try {
        const user = await User.where("username").equals(username)
            .findOne()
            .select("password");
        if (!user) {
            return res.status(404).json({
                error: "Username not found",
            });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(403).json({
                error: "Passwords donot match",
            });
        }

        const accessToken = jwt.sign({ username }, process.env.JWT_ACCESSTOKEN_SECRET, { expiresIn: '1d'});
        res.json({
            accessToken,
        });
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

export {
    register,
    login,
}