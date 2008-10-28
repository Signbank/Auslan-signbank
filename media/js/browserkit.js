function BrowserKit() {
	// Public Properties
	// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	this.browser = brs_detectBrowser();
	this.os = brs_detectPlatform();
	
	// These members are used for methods that return TRUE on success / FALSE 
	// on failure, but must also return other information.
	this.lastReturnedObject = null;		// Object reference returned by last 
										// function (for functions whose purpose 
										// is to return an object reference 
										// given some information).

	this.lastError = 0;			// Numeric error code returned by last function.
								// Meaning depends on function that was called.


	// Public Methods
	// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	this.getElementById = function (id, layerName) {
		// Initialise Variables
		var bSupported = false;
		var oResult;
		this.lastReturnedObject = null;
		this.lastError = 0;
		
		// STEP 1: Attempt to get a reference to the specified element using 
		//         whatever method the browser supports.
			if (document.all) {
				bSupported = true;
				oResult = document.all[id];
			}
			else if (document.getElementById) {
				bSupported = true;
				oResult = document.getElementById(id);
			}
			else if (document.layers) {
				// Insert code here to use the layerName attribute to locate the 
				// specified element on the layer.
			}
		
		// STEP 2: Update the lastReturnedObject property
			if (oResult) {this.lastReturnedObject = oResult;}
		
		// STEP 3: If the previous step failed, report the reason for failure 
		//         by using the .lastError property.
			if (this.lastReturnedObject == null) {
				if (bSupported) {
					// ERROR: Element not Found
					this.lastError = 2;
				} else {
					// ERROR: Operation not supported by Browser
					this.lastError = 1;
				}
			}

		// RETURN a reference to the specified DOM object
		return (this.lastReturnedObject);
	}
	
	this.debug_dumpInfo = function() {
		var sMsg = "Browser Info:\n";
		sMsg += this.debug_dumpObject(this.browser);
		
		sMsg += "\nPlatform Info:\n";
		sMsg += this.debug_dumpObject(this.os);
		
		return sMsg;
	}
	
	this.debug_dumpObject = function(obj, nNestLevel)  {
		if (nNestLevel == null) {nNestLevel = 0;}
		var sReturn = "";
		
		for (prop in obj) {
			for (i = 1; i <= nNestLevel; i++) {sReturn += "...";}
			sReturn += (prop + ": ");
			
			if (typeof obj[prop] == "object") {
				sReturn += "\n";
				sReturn += this.debug_dumpObject(obj[prop], nNestLevel + 1);
			} else {
				sReturn += (obj[prop] + "\n");
			}
		}
		
		return sReturn;
	}
}



