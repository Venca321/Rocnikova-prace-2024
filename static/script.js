
const socket = io.connect('ws://' + document.domain + ':' + location.port);
const urlParams = new URLSearchParams(window.location.search);

socket.on('response', function(data) {
    console.log(data);
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
    navigator.mediaDevices.enumerateDevices()
        .then(function(devices) {
            const videoDevices = devices.filter(function(device) {
                return device.kind === 'videoinput';
            });

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
                setInterval(captureAndSendImage, 250); // Snímek každých xxx ms
            };
        })
        .catch(function(err) {
            console.log(err);
        });
}

window.addEventListener("load", (event) => {
    startCamera();
});