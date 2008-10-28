// ==={ "CONSTANT" DEFINITIONS }================================================
var c_asb_fs_pageMode_initializing = 0;
var c_asb_fs_pageMode_view = 1;
var c_asb_fs_pageMode_practice = 2;

var c_asb_fs_pageModeUIMin = c_asb_fs_pageMode_view;
var c_asb_fs_pageModeUIMax = c_asb_fs_pageMode_practice;



// ==={ VARIABLE DEFINITIONS }==================================================
var asb_fs_currentSpeedLink = null;
var asb_fs_pageMode = 0;
var asb_fs_oViewer = null;
var asb_fs_nPlayCount = 0;		// Used to determine whether the current practice word is being shown for the first time.



// ==={ PROCEDURES }============================================================
function asb_fs_setPageMode(eState) {
	var sWrkState, sWrkTabImg, nIdx;

	// STEP 2: Store Page Mode
	asb_fs_pageMode = eState;


	// STEP 1: Synchronise the tab display with the current page mode		
		for (nIdx = c_asb_fs_pageModeUIMin; nIdx <= c_asb_fs_pageModeUIMax; nIdx++) {
			sWrkState = (nIdx == eState) ? "_select" : "";
			sWrkTabImg = "asbFSTabMode" + nIdx;
			if (browserKit.getElementById(sWrkTabImg)) {
				browserKit.lastReturnedObject.src = asb_fs_tabImages[nIdx][sWrkState].src;
			}
		}

	// STEP 2: Hide and Show appropriate layers
		// Determine the correct 'display' property for the DIVs that 
		// belong to each "mode".
		var sTmpInitDisplay = "none";	// This procedure is never used to set the mode to "intializing"
		var sTmpViewDisplay = (eState == c_asb_fs_pageMode_view)? "" : "none";
		var sTmpPracticeDisplay = (eState == c_asb_fs_pageMode_practice)? "" : "none";
	
		// Hide/Show: Initialisation Messages
		if ( browserKit.getElementById("asbFSInitializationMessage") ) {
			browserKit.lastReturnedObject.style.display = sTmpInitDisplay;
		}
		
		//  Hide/Show: View Mode DIVs
		if ( browserKit.getElementById("asbFSViewInput") ) {
			browserKit.lastReturnedObject.style.display = sTmpViewDisplay;
		}
		
		//  Hide/Show: Practice Mode DIVs
		if ( browserKit.getElementById("asbFSPracticeInput") ) {
			browserKit.lastReturnedObject.style.display = sTmpPracticeDisplay;
		}
		if ( browserKit.getElementById("asbFSPracticeResult") ) {
			browserKit.lastReturnedObject.style.display = "none";
		}
		
	// STEP 3: Perform mode-specific intialisation
		if (eState == c_asb_fs_pageMode_view) {
			asb_fs_view_initMode();
		} else if (eState == c_asb_fs_pageMode_practice) {
			asb_fs_practice_viewWord();
		}
}


function asb_fs_initViewer(oAlphabet, sTransitionImageSrc) {
	// Instantiate an FSViewer object to play animations and attach it to the 
	// image that will be used as a placeholder for animation frames.
	if (browserKit.getElementById("imgViewer")) {
		asb_fs_oViewer = new ASB_FSViewer(browserKit.lastReturnedObject, oAlphabet);
		asb_fs_oViewer.onSpellStart = "asb_fs_handleSpellStart";
		asb_fs_oViewer.onSpellFinish = "asb_fs_handleSpellFinish";
	}
	
	// Specify which image to show in transition frames
	asb_fs_oViewer.transitionImageSrc = sTransitionImageSrc;
	
	// Set default speed, and highlight the selected "speed option".
	if (browserKit.getElementById("optSpeed2")) {
		asb_fs_setWordSpeed(browserKit.lastReturnedObject, 1);
	}
}

