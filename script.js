
const connection = new signalR.HubConnectionBuilder()
    .withUrl("https://localhost:5000/Detection?type=flutter")
    .build();

let currentFrameChunks = [];
let expectedChunks = 0;

connection.on("ReceiveFrame", function (chunk, index, totalChunks) {
    console.log('here')
    if (index === 0) {
        // Start of a new frame
        currentFrameChunks = [];
        expectedChunks = totalChunks;
    }

    currentFrameChunks[index] = chunk;

    if (currentFrameChunks.length === expectedChunks && currentFrameChunks.every(c => c !== undefined)) {
        // All chunks received, assemble the frame
        const frameBase64 = currentFrameChunks.join('');
        currentFrameChunks = [];  // reset for next frame

        const img = document.getElementById("videoStream");
        img.src = 'data:image/jpeg;base64,' + frameBase64;
    }
});

connection.start().then(function () {
    console.log("Connected to SignalR hub");
}).catch(function (err) {
    return console.error(err.toString());
});