
const urlParams = new URLSearchParams(window.location.search);
const socket = io.connect('wss://' + document.domain + ':' + location.port);

socket.on('response', function(data) {
    if (data.status === "ok" && data.image) {
        console.log("Status: ok")
        const processedImageElement = document.getElementById('processedImage');
        processedImageElement.src = data.image;
    } else {
        console.error("Nepodařilo se získat zpracovaný obrázek.");
    }
});

function captureAndSendImage() {
    const video = document.querySelector('video');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    socket.emit('image_navigation', { image: canvas.toDataURL('image/jpeg')});
}

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true }) // get permission
    .then(() => navigator.mediaDevices.enumerateDevices())
    .then(devices => {
        const videoDevices = devices.filter(device => device.kind === 'videoinput');

        if (videoDevices.length <= 0){
            throw new Error('Žádná kamera nenalezena.');
        }
        
        if (urlParams.has('camera')){
            const cameraID = Number(urlParams.get('camera'));
            return navigator.mediaDevices.getUserMedia({ video: { deviceId: videoDevices[cameraID].deviceId } });
        }
        else {
            location.href = `?camera=0`;
        }
    })
    .then(function(stream) {
        const video = document.querySelector('video');
        video.srcObject = stream;
        video.onloadedmetadata = function(e) {
            video.play();
            setInterval(captureAndSendImage, 100); // Snímek každých xxx ms
        };
    })
    .catch(function(err) {
        console.log(err);
    });
}

window.addEventListener("load", (event) => {
    startCamera();
});