function asb_fs_view_initMode() {
	if (browserKit.getElementById("txtASBFSViewWord")) {
		if (asb_fs_oViewer) {
			asb_fs_oViewer.setWord(browserKit.lastReturnedObject.value);
		}
	}
}


function asb_fs_view_handleInput(oForm) {
	var sWord = oForm["txtViewWord"].value;

	window.status = "spelling:" + sWord + "... ";
	asb_fs_oViewer.spellWord(sWord);

	return false;	// Prevent the calling form from performing a Submit
}


function asb_fs_practice_viewWord() {
	// STEP 1: Select a random practice word from the list
	var sWord = asb_fs_aPracticeWords[( Math.round(Math.random() * (asb_fs_aPracticeWords.length - 1)) )];
	
	// STEP 2: Initialise Flags
	asb_fs_nPlayCount = 0;
	window.status = "practice mode: " + sWord;

	// STEP 3: Clear the form's input box
	if (browserKit.getElementById("txtASBFSPracticeWord")) {
		var oTmp = browserKit.lastReturnedObject;
		oTmp.value = "(Spelling Word ...)";
		oTmp.disabled = true;
	}

	// STEP 4: Display the word in the viewer
	asb_fs_oViewer.spellWord(sWord);
}


function asb_fs_practice_handleTryAnother() {
	// STEP 1: Display the input form
	if ( browserKit.getElementById("asbFSPracticeResult") ) {
		browserKit.lastReturnedObject.style.display = "none";
	}
	if ( browserKit.getElementById("asbFSPracticeInput") ) {
		browserKit.lastReturnedObject.style.display = "";
	}

	// STEP 2: Select and display another word
	asb_fs_practice_viewWord();
}


function asb_fs_practice_handleResponse(oForm) {
	var sFeedback = "";

	// Get the user's input
	var sWrkResponseRaw = oForm["txtPracticeWord"].value;

	// Eliminate all non alphabetic characters from the user's response
	var sWrkResponse = util_string_getAlphaNumeric(sWrkResponseRaw, true, false);

	// STEP 1: Determine whether the user has actually *seen* all of the word 
	//         spelt yet (i.e. has the animation played at least once?)
		if (asb_fs_nPlayCount < 1) {
			alert("Please wait for all of the letter signs to be displayed before typing an answer");
			return false;
		}
		
	// STEP 2: Ensure the user has provided a reponse of some kind
		if (sWrkResponse.length == 0) {
			alert("Please type the english transation of the signs that were just displayed into the text field. If you wish, you can click the Replay button to see the signs again.");
			return false;
		}
	
	// STEP 3: Determine whether the user's answer was correct or not
		// 3a) Compare only the alpha characters in the word, and the user's 
		//     response (ignore hyphens, spaces and other characters that 
		//     cannot be finger-spelt).
		var sWrkWord = util_string_getAlphaNumeric(asb_fs_oViewer.getWord(), true, false);
		var sFeedback = "";
		
		// 3b) Determine whether the answer was correct, and construct a 
		//     feedback message.
		if (sWrkWord.toUpperCase() == sWrkResponse.toUpperCase()) {
			sFeedback += "<p class='asbCFrameLeftPromptHeading'>Correct</p>";
		} else {
			sFeedback += "<p class='asbCFrameLeftPromptHeading'>Whoops</p>";
			sFeedback += "<p class='asbCFrameLeftPromptText'>You typed <span class='asbObjFSPracticeResponse'>" + sWrkResponseRaw + "</span></p>";
		}
		sFeedback += "<p class='asbCFrameLeftPromptText'>The word spelt above was <span class='asbObjFSPracticeResponse'>" + asb_fs_oViewer.getWord() + "</span></p>";
			
	// STEP 4: Display feedback to the user
		// 4a) Insert feedback message
		if ( browserKit.getElementById("asbFSPracticeResultFeedback") ) {
			browserKit.lastReturnedObject.innerHTML = sFeedback;
		}

		// 4b) Hide the input DIV, and show the "result" DIV
		if ( browserKit.getElementById("asbFSPracticeInput") ) {
			browserKit.lastReturnedObject.style.display = "none";
		}
		if ( browserKit.getElementById("asbFSPracticeResult") ) {
			browserKit.lastReturnedObject.style.display = "";
		}

	// RETURN a result
	return false;	// Prevent the calling form from performing a Submit
}


