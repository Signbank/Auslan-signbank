var asb_sif_guideButtons = new Array();
asb_sif_guideButtons["SEL"] = new Image(10,10);
asb_sif_guideButtons["SEL"].src = "/static/img/button_showguide_select.gif";
asb_sif_guideButtons["NRM"] = new Image(10,10);
asb_sif_guideButtons["NRM"].src = "/static/img/button_showguide.gif";


function asb_sif_handleGuideToggle(sDiv, sButton) {
	var bVisible = true;
	
	// STEP 1: Determine whether the specified guide is visible or not
		var oGuide = browserKit.getElementById(sDiv);

		if ( oGuide ) {
			if (oGuide.style) {
				bVisible =  (new String(oGuide.style.display).toLowerCase() == "none");
			}
		} else {
			alert("Error! Cannot locate guide. Please try reloading the page by clicking 'refresh' on your web browser.");
			return false;
		}
		
	// STEP 2: Call a method to set the visibility of the specified guide and 
	//         update the "state" of the toggle button
		asb_sif_setGuideDisplay(oGuide, browserKit.getElementById(sButton), bVisible)
	
	// RETURN Success
	return true;
}



function asb_sif_setGuideDisplay(oDiv, oButton, bVisible) {
	// STEP 1: Determine which CSS display attribute to assign, and which image 
	//         to use as the source for the (linked) toggle button
	var sDisplay = "none";
	var sState = "NRM";
	if (bVisible) {
		sDisplay = "block";
		sState = "SEL";
	}

	// STEP 2: Set the display attribute of the specified HTML element as 
	//         appropriate
	if (oDiv) {
		oDiv.style.display = sDisplay;
	}
	
	// STEP 3: Set the appearance of the show/hide button as appropriate
	if (oButton) {
		oButton.src = asb_sif_guideButtons[sState].src;
	}
}