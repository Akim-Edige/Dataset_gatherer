const video = document.getElementById('video');
const captureBtn = document.getElementById('capture-btn');
const recordBtn = document.getElementById('record-btn');
const signSelect = document.getElementById('sign-select');
const annotatedImage = document.getElementById('annotated-image');
const originalImage = document.getElementById('original-image');
const annotatedContainer = document.getElementById('annotated-container');
const originalContainer = document.getElementById('original-container');
const spinner = document.getElementById('spinner');
const saveBtn = document.getElementById('save-btn');
const retakeBtn = document.getElementById('retake-btn');

let mediaRecorder;
let recordedChunks = [];
let currentAnnotatedImage = null;
let currentOriginalImage = null;
let currentKeypoints = null;

// Access the webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing webcam: ", err);
    });

// Capture Image
captureBtn.addEventListener('click', () => {
    const selectedSign = signSelect.value;
    if (!selectedSign) {
        alert("Please select a sign.");
        return;
    }

    // Take a snapshot from the video stream
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');

    // Show spinner
    spinner.style.display = 'block';

    // Send the image to the server for processing
    fetch('/capture_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataURL, sign: selectedSign })
    })
    .then(response => response.json())
    .then(data => {
        // Hide spinner
        spinner.style.display = 'none';

        if (data.annotated_image && data.original_image) {
            // Display the original image
            originalImage.src = data.original_image;
            originalContainer.style.display = 'block';

            // Display the annotated image
            annotatedImage.src = data.annotated_image;
            annotatedContainer.style.display = 'block';
            currentAnnotatedImage = data.annotated_image;
            currentOriginalImage = data.original_image;
            currentKeypoints = data.keypoints;
        } else {
            originalImage.src = "";
            annotatedImage.src = "";
            originalContainer.style.display = 'none';
            annotatedContainer.style.display = 'none';
            alert("No hands detected or failed to process the image. Please try again.");
        }
    })
    .catch(err => {
        // Hide spinner
        spinner.style.display = 'none';
        console.error("Error processing image: ", err);
        alert("An error occurred while processing the image. Please try again.");
    });
});

// Save Image
saveBtn.addEventListener('click', () => {
    const selectedSign = signSelect.value;
    if (!selectedSign) {
        alert("Sign not selected. Please select a sign.");
        return;
    }
    if (!currentAnnotatedImage || !currentOriginalImage || !currentKeypoints) {
        alert("No image to save.");
        return;
    }

    // Send the images and keypoints to the server to save
    fetch('/save_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            original_image: currentOriginalImage,
            annotated_image: currentAnnotatedImage,
            sign: selectedSign,
            keypoints: currentKeypoints
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Reset the images
        originalImage.src = "";
        annotatedImage.src = "";
        originalContainer.style.display = 'none';
        annotatedContainer.style.display = 'none';
        currentAnnotatedImage = null;
        currentOriginalImage = null;
        currentKeypoints = null;
    })
    .catch(err => {
        console.error("Error saving images: ", err);
        alert("An error occurred while saving the images. Please try again.");
    });
});

// Retake Image
retakeBtn.addEventListener('click', () => {
    // Clear the images and allow user to take a new photo
    originalImage.src = "";
    annotatedImage.src = "";
    originalContainer.style.display = 'none';
    annotatedContainer.style.display = 'none';
    currentAnnotatedImage = null;
    currentOriginalImage = null;
    currentKeypoints = null;
});

// Record Video (Existing Implementation)
recordBtn.addEventListener('click', () => {
    const selectedSign = signSelect.value;
    if (!selectedSign) {
        alert("Please select a sign.");
        return;
    }

    if (recordBtn.textContent === "Start Recording") {
        recordedChunks = [];
        mediaRecorder = new MediaRecorder(video.srcObject);
        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };
        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => {
                const base64data = reader.result;
                fetch('/capture_video', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ video: base64data, sign: selectedSign })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                })
                .catch(err => {
                    console.error("Error sending video: ", err);
                });
            };
        };
        mediaRecorder.start();
        recordBtn.textContent = "Stop Recording";
    } else {
        mediaRecorder.stop();
        recordBtn.textContent = "Start Recording";
    }
});