function asb_fs_setPageModeViaUI(eState) {
	if (asb_fs_pageMode == c_asb_fs_pageMode_initializing) {
		// Cannot chrange the pageMode via the UI while the page is 
		// initialising.
		alert("Please wait until the page has finished loading and all images have been pre-cached");
	} else {
		asb_fs_setPageMode(eState);
	}
}


function asb_fs_handleAlphabetLoad() {
	window.status = "asb_fs_handleAlphabetLoad: All Images have been loaded";
	
	// Default to "view" mode.
	asb_fs_setPageMode(c_asb_fs_pageMode_view);
}

function asb_fs_handleAlphabetImageLoad(nLoaded, nTotal) {
	var sHTML = "";
	sHTML += "<p>Please wait while the fingerspelling images are pre-cached for faster playback.</p>";
	sHTML += "<p>(loaded " + nLoaded + " of " + nTotal + " images)</p>";

	if ( browserKit.getElementById("asbFSInitializationMessage") ) {
		browserKit.lastReturnedObject.innerHTML = sHTML;
	}
}


function asb_fs_replayWord() {
	asb_fs_oViewer.showWord();
}


function asb_fs_setWordSpeed(oLink, nRate) {
	window.status = "spelling speed set to: " + nRate;
	asb_fs_oViewer.setLetterRate(nRate);
	
	if (asb_fs_currentSpeedLink) {
		asb_fs_currentSpeedLink.className = "asbObjFSPreviewSpeedOptionNRM";
		asb_fs_currentSpeedLink = null;
	}
	
	if (oLink) {
		asb_fs_currentSpeedLink = oLink;
		oLink.className = "asbObjFSPreviewSpeedOptionSEL";
	}
}


function asb_fs_handleSpellStart() {
}

function asb_fs_handleSpellFinish() {
	asb_fs_nPlayCount++;

	if (asb_fs_pageMode == c_asb_fs_pageMode_practice) {
		// OPTION 1: Page is in "practice" mode. If the 'response' input field 
		//           is disabled, it can now be enabled.
			// 1a) Determine whether the practice "input" form is currently visible
			if ( browserKit.getElementById("asbFSPracticeInput") ) {
				var bTmpFormVisible = (browserKit.lastReturnedObject.style.display != "none");
			}
		
			// 1b) Initialise the input field
			if (browserKit.getElementById("txtASBFSPracticeWord")) {
				var oTmp = browserKit.lastReturnedObject;

				if (asb_fs_nPlayCount == 1) {oTmp.value = "";}	// Clear the "please wait" message if this is the first time the current practice word has been played
				oTmp.disabled = false;
				if (bTmpFormVisible) {oTmp.focus();}
			}
	}
}


function asb_fs_preloadTabs(sPath) {
	var aTmp;
	var nIdx;
	aTmp = new Array();

	// Build an array of image pairs, one for each tab in the collection.
	for (nIdx = c_asb_fs_pageModeUIMin; nIdx <= c_asb_fs_pageModeUIMax; nIdx++) {
		aTmp[nIdx] = new Array();
		asb_fs_preloadTabState(aTmp[nIdx], sPath, nIdx, "");
		asb_fs_preloadTabState(aTmp[nIdx], sPath, nIdx, "_select");
	}
	
	return aTmp;
}

function asb_fs_preloadTabState(aCol, sPath, sObjName, sObjState) {
	aCol[sObjState] = new Image(10,10);
	aCol[sObjState].src = sPath + "fstab_0" + sObjName + sObjState + ".gif";
}