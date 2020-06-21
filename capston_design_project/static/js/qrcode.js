var time = "180";
var min = "";
var sec = "";

var x = setInterval(function () {
    min = parseInt(time / 60);
    sec = time % 60;

    document
        .getElementById("time")
        .innerHTML = "Qrcode will be deleted after "+ min + "min" + sec + "sec";
    time--;
    if (time < 0) {
        clearInterval(x);
        document
            .getElementById("time")
            .innerHTML = "시간초과";
        document
            .getElementById("delete")
            .click();
        alert("QRcode가 삭제되었습니다. 다시 발급받아주세요.")
    }
}, 1000);