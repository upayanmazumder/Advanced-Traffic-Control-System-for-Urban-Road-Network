import jwt from "jsonwebtoken";

async function verifyToken(req, res, next) {
    const authorizationHeader = req.header('Authorization');

    if (!authorizationHeader) {
        return res.status(401).json({
            status: "failure",
            error: "Missing access token",
        });
    }

    const tokenParts = authorizationHeader.split(' ');
    if (tokenParts.length < 2 || tokenParts[0] !== 'Bearer') {
        return res.status(401).json({
            status: "failure",
            error: "Invalid Authorization header format",
        });
    }

    const accessToken = tokenParts[1];

    try {
        const decodedUser = jwt.verify(accessToken, process.env.JWT_ACCESSTOKEN_SECRET);
        console.log(decodedUser);
        req.user = {
            username: decodedUser.username,
        }
        next();
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

export {
    verifyToken,
}