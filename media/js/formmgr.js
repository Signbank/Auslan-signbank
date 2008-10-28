var TYPEID_SELECTBOX = 0;
var TYPEID_TEXTBOX = 1;
var TYPEID_CHECKBOX = 2;
var TYPEID_BUTTON = 3;
var TYPEID_TEXTAREA = 4;
var TYPEID_NONE = 5;
var TYPEID_FILEBOX = 6;
var TYPEID_IMAGEBUTTON = 7;

var TYPE_NAMES = new Array("selectbox","textbox","checkbox","button","textarea","none","filebox", "imagebutton");

function typeID(type)
{
    var id = -1;
    var n;

    for(n=0;n<TYPE_NAMES.length;n++)
    {
      if(TYPE_NAMES[n] == type)
      {
        id = n;
        break;
      }
    }
     
    if(id == -1)
    {
      alert("Type '" + type + "' is not supported!");
    }

    return id;
}

function getList(stringList)
{
    var list = new Array();
    var n = 0;
    var start = 0;
    var stop;

    stop = stringList.indexOf(",");
    while(stop != -1)
    {
      list[n++] = stringList.substring(start,stop);
      start = stop+1;
      stop = stringList.indexOf(",", start);
    }        
    list[n++] = stringList.substring(start,stringList.length);

    return list;
}

// Component Class
//================================================================
// Contains information about a form component (usually a control
// of some description).
//================================================================
// member - typeID (int)
//          Type of the component.
//        - controlName (string)
//          Name of component (or in the case of a non-control, 
//          the ID value).
//        - parentName (string)
//          Name of the parent component.
//        - parentID (int)
//          Index of the parent component, -1 if this is the root
//          component.
//        - parentValues (string[])
//          List of parent values which this component is 
//          displayed for.
//        - divName (string)
//          Name of the div which contains the component.
//        - visible (boolean)
//          Is this component currently visible.
//        - defaultValue (string)
//          Default value after being reset.
//
//        - nImage (string)
//          URL of normal button image.
//        - aImage (string)
//          URL of active button image.
// method - void dump() (void)
//          Dumps the contents of this component class to an alert
//          box.
//        - bool isMatch() (string)
//          Returns true if the passed string is one of the items
//          in the parentValues list.
//================================================================
function Component(controlName, type, parentName, parentValues, divName, defaultValue, nImage, aImage)
{
    this.typeID = typeID(type);
    this.controlName = controlName;
    this.parentName = parentName;
    this.parentID = -1;
    this.parentValues = getList(parentValues);
    this.divName = divName;

    this.visible = true;

    this.defaultValue = defaultValue;

    this.dump = componentDump;
    this.isMatch = componentIsMatch;

    this.nImage = nImage;
    this.aImage = aImage;

    this.state = false;
}

/*
function Component(controlName, type, parentName, parentValues, divName, defaultValue)
{
    this.typeID = typeID(type);
    this.controlName = controlName;
    this.parentName = parentName;
    this.parentID = -1;
    this.parentValues = getList(parentValues);
    this.divName = divName;
    this.visible = true;
    this.defaultValue = defaultValue;

    this.dump = componentDump;
    this.isMatch = componentIsMatch;
}
*/

function componentDump()
{
    var s = "";
    var n;

    s = "Component: " + this.controlName + " (type=" + this.typeID + " (" + TYPE_NAMES[this.typeID] + "))\n\n";
    s = s + "Parent: " + this.parentName + " (ID=" + this.parentID + ", Values=";
    s = s + "'" + this.parentValues[0] + "'";
    for(n=1;n<this.parentValues.length;n++)
    {
      s = s + ",'" + this.parentValues[n] + "'";
    }
    s = s + ")\n";
    s = s + "Div Block: " + this.divName + "\n";
    s = s + "Default Value: " + this.defaultValue + "\n";
    s = s + "Visible=" + this.visible + "\n";

    alert(s); 
}

function componentIsMatch(value)
{
    var n;
    var match = false;

    for(n=0;n<this.parentValues.length;n++)
    {
      if(this.parentValues[n] == value)
      {
        match = true;      
        break;
      }
    }

    return match;
}

// Form Manager Class
//================================================================
// Contains definitions of a form, and methods for controlling the
// visibility of components.
//================================================================
// member - name (string)
//          The name of the form.
//        - components (component[])
//          Array of components which are in the form.
// method - void dump() (void)
//          Dumps the contents of this component class to an alert
//          box.
//        - bool isMatch() (string)
//          Returns true if the passed string is one of the items
//          in the parentValues list.
//================================================================
function FormManager(name)
{
    this.components = new Array();
    this.name = name;

    this.register = formManagerRegister;
    this.clearAll = formManagerClearAll;
    this.clearID = formManagerClearID;
    this.change = formManagerChange;
    this.changeID = formManagerChangeID;
    this.hideID = formManagerHideID;
    this.showID = formManagerShowID;
    this.findComponent = formManagerFindComponent;
    this.getValue = formManagerGetValue;
    this.setValue = formManagerSetValue;
    this.toggle = formManagerToggle;
}

