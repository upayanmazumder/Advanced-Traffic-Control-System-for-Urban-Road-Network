import spawn from "cross-spawn";

function getTrafficData(req, res) {
    try {
        const process = spawn('python', ['main.py'], {
            cwd: '../AI',
        });

        process.stdout.on('data', (data) => {
            const consoleData = data.toString();

            if (consoleData[0] === '[') {
                res.json({
                    data: eval(consoleData),
                });
                process.kill();
            }
        });

        process.stderr.on('data', (data) => {
            res.status(500).json({
                error: data.toString(),
            });
            process.kill();
        });

        process.on('error', (error) => {
            res.status(500).json({ error });
            process.kill();
        });

        process.on('exit', (code, signal) => {
            //nothing for now
        });
    } catch (error) {
        res.status(500).json({
            error: error.message,
        });
    }
}

export { getTrafficData };
