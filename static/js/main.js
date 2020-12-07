$(document).ready(function(){
    var image = document.querySelector('#imageElement');
    if ("WebSocket" in window) {
            var ws = new WebSocket("ws://localhost:8008/ws");
            ws.onopen = function() {
                console.log("Sending websocket data");
            };
            ws.onmessage = function(e) {
                image.setAttribute('src', e.data);
                //alert(e.data);
            };
            ws.onclose = function() {
                console.log("Closing websocket connection");
            };
        } else {
            alert("WS not supported, sorry!");
        }
    function runWebsockets(message) {
        ws.send(message);
    }
	var video = document.querySelector("#videoElement");

	var canvas = document.querySelector('#canvasElement');
    let ctx = canvas.getContext('2d');


	var constraints = {
		video: {
		  width: { min: 640 },
		  height: { min: 480 }
		}
	  };

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {

	  video.srcObject = stream;
	  localMediaStream = stream;

	  setInterval(function () {
		 ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);
		 let dataURL = canvas.toDataURL('image/jpeg', 1.0);
		 runWebsockets(dataURL)
	  }, 50);
	}).catch(function(error) {
	  console.log(error);
	});
})