function brs_detectBrowser() {
	var ua = navigator.userAgent.toLowerCase(); 
	var browser = new Object();
	
	// browser engine name
	var isGecko       = (ua.indexOf('gecko') != -1 && ua.indexOf('safari') == -1);
	var isAppleWebKit = (ua.indexOf('applewebkit') != -1);
	
	// browser name
	var isKonqueror   = (ua.indexOf('konqueror') != -1); 
	var isSafari      = (ua.indexOf('safari') != - 1);
	var isOmniweb     = (ua.indexOf('omniweb') != - 1);
	var isOpera       = (ua.indexOf('opera') != -1); 
	var isIcab        = (ua.indexOf('icab') != -1); 
	var isAol         = (ua.indexOf('aol') != -1); 
	var isIE          = (ua.indexOf('msie') != -1 && !isOpera && (ua.indexOf('webtv') == -1) ); 
	var isMozilla     = (isGecko && ua.indexOf('gecko/') + 14 == ua.length); 
	var isFirebird    = (ua.indexOf('firebird/') != -1);
	var isNS          = ( (isGecko) ? (ua.indexOf('netscape') != -1) : ( (ua.indexOf('mozilla') != -1) && !isOpera && !isSafari && (ua.indexOf('spoofer') == -1) && (ua.indexOf('compatible') == -1) && (ua.indexOf('webtv') == -1) && (ua.indexOf('hotjava') == -1) ) );
	
	// Correct version number
		var versionMinor = parseFloat(navigator.appVersion);
		browser.version = new Object();

		if (isGecko && !isMozilla) {
			browser.version.minor = parseFloat( ua.substring( ua.indexOf('/', ua.indexOf('gecko/') + 6) + 1 ) );
			browser.type = "mozilla";
		}
		else if (isMozilla) {
			browser.versionMinor = parseFloat( ua.substring( ua.indexOf('rv:') + 3 ) );
			browser.type = "mozilla";
		}
		else if (isIE) {
			browser.type = "ie";
			if (versionMinor >= 4) {
				browser.version.minor = parseFloat( ua.substring( ua.indexOf('msie ') + 5 ) );
			}
		}
		else if (isKonqueror) {
			browser.type = "konqueror";
			browser.version.minor = parseFloat( ua.substring( ua.indexOf('konqueror/') + 10 ) );
		}
		else if (isSafari) {
			browser.type = "safari";
			browser.version.minor = parseFloat( ua.substring( ua.lastIndexOf('safari/') + 7 ) );
		}
		else if (isOmniweb) {
			browser.type = "omniweb";
			browser.version.minor = parseFloat( ua.substring( ua.lastIndexOf('omniweb/') + 8 ) );
		}
		else if (isOpera) {
			browser.type = "opera";
			browser.version.minor = parseFloat( ua.substring( ua.indexOf('opera') + 6 ) );
		}
		else if (isIcab) {
			browser.type = "icab";
			browser.version.minor = parseFloat( ua.substring( ua.indexOf('icab') + 5 ) );
		}
		else {
			browser.type = "unknown";
			browser.version.minor = versionMinor; 
		}
		
		browser.version.major = parseInt(browser.version.minor); 
	
	// Rendering Engine Versions
		browser.version.gecko = ( (isGecko) ? ua.substring( (ua.lastIndexOf('gecko/') + 6), (ua.lastIndexOf('gecko/') + 14) ) : -1 );
		browser.version.mozillaEquiv = ( (isGecko) ? parseFloat( ua.substring( ua.indexOf('rv:') + 3 ) ) : -1 );
		browser.version.appleWebKit = ( (isAppleWebKit) ? parseFloat( ua.substring( ua.indexOf('applewebkit/') + 12) ) : -1 );
	
	// Browser Rendering Engines
		if (isGecko) {
			// Browser is some variation of the Mozilla gecko engine
			browser.family = "gecko";
		}
		else if (isAppleWebKit) {
			browser.family = "applewebkit";
		}
		else if (isKonqueror || isSafari) {
			// Safari is based on konquereo, so all safari/konqueror browser will 
			// return "konqueror" here.
			browser.family = "konqueror";
		}
		else {
			browser.family = "";
		}
	
	// Browser Compatibility
		browser.compatible = new Object();
		browser.compatible.mozilla = ( (ua.indexOf('mozilla') != -1) && !isNS && !isMozilla);
		browser.compatible.ie = ( (ua.indexOf('msie') != -1) && !isIE);
	
	// Browser Capabilities
		browser.supports = new Object();
		browser.supports.dom1 = (document.getElementById != null);
		browser.supports.dom2Event = ((document.addEventListener != null) && (document.removeEventListener != null));
	
	// CSS Compatibility Mode
		// Will return BackCompat for browsers that don't support WC3 
		// standards, or standards-compliant browsers that are rendering in 
		// backwards-compatibility mode because of a DOCTYPE directive in the 
		// page.
		browser.renderingMode = document.compatMode ? document.compatMode : 'BackCompat';

	// RETURN a result
	return browser;
}


function brs_detectPlatform() {
	var ua = navigator.userAgent.toLowerCase(); 
	var os = new Object();

	// Tests on UserAgent string for clues to operating system
	var isWin    = (ua.indexOf('win') != -1);
	var isWin32  = (isWin && ( ua.indexOf('95') != -1 || ua.indexOf('98') != -1 || ua.indexOf('me') != -1 || ua.indexOf('nt') != -1 || ua.indexOf('win32') != -1 || ua.indexOf('32bit') != -1 || ua.indexOf('xp') != -1) );
	var isWinNT  = (isWin && ( ua.indexOf('nt') != -1 || ua.indexOf('win32') != -1 || ua.indexOf('xp') != -1)) // Might be a problem in looking for "nt" with "win" somewhere in the string. Is this reliable???
	var isMac    = (ua.indexOf('mac') != -1);
	var isUnix   = (ua.indexOf('unix') != -1 || ua.indexOf('sunos') != -1 || ua.indexOf('bsd') != -1 || ua.indexOf('x11') != -1)
	var isLinux  = (ua.indexOf('linux') != -1);
	
	// Operating System Family and Specific Type
	if (isWin) {
		if (isWinNT) {
			os.family = "win-32";
			os.type = "win-nt";
		}
		else if (isWin32) {
			os.family = "win-32";
			os.type = "win-9x";
		}
		else {
			os.family = "win-32";
			os.type = "win-3x";
		}
	}
	else if (isMac) {
		// To-Do: Would be nice to be able to differentiate between classic 
		// MacOS and MacOS X families.
		os.family = "mac-os";
		os.type = "mac-os";
	}
	else if (isUnix || isLinux) {
		os.family = "posix";
		if (isLinux) {
			os.type = "linux";
		} else {
			os.type = "unix";
		}
	}
	
	return os;
}