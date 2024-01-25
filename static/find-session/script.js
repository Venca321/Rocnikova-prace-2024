async function register(name){
    response = await fetch("https://" + document.domain + ':' + location.port + "/register", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: name})
    });
    data = await response.json();
    return data.user_id;
}

async function connect_session(user_id){
    response = await fetch("https://" + document.domain + ':' + location.port + "/find-random-session", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id: user_id})
    });
    data = await response.json();
    return data.session_id;
}

async function joinRandom() {
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get('name');
    const user_id = await register(name);

    console.log(user_id);
    console.log(await connect_session(user_id));

    location.href = `/game?name=${name}&user_id=${user_id}`;
}