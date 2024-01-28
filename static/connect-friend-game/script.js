async function connect_friend_game(){
    const session_id = document.getElementById("session_id").value; 

    

    await fetch("https://" + document.domain + ':' + location.port + "/connect-friend-game", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: session_id})
    });
}