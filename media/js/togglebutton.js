// ==={ CLASS DEFINITIONS }=====================================================

/* -----------------------------------------------------------------------------
 * CLASS .......... UTIL_UI_TB_ToggleGroup
 * DESCRIPTION .... This 'class' provides a grouping control for sets of 
 *                  "ToggleButtons". Buttons grouped under a ToggleGroup work 
 *                  in a "mutually" exclusive manner (i.e. only one button 
 *                  will ever be "selected" at one time)
 * -------------------------------------------------------------------------- */
function UTIL_UI_TB_ToggleGroup(sImagePath) {

	// - { METHODS } - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	this.addButton = function(sKey, sImageID, sAnchorID, sBaseImageName, sStateList, sTag) {
		var nTmp, sTmp;
		var oTmpImage, oTmpAnchor;

		// STEP 1: Get references to the specified DOM objects
			if (sImageID) {
				oTmpImage = browserKit.getElementById(sImageID);
			}

			if (sAnchorID) {
				oTmpAnchor = browserKit.getElementById(sAnchorID);
			}
		
		// STEP 2: Initialise a new button object
			var oButton = this.buttons[sKey] = new UTIL_UI_TB_Button(sKey, this, oTmpImage, oTmpAnchor);
			oButton.tag = sTag;
		
		// STEP 3: Preload images for specified button states based on the 
		//         image-naming convention for this ToggleGroup
			if (sBaseImageName) {
				oButton.imagesBaseName = sBaseImageName;
				
				if (sStateList) {
					// Preload the specified list of button states
					var aStates = sStateList.split(",");
					
					for (nTmp = 0; nTmp < aStates.length; nTmp++) {
						oButton.addState(aStates[nTmp]);
					}
				}
			}
		
		// RETURN a reference to the new object
		return oButton;
	}
	
	this.setSelectedButton = function(sKey) {
		if (sKey) {
			var oCurrent = this.buttons[sKey]
		} else {
			return false;
		}
		
		if (this._selectedButton != oCurrent) {
			// Deselect "current" button
			if (this._selectedButton) {
				this._selectedButton.setState(this.stateNormal);
			}
			
			// Establish new "current" button
			oCurrent.setState(this.stateSelected);
			this._selectedButton = oCurrent;
			
			// Call specified "event handler"
			if (this.onChange) {
				eval("window." + this.onChange + "();");
			}
		}
	}
	
	this.getSelectedButton = function() {
		return this._selectedButton;
	}
	
	// - { INITIALISATION  PROCEDURE } - - - - - - - - - - - - - - - - - - - - -
	
	// PRIVATE Properties (should not be modified by outside code)
	this._selectedButton = null;

	// Public Properties
	this.buttons = new Array();
	this.onChange = "";

	// Set up base "states". other states may be specified by the page code, 
	// and buttons put into these 'custom' states. Inbuilt behaviours will 
	// set buttons into the following states however.
		this.stateSelected = "select";
		this.stateNormal = "";
		this.stateDisabled = "dis";
		this.stateHover = "ovr";

	// Set up image naming conventions
		// Suffixes appended to base image name for different button states
		this.imageSuffix = new Array();
		this.imageSuffix[this.stateNormal] = "";
		this.imageSuffix[this.stateSelected] = "_select";
		this.imageSuffix[this.stateHover] = "_OVR";
		this.imageSuffix[this.stateDisabled] = "_DIS";
	
		// Image Type
		this.imageExtension = "gif";

		// Images Path
		this.imagePath = sImagePath;
}


/* -----------------------------------------------------------------------------
 * CLASS .......... UTIL_UI_TB_Button
 * DESCRIPTION .... This 'class' controls a single "ToggleButton"
 * -------------------------------------------------------------------------- */
function UTIL_UI_TB_Button(sKey, oParent, oImage, oAnchor) {

	// - { METHODS } - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	this.addState = function(sState, sImagePath) {
		var sTmpImagePath = "";
		var sTmp;

		// STEP 1: Determine the path to the image for the specified state
		if (sImagePath) {
			// OPTION 1a: Use the fully specified image path
			sTmpImagePath = sImagePath;

		} else if (this.imagesBaseName) {
			// OPTION 1b: Create a path based on image naming rules
			sTmp = this.parent.imageSuffix[sState];
			if (!sTmp) {sTmp = "";}
			sTmpImagePath = this.parent.imagePath + this.imagesBaseName + sTmp + "." + this.parent.imageExtension;

		}
		
		// STEP 2: Preload Image
		this.images[sState] = new Image(10,10);
		this.images[sState].src = sTmpImagePath;
	}
	
	this.setState = function(sState) {
		if (this.domImage) { if (this.domImage.src) {
				if (this.images[sState]) {
					this.domImage.src = this.images[sState].src;
				}
		}	}
	}
	
	this.handleClick = function() {
		if (this.parent) {
			this.parent.setSelectedButton(this.key);
		}
	}
	
	// - { INITIALISATION  PROCEDURE } - - - - - - - - - - - - - - - - - - - - -
	this.key = sKey;
	this.tag = "";
	
	this.images = new Array();
	this.imagesBaseName = "";
	
	this.domImage = oImage;
	this.domAnchor = oAnchor;
	this.parent = oParent;
	
	if (this.domAnchor) {
		this.domAnchor.uiLinkedToggleButton = this;
		this.domAnchor.onclick = function() {
			if (this.uiLinkedToggleButton) {
				this.uiLinkedToggleButton.handleClick();
			}
			return false;
		}
	}
}



// ==={ SUPPORT FUNCTIONS }=====================================================
function util_ui_tb_button_handleButtonClick() {
	var oButton = this.uiLinkedToggleButton;
	
	if (oButton) {
		oButton.handleClick();
	}
	
	return false;
}