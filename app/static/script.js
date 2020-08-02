(function (){
	var width = 350;  // scaling the photo width to this
	var height = 0;  // this will use the height of input stream 

	var streaming = false ;

	var photo = null;
	var video = null;
	var captureButton  = null;
	var canvas = null;
	var inputfile = null;



	function startup(){
		video = document.getElementById('video');
		photo = document.getElementById('photo');
		captureButton = document.getElementById('captureButton');
		canvas = document.getElementById('canvas');
		inputfile = document.getElementById('b64');

		navigator.mediaDevices.getUserMedia({video: true, audio: false}).then(stream=>{
			video.srcObject = stream;
			video.play();
		}).catch(err=>{
			console.log("An error occured: "+err);
		});
	

	video.addEventListener('canplay', ev=>{
		if(!streaming){
			height = video.videoHeight / (video.videoWidth/width);

			video.setAttribute('width', width)
			video.setAttribute('height', height)
			canvas.setAttribute('width', width)
			canvas.setAttribute('height', height)
			streaming = true
		}
	}, false);

	captureButton.addEventListener('click', ev=>{
		takePicture();
		ev.preventDefault();
	}, false);

	clearPhoto();

}


function clearPhoto(){
	var contxt = canvas.getContext('2d');
	contxt.fillStyle = "#AAA";
	contxt.fillRect(0, 0, canvas.width, canvas.height);

	var data = canvas.toDataURL('image/png');
	photo.setAttribute('src', data);
	inputfile.setAttribute('value', data);
	console.log(data)
}

function takePicture(){
	var contxt = canvas.getContext('2d');
	if (width && height){
		canvas.width = width;
		canvas.height = height;
		contxt.drawImage(video, 0, 0, width, height);

		var data = canvas.toDataURL('image/png');
		photo.setAttribute('src', data);
		inputfile.setAttribute('value', data);
	}else{
		clearPhoto
	}
}


window.addEventListener('load', startup, false)

})();