var already_status = document.querySelector("#already_status");
var send_ok = document.querySelector('#send_ok');
var accept_ok = document.querySelector('#accept_ok');
var superuser_no = document.querySelector('#superuser_no');

if (already_status.value == "lock"){
    alert("Already Lock");
} else if (already_status.value == "unlock"){
    alert("Already Unlock");
}

if (send_ok.value == "send_ok"){
    alert("Invitation message send sucessfully!!");
}

if (accept_ok.value == "accept_ok"){
    alert("Your account can access to control device!!");
}

if (superuser_no.value == "superuser_no"){
    alert("Superuser can be deleted");
}