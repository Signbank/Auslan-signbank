// ==={ CLASS DEFINITIONS }=====================================================

/* -----------------------------------------------------------------------------
 * CLASS ......... UTIL_ObjectRegistry
 * DESCRIPTION ... Provides a mechanism for tracking instances of classes and 
 *                 for class methods to invoke themselves using javascript 
 *                 built-in functions such as setTimeout().
 *
 *                 Within the class constructor, include the following line of 
 *                 code: 
 *                 this._instance = util_ObjectRegistry.addObject(<classname>, this);
 *
 *                 For class code to call a method via setTimeout, use the 
 *                 following:
 *                 setTimeout("util_ObjectRegistry.callObjectMethod('<classname>'," + this._instance + ",'<methodname>','<arguments as a comma separated string>')", <timeout>);
 * -------------------------------------------------------------------------- */
	function UTIL_ObjectRegistry() {
		this.objects = new Array();
	
		this.addObject = function(sClass, oObject) {
			var sTmpClass = new String(sClass);
	
			if (this.objects[sTmpClass] == null) {this.objects[sTmpClass] = new Array();}
	
			var nInstance = this.objects[sTmpClass].length;
			this.objects[sTmpClass][nInstance] = oObject;
	
			return nInstance;
		}
		
		this.callObjectMethod = function(sClass, nInstance, sMethod, sArgs) {
			var sTmpClass = new String(sClass);
			var sTmpArgs = "";
			var oWrk = this.objects[sTmpClass][nInstance];
			if (sArgs != null) {sTmpArgs = new String(sArgs);}
	
			eval("oWrk." + sMethod + "(" + sTmpArgs + ")");
		}
	}



// ==={ INTIALISATION CODE: EXECUTED ON INCLUDE }===============================

var util_ObjectRegistry = new UTIL_ObjectRegistry();