/* Image Preloading and Rollovers */

function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_findObj(n, d) { //v4.0
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && document.getElementById) x=document.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

/* Popup Windows */
function MM_openBrWindow(theURL,winName,features) { //v2.0
  window.open(theURL,winName,features);
}

function asb_openWindow(sName, sURL) {
	if (!window.asb_windows) { window.asb_windows = new Array(); }
	window.asb_windows[sName] = util_window_open(window.asb_windows[sName], sURL, sName, "toolbar=0,location=1,directories=0,status=1,menubar=1,scrollbars=1,resizable=1,width=630,height=600");
	
	return window.asb_windows[sName];
}


function util_flash_replay(sFlashObjectID, sFlashEmbeddedID, sContainerID) {
	// STEP 1: Try for Internet Explorer on Windows (using <object> tag)
		if ( (browserKit.os.family == "win-32") && (browserKit.browser.type == "ie") ) {
			if ( util_flash_replayIeWin(sFlashObjectID) ) {
				return true;
			}
		}
	
	// STEP 2: Try using LiveConnect with Netscape style plugin in <embed> tag
		if (browserKit.getElementById(sFlashEmbeddedID)) {
			if (browserKit.browser.type == "netscape") {
				if (browserKit.lastReturnedObject.Play) {
					browserKit.lastReturnedObject.StopPlay();
					browserKit.lastReturnedObject.Rewind();
					browserKit.lastReturnedObject.Play();
					return true;
				}
			}
		}
	
	// STEP 3: Flash plugin is either not ActiveX, or is not running in a 
	//         browser that supports LiveConnect API for Netscape style 
	//         plugins. Replay by re-rendering container
		if ( browserKit.getElementById(sContainerID) ) {
			var sTmp = new String(browserKit.lastReturnedObject.innerHTML);
			browserKit.lastReturnedObject.innerHTML = sTmp;
			return true;
		}
	
	return false;
}

function util_flash_replayIeWin(sFlashObjectID) {
	if ( browserKit.getElementById(sFlashObjectID) ) {
		try {
			browserKit.lastReturnedObject.StopPlay();
			browserKit.lastReturnedObject.Rewind();
			browserKit.lastReturnedObject.Play();
			return true;
		}
		catch (e) {
			// Do Nothing
		} 
	}
	return false;
}

function util_debug_dumpProperties(obj) {
	var sOutput = "";
	for (prop in obj) {	
		sOutput = prop + ": [" + obj[prop] + "]\n";
	}
	return sOutput;
}


function util_window_open(oWindowRef, sURL, sWindowName, sFeatures) {
	var bOpened = false;

	// STEP 1: Open window at correct URL
		// OPTION 1a: Update window location if it is already open
		if (oWindowRef) { if (!oWindowRef.closed) {
			oWindowRef.location = sURL;
			bOpened = true;
		} }

		// OPTION 1b: Open window
		if (!bOpened) {
			oWindowRef = window.open(sURL, sWindowName, sFeatures);
		}

	// STEP 2: Set Focus
		if (oWindowRef.focus) {oWindowRef.focus();}

	return oWindowRef;
}





// Eliminates all non-alphanumeric characters from a source string. 
// NOTE! This prodedure will only work for strings containing Latin unicode 
//       characters.
function util_string_getAlphaNumeric(sInput, bIncludeLetters, bIncludeNumbers, sExtraCharsAllowed) {
	var sWrk = "";
	var nWrkChar, nIdx, nIdx2;
	var sWrkExtraChars;

	// STEP 1: Validate Input
		sWrkInput = new String(sInput);
		
		if (sExtraCharsAllowed) {
			sWrkExtraChars = new String(sExtraCharsAllowed);
		}
	
	// STEP 2: Iterate over the source string, including only characters that 
	//         we have been allowed to include.
		for (nIdx = 0; nIdx < sWrkInput.length; nIdx++) {
			nWrkChar = sWrkInput.charCodeAt(nIdx);
			
			if ( (nWrkChar >= 65 && nWrkChar <= 90) || (nWrkChar >= 97 && nWrkChar <= 122) ) {
				// Character is a lower-case or upper-case letter
				if (bIncludeLetters) {sWrk += String.fromCharCode(nWrkChar);}
	
			} else if (nWrkChar >= 48 && nWrkChar <= 57) {
				// Character is a digit (0-9)
				if (bIncludeNumbers) {sWrk += String.fromCharCode(nWrkChar);}
	
			} else {
				// Character is unknown - we should test it against our list of 
				// special characters allowed (if supplied).
				if (sWrkExtraChars) {
					nIdx2 = 0;
					while (nIdx2 < sWrkExtraChars.length) {
						if (sWrkExtraChars.charCodeAt(nIdx2) == nWrkChar) {
							sWrk += String.fromCharCode(nWrkChar);
							break;
						}
						nIdx2++
					}
				}
			}
		}
	
	// RETURN a result (as a primitive string type)
	return sWrk.toString();
}