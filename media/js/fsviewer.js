// ==={ CLASS DEFINITIONS }=====================================================

/* -----------------------------------------------------------------------------
 * CLASS: ASB_FSViewer
 * -------------------------------------------------------------------------- */

function ASB_FSViewer(oViewerImg, oFSAlphabet) {
	this.image = oViewerImg;		// Hold a reference to the document Image object that will be used to display images
	this.alphabet = oFSAlphabet;	// Current Finger-Spelling Alphabet
	this.transitionDelay = 325;
	this.transitionImageSrc = "";
	
	this.onSpellStart = "";
	this.onSpellFinish = "";

	this._delayLtr = 0;				// Delay between letters
	this._delayCurrentFrame = 0;
	this._currentWord = "";
	this._currentCharIdx = 0;
	this._currentFrame = 0;
	this._instance = util_ObjectRegistry.addObject("ASB_FSViewer", this);
	this._currentAnimationID = 0;	// Used to determine which scheduled calls to showNextFrame() should be acted on
	
	this.setLetterRate = function(nLettersPerSecond) {
		this._delayLtr = Math.round(1000 / nLettersPerSecond);
	}

	
	this.getWord = function() {
		return this._currentWord;
	}

	
	this.setWord = function(sWord) {
		if (sWord == null) {return false;}
		if (sWord.length == 0) {return false;}

		this._currentWord = sWord.toUpperCase();
		return true;
	}

	
	this.showWord = function () {
		// STEP 1: Call specified onSpellStart "event handler" if appropriate
		if (this.onSpellStart.length) {eval(this.onSpellStart + "();");}
		
		// STEP 2: Initialise object state
			this._currentCharIdx = -1;

			// Increment the AnimationID. This property ensures that if 
			// ShowNextFrame() is called by a timeout that was set by the last 
			// animation (because the user has interrupted that animation to 
			// start a new one) then the call will be ignored.
			this._currentAnimationID = (this._currentAnimationID < 1000000) ? this._currentAnimationID + 1 : 1;

		// STEP 3: Begin the animation
		this.showNextLetter();
	}
	

	this.spellWord = function(sWord) {
		if (this.setWord(sWord)) {
			this.showWord();
		}
	}
	
	
	/* Method: showNextLetter()
	   Advances the current animation to the next letter in the word being 
	   spelt */
	this.showNextLetter = function() {
		// Move to the next position in the word being spelt
		this._currentCharIdx++;

		if (this._currentCharIdx < this._currentWord.length) {
			// Get a reference to the current letter object from the 'alphabet' 
			// collection.
			var oLetter = this.getCurrentLetterObj();
			if (oLetter == null) {this.showNextLetter(); return 0;}	// Skip the letter if it is not in the alphabet

			// Determine what the frame delay should be for the current letter 
			// animation (i.e. standard letter duration (divided by) number of 
			// frames of animation defined for the current letter
			this._delayCurrentFrame = ( (this._delayLtr - this.transitionDelay) / oLetter.length );

			// Initialise frame counter
			this._currentFrame = -1;

			if (this._currentCharIdx) {
				// Show a transition frame before displaying the first frame of 
				// the current letter animation
				this.showTransitionFrame();
			} else {
				// Do not show a transition frame before the first letter
				this.showNextFrame(this._currentAnimationID);
			}

		} else {
			// The word has finished displaying
			if (this.onSpellFinish.length) {
				eval(this.onSpellFinish + "();");
			}

		}
	}
	
	
	/* Method: showNextFrame()
	   Advances to the next frame in the current letter animation and displays 
	   it. If there are no more frames defined for the current letter, then the 
	   animation is advanced to the next letter in the word being spelt) */
	this.showNextFrame = function(nAnimationID) {
		// Abort if the specified animation is no longer current (i.e. a new 
		// animation has been started since the call to this method was 
		// "scheduled").
		//alert(nAnimationID + "," + this._currentAnimationID);
		if (nAnimationID != this._currentAnimationID) {return 0;}

		this._currentFrame++;
		var oLetter = this.getCurrentLetterObj();
		
		if (oLetter) {
			if (this._currentFrame < oLetter.length) {
				this.image.src = oLetter[this._currentFrame].src;
				setTimeout("util_ObjectRegistry.callObjectMethod('ASB_FSViewer'," + this._instance + ",'showNextFrame','" + this._currentAnimationID + "');", this._delayCurrentFrame);
			} else {
				// no more frames to display for current letter. Move to the next 
				// letter
				this.showNextLetter();
			}
		}
	}


	/* Method: showTransitionFrame()
	   Displays a transition frame and schedules a call to showNextFrame in 
	   order to display the current letter's animation */
	this.showTransitionFrame = function() {
		this.image.src = this.transitionImageSrc;
		setTimeout("util_ObjectRegistry.callObjectMethod('ASB_FSViewer'," + this._instance + ",'showNextFrame','" + this._currentAnimationID + "');", this.transitionDelay);
	}
	

	/* Method: getCurrentLetterObj()
	   Returns letter object (from the linked FSAlphabet) that corresponds to 
	   the letter (form the current "word") that is being shown. */
	this.getCurrentLetterObj = function() {
		var sLetter = this._currentWord.charAt(this._currentCharIdx);
		return this.alphabet.letters[sLetter];
	}
	
	// Initialisation Procedure ................................................
	this.setLetterRate(1);	// Set default speed to one letter per second
}



