const gifFrames = require('gif-frames');
const Jimp = require('jimp');
const fs = require('fs/promises');

// Input GIF file path
const inputGifPath = 'C:\\Users\\william\\Documents\\GitHub\\Cv3D\\CV3D Meta Prompts for Build\\LOGSiTE\\trip-love.gif';

// Output directory for PNG frames
const outputDirectory = 'animated-favicon';
const sharp = require('sharp');

// Function to generate boundary points based on a polar curve
async function generateBoundaryPoints(frameIndex, totalFrames) {
    const boundaryPoints = [];
    const polarCurve = async (theta) => {
        // Modify the polar curve equation as needed
        const r = 100 + 50 * Math.sin(theta * 4 * Math.PI * frameIndex / totalFrames);
        return { x: r * Math.cos(theta), y: r * Math.sin(theta) };
    };

    const numPoints = 360; // Number of points on the curve
    for (let i = 0; i < numPoints; i++) {
        const theta = (i / numPoints) * 2 * Math.PI;
        const { x, y } = await polarCurve(theta);

        // Use sharp to create a transparent circle image
        const circleRadius = 50;
        const image = sharp({ create: { width: 2 * circleRadius, height: 2 * circleRadius, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } } });
        const circleImage = await image.circle({ radius: circleRadius }).toBuffer();

        boundaryPoints.push({ x, y, circleImage });
    }

    return boundaryPoints;
}

module.exports = generateBoundaryPoints;


(async () => {
    try {
        const frameData = await gifFrames({ url: inputGifPath, frames: 'all', outputType: 'png' });

        // Ensure the output directory exists
        await fs.mkdir(outputDirectory, { recursive: true });

        for (const [index, frame] of frameData.entries()) {
            const circleRadius = 50;

            const image = await Jimp.read(frame.getImage());
            const circleImage = new Jimp(2 * circleRadius, 2 * circleRadius, (err, circle) => {
                if (err) throw err;
                circle.circle({ radius: circleRadius });
            });

            const clippedImage = image.clone();
            clippedImage.blit(circleImage, 0, 0);

            const outputImagePath = `${outputDirectory}/frame_${index + 1}.png`;
            await clippedImage.writeAsync(outputImagePath);

            console.log(`Frame ${index + 1} saved.`);
        }

        console.log('Frames extracted and saved.');
    } catch (error) {
        console.error('Error:', error);
    }
})();
