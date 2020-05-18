var userId = document.querySelector("#ID");
var overlap = document.querySelector("#overlap");
var overlapjs = document.querySelector("#overlap_check");

// 아이디 중복을 확인하지 않고 form이 넘어가게 되는 경우에 알림창 표시
if (overlapjs.value == "false") {
    alert("ID 중복 확인을 해주세요.")
}

overlap.onclick = overlapF;
userId.onchange = checkId;

function overlapF() {
    var h = location.protocol + "//" + location.hostname + "/overlap/";

    if (userId.value == "") {
        alert("ID를 입력하세요.");
        userId.focus();
    } else {
        // 개발용 서버
        // window.open(
        //     "http://127.0.0.1:8000/overlap/" + userId.value,
        //     "_self",
        //     "",
        //     false
        // );

        // 시연용 서버
        window.open(
                "https://51635f05.ngrok.io/overlap/" + userId.value,
                "_self",
                "",
                false
        );
    }
}

function checkId() {
    if (userId.value.length < 4 || userId.value.length > 15) {
        alert("4~15자리의 영문과 숫자를 사용하세요.");
        userId.value = "";
        userId.focus();
    }
}

var pw1 = document.querySelector("#PW");
var pw2 = document.querySelector("#PWC");

pw1.onchange = checkPw;
pw2.onchange = comparePw;

function checkPw() {
    if (pw1.value.length < 8) {
        alert("비밀번호는 8자리 이상이어야 합니다.");
        pw1.value = "";
        pw1.focus();
    }
}

function comparePw() {
    if (pw1.value != pw2.value) {
        alert("암호가 다릅니다. 다시 입력하세요.");
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