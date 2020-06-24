var userId = document.querySelector("#ID");
var pw1 = document.querySelector("#PW");
var pw2 = document.querySelector("#PWC");

var overlap = document.querySelector("#overlap");
var overlap_check = document.querySelector("#overlap_check");
var overlap_alert = document.querySelector("#overlap_alert");

overlap.onclick = overlapF;
userId.onchange = checkId;
pw1.onchange = checkPw;
pw2.onchange = comparePw;

// 아이디 중복확인을 위해 django의 urls.py의 overlap으로 연결
function overlapF() {
    var h = location.protocol + "//" + location.host + "/overlap/";
    if (userId.value == "") {
        alert("Input your ID correctly!!");
        userId.focus();
    } else {
        window.open(
            h + userId.value,
            "_self",
            "",
            false
        );
    }
}

// 아이디 중복 확인 버튼을 누르고 overlap_check.value를 받고 알려주는 기능
if (overlap_check.value == "true") {
    alert("Available to use this ID!!");
} else if (overlap_check.value == "false") {
    alert("Unavailable to use this ID!!");
}

// 아이디 중복을 확인하지 않고 form이 넘어가게 되는 경우에 알림창 표시
if (overlap_alert.value == "false") {
    alert("Check to use this ID!!");
}

// 4~15자리의 영문과 숫자를 사용하세요.
function checkId() {
    if (userId.value.length < 4 || userId.value.length > 15) {
        alert("Use 4 to 15 digits of English and numbers!!");
        userId.value = "";
        userId.focus();
    }
}

// 비밀번호는 8자리 이상이어야 합니다.
function checkPw() {
    if (pw1.value.length < 8) {
        alert("Password must be at least 8 digits!!");
        pw1.value = "";
        pw1.focus();
    }
}

// 암호가 다릅니다. 다시 입력하세요.
function comparePw() {
    if (pw1.value != pw2.value) {
        alert("Passwords are different. Please re-input!!");
        pw2.value = "";
        pw2.focus();
    }
}

function numkeyCheck(e) {
    var keyValue = event.keyCode;
    if (((keyValue >= 48) && (keyValue <= 57))) {
        return true;
    } else {
        return false;
    }
}