window.addEventListener("load", () => {
    navigator.mediaDevices.getUserMedia({ video: true }) // get permission
    .then(() => navigator.mediaDevices.enumerateDevices())
    .then(devices => {
        const videoDevices = devices.filter(device => device.kind === 'videoinput');

        if (videoDevices.length === 0) {
            throw new Error('Žádná kamera nenalezena.');
        }

        const urlParams = new URLSearchParams(window.location.search);
        const deviceList = document.getElementById("deviceList");

        videoDevices.forEach((device, index) => {
            let listItem = document.createElement("li");
            listItem.textContent = device.label || `Kamera ${index + 1}`;
            listItem.onclick = () => location.href = `/game?name=${urlParams.get("name")}&camera=${index}&user_id=${urlParams.get("user_id")}`;
            deviceList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error(error.message);
    });
});