const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const sharp = require('sharp'); // Import sharp for image processing
const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// Set the path to the directory containing the logs
const logsDirectory = path.join(__dirname, 'LOGSiT');

// Ensure the directory exists
if (!fs.existsSync(logsDirectory)) {
    fs.mkdirSync(logsDirectory);
}

// Function to create a stream for overlaying a boundary on the favicon using sharp
function createFaviconOverlayStream(options) {
    const { Transform } = require('stream'); // Import Transform from 'stream'

    const stream = new Transform();

    stream._transform = async function (chunk, encoding, done) {
        try {
            const image = await sharp(chunk);
            const favicon = await image.clone().resize(16, 16).toBuffer(); // Adjust the size as needed

            // Draw the boundary on the favicon
            for (let i = 0; i < favicon.length; i += 4) {
                const x = (i / 4) % 16;
                const y = Math.floor((i / 4) / 16);
                const pointInsideBoundary = isPointInsideBoundary({ x, y }, options.boundaryPoints);

                if (pointInsideBoundary) {
                    // Set the pixel color to the boundary color
                    favicon[i] = (options.boundaryColor >> 24) & 0xFF; // Red
                    favicon[i + 1] = (options.boundaryColor >> 16) & 0xFF; // Green
                    favicon[i + 2] = (options.boundaryColor >> 8) & 0xFF;  // Blue
                    favicon[i + 3] = options.boundaryColor & 0xFF;         // Alpha
                } else if (options.backgroundColor !== undefined) {
                    // Set the pixel color to the background color if specified
                    favicon[i] = (options.backgroundColor >> 24) & 0xFF; // Red
                    favicon[i + 1] = (options.backgroundColor >> 16) & 0xFF; // Green
                    favicon[i + 2] = (options.backgroundColor >> 8) & 0xFF;  // Blue
                    favicon[i + 3] = options.backgroundColor & 0xFF;         // Alpha
                }
            }

            this.push(favicon);
            done();
        } catch (err) {
            console.error(err);
            done();
        }
    };

    return stream;
}

// Function to check if a point is inside the boundary
function isPointInsideBoundary(point, boundaryPoints) {
    const x = point.x;
    const y = point.y;

    let inside = false;
    for (let i = 0, j = boundaryPoints.length - 1; i < boundaryPoints.length; j = i++) {
        const xi = boundaryPoints[i].x;
        const yi = boundaryPoints[i].y;
        const xj = boundaryPoints[j].x;
        const yj = boundaryPoints[j].y;

        const intersect = ((yi > y) !== (yj > y)) &&
            (x < ((xj - xi) * (y - yi)) / (yj - yi) + xi);

        if (intersect) {
            inside = !inside;
        }
    }

    return inside;
}

// Function to generate boundary points based on a polar curve
function generateBoundaryPoints(frameIndex, totalFrames) {
    const boundaryPoints = [];
    const polarCurve = (theta) => {
        // Modify the polar curve equation as needed
        const r = 100 + 50 * Math.sin(theta * 4 * Math.PI * frameIndex / totalFrames);
        return { x: r * Math.cos(theta), y: r * Math.sin(theta) };
    };

    const numPoints = 360; // Number of points on the curve
    for (let i = 0; i < numPoints; i++) {
        const theta = (i / numPoints) * 2 * Math.PI;
        const { x, y } = polarCurve(theta);
        boundaryPoints.push({ x, y });
    }

    return boundaryPoints;
}

// Serve animated favicon
app.get('/favicon.ico', (req, res) => {
    const frameIndex = 1; // Set the frame index based on your logic
    const totalFrames = 100; // Set the total number of frames

    const boundaryPoints = generateBoundaryPoints(frameIndex, totalFrames);

    res.setHeader('Content-Type', 'image/x-icon');
    res.setHeader('Cache-Control', 'public, max-age=86400'); // Cache for 24 hours

    const faviconPath = path.join(__dirname, 'animated-favicon', `frame_${frameIndex}.png`);
    const faviconStream = fs.createReadStream(faviconPath);

    // Overlay the boundary on the favicon
    const overlayOptions = {
        boundaryPoints,
        boundaryColor: 0xFF0000FF, // Red color for the boundary
        backgroundColor: 0x00000000, // Transparent background
    };

    faviconStream.pipe(createFaviconOverlayStream(overlayOptions)).pipe(res);
});
// Serve static files from the LOGSiTE directory
app.use(express.static(__dirname));

// Basic HTML response for the root path
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/saveLog', (req, res) => {
    const logEntry = req.body;
    const logFilePath = path.join(__dirname, 'log.txt');

    console.log('Received log entry:', logEntry);

    fs.appendFile(logFilePath, JSON.stringify(logEntry) + '\n', (err) => {
        if (err) {
            console.error(err);
            res.status(500).send('Error saving log entry');
        } else {
            console.log('Log entry saved successfully');
            res.status(200).send('Log entry saved successfully');
        }
    });
});

// Shutdown handler
function handleShutdown() {
    console.log('Server is shutting down. Performing cleanup...');

    // Save any data or perform cleanup actions here before exiting

    console.log('Cleanup complete. Server is now shutting down.');
    process.exit();
}

// Attach the shutdown handler
process.on('SIGINT', handleShutdown);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