/* -----------------------------------------------------------------------------
 * CLASS: ASB_FSAlphabet
 * -------------------------------------------------------------------------- */

function ASB_FSAlphabet(nId, nImageCountTotal, sImagesPath, sOnLoad, sOnImageLoad) {
	this.id = nId;
	this.letters = new Array();
	this.imageCount = 0;
	this.imageCountTotal = nImageCountTotal; 
	this.imagesLoaded = false;
	this.imagesPath = sImagesPath;
	this.onImageLoad = "";
	this.onLoad = "";

	if (sOnLoad != null) {this.onLoad = new String(sOnLoad);}
	if (sOnImageLoad != null) {this.onImageLoad = new String(sOnImageLoad);}

	/* Method: handleImageLoaded() ... Event handler for images that are 
	                                   preloaded using the addLetter() method. 
									   */
	this.handleImageLoaded = function() {
		this.imageCount++;
		
		// Call the specified event handler for image loading progress
		if (this.onImageLoad.length) {
			eval(this.onImageLoad + "(" + this.imageCount + "," + this.imageCountTotal + ");");
		}
		
		// Determine whether loading has completed
		if (this.imageCount >= nImageCountTotal) {
			this.imagesLoaded = true;

			// Invoke the specified callback function ('event handler') if one 
			// was supplied in the constructor.
			if (this.onLoad.length) {
				eval(this.onLoad + "();");
			}
		}
	}
	

	/* Method: loadImages() ... Loads specified images and 'links' them to a 
	                            letter of the alphabet */
	this.addLetter = function(sLetter, sImageNames) {
		var aImages = sImageNames.split(',');
		var sTmpLetter = sLetter.toUpperCase();
		
		if (aImages.length > 0) {
			// Add a letter to the alphabet
			this.letters[sTmpLetter] = new Array();

			// Add Images to the "letter" definition
			for (var nIdx = 0; nIdx < aImages.length; nIdx++) {
				if (browserKit.browser.family == "applewebkit") {
					// HACK: Safari / AppleWebKit based browsers don't properly 
					//       set the event target (for the onLoad) event when 
					//       the image firing the event is not part of the 
					//       document.
					//       Therefore, instead of referencing the new image 
					//       only in an array, we will write an IMG tag to the 
					//       document and get a reference to that image object.
					sID = "asb_fs_imgLetter_" + this.id + "_" + sLetter + "_" + nIdx;
					document.writeln("<img src=\"" + this.imagesPath + aImages[nIdx] + "\" width=\"1\" height=\"1\" id=\"" + sID +"\" style=\"visibility:hidden\">");
					objWrk = document.getElementById(sID);
				} else {
					objWrk = new Image(10,10);
				}

				objWrk.asb_fsAlphabet = this;	// Add a reference to the alphabet that is "loading" the image to the image's properties.
				objWrk.onload = asb_fs_handleFSAImagePreload;
				objWrk.src = this.imagesPath + aImages[nIdx];
			
				this.letters[sTmpLetter][nIdx] = objWrk;
			}
		}  
	}
}



// ==={ SUPPORT FUNCTIONS }=====================================================
function asb_fs_handleFSAImagePreload(e) {
	var obj = this.asb_fsAlphabet;
	if (obj) {
		obj.handleImageLoaded();
	} else {
		obj = e.target;
		if (obj) {obj.handleImageLoaded();}
	}
}
