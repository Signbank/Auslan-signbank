
function videosetup(aspectRatio){
	
	var myPlayer = videojs('sign'); 

    function resizeVideoJS(){
        
      // Get the parent element's actual width
      var width = document.getElementById('signbody').offsetWidth;
      // Set width to fill parent element, Set height
      myPlayer.dimensions(width, width * aspectRatio);
    }
    	
    myPlayer.ready(function(){
        resizeVideoJS(); // Initialize the function
        window.onresize = resizeVideoJS; // Call the function on resize
        
        myPlayer.removeChild("bigPlayButton");
        
    	myPlayer.on('fullscreenchange', function(){
    		if(myPlayer.isFullscreen()) {
    			myPlayer.removeClass("vjs-static-controls");
    		} else {
    			myPlayer.addClass("vjs-static-controls");
    		}
    	});
     });
}