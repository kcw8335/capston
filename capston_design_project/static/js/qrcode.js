var time = "180";
var min = "";
var sec = "";

var x = setInterval(function () {
    min = parseInt(time / 60);
    sec = time % 60;

    document
        .getElementById("time")
        .innerHTML = min + "분" + sec + "초 후에 QRcode가 삭제됩니다.";
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