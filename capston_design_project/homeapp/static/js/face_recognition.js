var camStreamWidth = 640;
var camStreamHeight = 480;

var VIEW_WIDTH = 320;
var VIEW_HEIGHT = 240;

var video = document.getElementById("video");
var canvas = document.getElementById("canvas");

canvas.width = VIEW_WIDTH;
canvas.height = VIEW_HEIGHT;

var webcamParams = {
    video: {
        mandatory: {
            maxWidth: camStreamWidth,
            maxHeight: camStreamHeight,
            minWidth: camStreamWidth,
            minHeight: camStreamHeight
        }
    }
};

var webcamMgr = new WebCamManager({
    webcamParams: webcamParams, //Set params for web camera
    testVideoMode: false, //true:force use example video for test false:use web camera
    videoTag: video
});

var faceDetector = new FaceDetector(
    {video: webcamMgr.getVideoTag(), flipLeftRight: false, flipUpsideDown: false}
);

webcamMgr.setOnGetUserMediaCallback(function () {
    faceDetector.startDetecting();
});

faceDetector.setOnFaceAddedCallback(function (addedFaces, detectedFaces) {
    for (var i = 0; i < addedFaces.length; i++) {
        console.log(
            "[facedetector] New face detected id=" + addedFaces[i].faceId + " index=" +
            addedFaces[i].faceIndex
        );
    }
});

faceDetector.setOnFaceLostCallback(function (lostFaces, detectedFaces) {

    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, VIEW_WIDTH, VIEW_HEIGHT);

    for (var i = 0; i < lostFaces.length; i++) {
        console.log(
            "[facedetector] Face removed id=" + lostFaces[i].faceId + " index=" +
            lostFaces[i].faceIndex
        );
    }

});

faceDetector.setOnFaceUpdatedCallback(function (detectedFaces) {

    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, VIEW_WIDTH, VIEW_HEIGHT);

    ctx.strokeStyle = "red";
    ctx.lineWidth = 3;
    ctx.fillStyle = "red";
    ctx.font = "italic small-caps bold 20px arial";

    for (var i = 0; i < detectedFaces.length; i++) {

        var face = detectedFaces[i];

        ctx.fillText(face.faceId, face.x * VIEW_WIDTH, face.y * VIEW_HEIGHT);
        ctx.strokeRect(
            face.x * VIEW_WIDTH,
            face.y * VIEW_HEIGHT + 10,
            face.width * VIEW_WIDTH,
            face.height * VIEW_HEIGHT
        );

    }
});

webcamMgr.startCamera();
