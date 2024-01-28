async function connect_friend_game(){
    const session_id = document.getElementById("session_id").value; 
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get('name');

    response = await fetch("https://" + document.domain + ':' + location.port + "/register", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: name})
    });
    data = await response.json();
    const {user_id} = data;

    await fetch("https://" + document.domain + ':' + location.port + "/connect-friend-game", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: session_id, user_id: user_id})
    });

    location.href = `/game?name=${name}&user_id=${user_id}`;
}