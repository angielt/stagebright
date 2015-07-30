
console.log("hey from my_recorder");




function __log(e, data) {
   console.log(e, data);
  //  log.innerHTML += "\n" + e + " " + (data || '');
 }
 var audio_context;
 var recorder;
 var timer;
 var ok_to_start = false;
 function startUserMedia(stream) {
   console.log("startUserMedia")
   var input = audio_context.createMediaStreamSource(stream);
   __log('Media stream created.');
   // Uncomment if you want the audio to feedback directly
   //input.connect(audio_context.destination);
   //__log('Input connected to audio context destination.');

   recorder = new Recorder(input);
   __log('Recorder initialised.');
   ok_to_start = true;
 }
 function startRecording(button) {
  //  document.getElementById("seconds").innerHTML = "00";
  //  document.getElementById("minutes").innerHTML = "00";
  if (ok_to_start === false) {
    alert("Not Recording! Please allow microphone access.");
  }
  else {
   var sec = 0;
   document.getElementById("status").innerHTML = "Recording... ";
   document.getElementById("seconds").innerHTML = "00";
   document.getElementById("colon").innerHTML = ":";
   document.getElementById("minutes").innerHTML = "00";
    function pad(val) {
        return val > 9 ? val : "0" + val;
    }
    timer = setInterval(function () {
        document.getElementById("seconds").innerHTML = pad(++sec % 60);
        document.getElementById("minutes").innerHTML = pad(parseInt(sec / 60, 10));
    }, 1000);



   recorder && recorder.record();
   button.disabled = true;
   button.nextElementSibling.disabled = false;
   __log('Recording...');
 }
 }
 function stopRecording(button) {
   document.getElementById("status").innerHTML = "";
   clearInterval(timer);
   document.getElementById("seconds").innerHTML = "";
   document.getElementById("colon").innerHTML = "";
   document.getElementById("minutes").innerHTML = "";

   recorder && recorder.stop();
   button.disabled = true;
   button.previousElementSibling.disabled = false;
   __log('Stopped recording.');

   // create WAV download link using audio data blob
   createDownloadLink();

   recorder.clear();
 }
 function createDownloadLink() {
   recorder && recorder.exportWAV(function(blob) {
     var url = URL.createObjectURL(blob);
     var li = document.createElement('li');
     var au = document.createElement('audio');
     var hf = document.createElement('a');
     var breakline = document.createElement("br")

     try {
     last_link = document.querySelector("#recordingslist").lastChild.getElementsByTagName("a")[0].getAttribute("download").split(".")[0];
     last_number = parseInt(last_link.slice(-1));
     this_number = last_number + 1;
     }
     catch(err) {
      this_number = 1;
     }

     au.controls = true;
     au.src = url;
     hf.href = url;
    //  hf.download = new Date().toISOString() + 'SpeechBright'+ '.wav';
     hf.download = 'StageBright-'+ this_number+'.wav';


    //  hf.download = new Date().toISOString() + '.wav';
     hf.innerHTML = hf.download;
     li.appendChild(au);
     li.appendChild(hf);
    //  li.appendChild(breakline);
     document.querySelector("#recordingslist").appendChild(li);
   });
 }
 window.onload = function init() {
   try {
     // webkit shim
     window.AudioContext = window.AudioContext || window.webkitAudioContext;
    //  navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
    //  window.URL = window.URL || window.webkitURL;
     navigator.getUserMedia = navigator.webkitGetUserMedia;

     audio_context = new AudioContext;
     __log('Audio context set up.');
     __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
   } catch (e) {
     alert('No web audio support in this browser!');
   }

   navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
     __log('No live audio input: ' + e);
   });
 };


 //
 // setTimeout(function () {
 //     clearInterval(timer);
 // }, 110000);