// Gets the id of the supplied component name
function formManagerFindComponent(componentName)
{
    var id = -1;
    var n;

    if(componentName.length != 0)
    {
      for(n=0;n<this.components.length;n++)                     
      {
        if(this.components[n].controlName == componentName)
        {          
          id = n;
          break;
        }
      }

      if(id == -1)
      {
        alert("Component '" + componentName + "' not found!");
      }
    }

    return id;
}

// Registers a component with the form manager
function formManagerRegister(component)
{
    var n;

    component.parentID = this.findComponent(component.parentName);    
    this.components[this.components.length] = component;
}

// Clears the entire form.
function formManagerClearAll()
{
    var n;
    var component;

    for(n=0;n<this.components.length;n++)
    {
      component = this.components[n];
      if(component.parentID == -1)
      {
        this.clearID(n, true);
      }
    }
}

// Updates the form after the components state changed.
function formManagerChange(componentName)
{
    var id;

    id = this.findComponent(componentName);
    this.changeID(id, false);    
}

// Updates a controls visual settings after it changed.
function formManagerChangeID(id, forceUpdate)
{
    var n;
    var component;

    for(n=0;n<this.components.length;n++)
    {
      component = this.components[n];
      if(component.parentID == id)
      {
        if(component.isMatch(this.getValue(this.components[id])) == true)
        {          
          this.showID(n, forceUpdate);
        }            
        else
        {
          this.hideID(n, forceUpdate);
        }
      }
    }      
}

// Set the value of a component.
function formManagerSetValue(component, value)
{
    var c;
    var img;

    if(component.typeID != TYPEID_NONE)
    {
      switch(component.typeID)
      {
        case TYPEID_IMAGEBUTTON:
        {
          component.state = value;
    
          img = document.getElementById(component.divName);
          if(value == 'on')
          {
            img.src = component.aImage;
          }
          else
          {
            img.src = component.nImage;
          }
          break;
        }

        default:
        {
          c = document.forms[this.name].elements[component.controlName];
          c.value = value;
          break;
        }
      }
    }
    else
    {
      alert('Can not set the value of non-control ' + component.name + '.');
    }
}

// Gets the value of a component.
function formManagerGetValue(component)
{    
    var c;
    var value = "";

    if(component.typeID != TYPEID_NONE)
    {
      if(component.typeID == TYPEID_IMAGEBUTTON)
      {
        value = component.state;
      }
      else
      {
        c = document.forms[this.name].elements[component.controlName];

        switch(component.typeID)
        {
          case TYPEID_SELECTBOX:
          {
            value = c.options[c.selectedIndex].value;
            break;
          }
 
          default:
          {
            value = c.value;
            break;
          }
        }
      }
    }    

    return value;
}

function formManagerHideID(id, forceUpdate)
{
    var n;
    var component;
    var div;

    component = this.components[id];
    if(component.visible == true || forceUpdate)
    {
      div = document.getElementById(component.divName);
      div.style.display = "none";
      this.clearID(id, forceUpdate);
        
      component.visible = false;
    }
}

function formManagerShowID(id, forceUpdate)
{
    var n;
    var component;
    var div;

    component = this.components[id];
    if(component.visible == false || forceUpdate)
    {
      div = document.getElementById(component.divName);
      div.style.display = "block";

      component.visible = true;
    }
}

function formManagerClearID(id, forceUpdate)
{    
    var currentValue;
    var component;
    
    component = this.components[id];
    if(component.typeID != TYPEID_NONE)
    {
      currentValue = this.getValue(component);

      if(currentValue != component.defaultvalue || forceUpdate)
      {      
        this.setValue(component, component.defaultValue);
        this.changeID(id, forceUpdate);          
      }
    }
}

function formManagerToggle(componentName)
{
    var component;
    var cur;
    var id;

    id = this.findComponent(componentName);
    component = this.components[id];

    if(component.typeID == TYPEID_IMAGEBUTTON)
    {
      cur = this.getValue(component);
      if(cur == 'on')           
      {
        this.setValue(component, 'off');
      }
      else
      {
        this.setValue(component, 'on');
      }
      this.change(componentName);
    }
    else
    {
      alert("Don't call toggle on anything, but an image button!");
    }
}