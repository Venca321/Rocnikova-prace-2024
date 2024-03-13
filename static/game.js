
const urlParams = new URLSearchParams(window.location.search);
const socket = io.connect('wss://' + document.domain + ':' + location.port);
let sended = 0;
let received = 0;
let last_user_status = 0;
let user_status = 0;
let user_gesture = 0;
let history = [];
let game_started = undefined;
let win_screen_started = undefined;

socket.on('response', function(data) {
    received += 1;
    if (data.status === "ok" && data.image) {
        console.log("Status: ok", "| Gesture:", data.gesture, "| User status:", data.user_status)
        if (last_user_status == data.user_status){
            user_status = data.user_status;
        }
        last_user_status = data.user_status;
        user_gesture = data.gesture;

        const processedImageElement = document.getElementById('processedImage');
        processedImageElement.src = data.image;

        if (data.user_status === 1) {
            let now = new Date().getTime();
            if (game_started === undefined) {
                game_started = now;
            }

            if (now - game_started > 3000) {
                user_status = 2;
                game_started = undefined;
            }
        }

        if (data.user_status > 2) {
            let now = new Date().getTime();
            if (win_screen_started === undefined) {
                win_screen_started = now;
                history.push({
                    user_gesture: user_gesture, user_status: user_status, 
                    bot_gesture: data.bot_gesture
                });

                const winScreenTextElement = document.getElementById('win-screen-text');
                winScreenTextElement.innerText = `${data.user_status_text}`

                const winScreenElement = document.getElementById('win-screen');
                winScreenElement.classList.add("win-screen-show")
            }

            if (now - win_screen_started > 1500) {
                user_status = 0;
                win_screen_started = undefined;
                game_started = undefined;

                const winScreenElement = document.getElementById('win-screen');
                winScreenElement.classList.remove("win-screen-show")
            }
        }

        const statusTextElement = document.getElementById('status-text');
        statusTextElement.textContent = `Stav: ${data.user_status_text},`;
        const gestureTextElement = document.getElementById('gesture-text');
        gestureTextElement.textContent = `Gesto: ${data.gesture_text}`;
    } else {
        console.error("Status:", data.status);
    }
});

function captureAndSendImage() {
    const video = document.querySelector('video');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    video_res = [video.videoWidth, video.videoHeight]
    canvas.getContext('2d').drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    if (sended -1 <= received) {
        socket.emit('image', {
            flip: urlParams.get("flip"), user_status: user_status, 
            gesture: user_gesture, history: history, 
            image: canvas.toDataURL('image/jpeg')
        });
        sended += 1;
    }
}

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true }) // get permission
    .then(() => navigator.mediaDevices.enumerateDevices())
    .then(devices => {
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
    
        if (videoDevices.length <= 0){
            throw new Error('Žádná kamera nenalezena.');
        }
        
        const cameraID = Number(urlParams.get('camera'));
        return navigator.mediaDevices.getUserMedia({ 
            video: { 
                deviceId: videoDevices[cameraID].deviceId,
                width: { ideal: 640 },
                height: { ideal: 480 }
            } 
        });
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
    if (!urlParams.has('flip')){
        if (location.href.includes("?")) {
            location.href = window.location.search + `&flip=true`;
        } else {
            location.href = `?flip=true`;
        }
    }

    if (!urlParams.has('camera')){
        if (location.href.includes("?")) {
            location.href = window.location.search + `&camera=0`;
        } else {
            location.href = `?camera=0`;
        }
    }

    startCamera();
});