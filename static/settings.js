
const urlParams = new URLSearchParams(window.location.search);
const socket = io.connect('wss://' + document.domain + ':' + location.port);
let loaded = false;
let video_res = [0, 0]
let sended = 0;
let received = 0;

socket.on('response', function(data) {
    received += 1;
    let cursor = [0, 0];
    if (data.status === "ok" && data.image) {
        console.log("Status: ok")

        if (!loaded && !data.click) {
            loaded = true;
        }

        const buttons = document.querySelectorAll('.button');
        if (data.cursor != null && loaded) {
          cursor = [(window.innerWidth / video_res[0]) * data.cursor[0], (window.innerHeight / video_res[1]) * data.cursor[1]]
        }

        buttons.forEach(button => {
            const rect = button.getBoundingClientRect();
            if (cursor[0] >= rect.left && cursor[0] <= rect.right && cursor[1] >= rect.top && cursor[1] <= rect.bottom) {
                button.classList.add('button_hover');
                if (data.click){
                    const hrefValue = button.getAttribute('onclick');
                    eval(hrefValue);
                }
            } else {
                button.classList.remove('button_hover');
            }            
        });

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
    video_res = [video.videoWidth, video.videoHeight]
    canvas.getContext('2d').drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    if (sended -1 <= received) {
        socket.emit('image_navigation', { flip: urlParams.get("flip"), image: canvas.toDataURL('image/jpeg')});
        sended += 1;
    }
}

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true }) // get permission
    .then(() => navigator.mediaDevices.enumerateDevices())
    .then(devices => {
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        const deviceList = document.getElementById("deviceList");
        videoDevices.forEach((device, index) => {
            let listItem = document.createElement("a");
            listItem.textContent = `Kamera ${index + 1}`;
            listItem.onclick = () => location.href = `?camera=${index}&flip=${urlParams.get("flip")}`;
            listItem.classList.add("button");
            if (index === Number(urlParams.get('camera'))) {
              listItem.classList.add("underline");
            }
            deviceList.appendChild(listItem);
        });

        if (videoDevices.length <= 0){
            throw new Error('Žádná kamera nenalezena.');
        }
        
        const cameraID = Number(urlParams.get('camera'));
        return navigator.mediaDevices.getUserMedia({ video: { deviceId: videoDevices[cameraID].deviceId } });
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