var msf = new FormManager("missingsign");


//                         control name           type           parent control name     parent vals    element id             default
msf.register(new Component("handform"            ,"selectbox"   ,""                     ,""            ,"handformdiv"         ,"0"));
msf.register(new Component("handshapeguidebtn"   ,"imagebutton" ,"handform"             ,"179,180,290" ,"handshapeguidebtn"   ,"off" , "/static/img/button_showguide.gif", "/static/img/button_showguide_select.gif"));
msf.register(new Component("handshapeguide"      ,"none"        ,"handshapeguidebtn"    ,"on"          ,"handshapeguide"      ,""));
msf.register(new Component("handshape"           ,"selectbox"   ,"handform"             ,"179,180,290" ,"handshapediv"        ,"0"));
msf.register(new Component("althandshapeguidebtn","imagebutton" ,"handform"             ,"179,180,290" ,"althandshapeguidebtn","off" , "/static/img/button_showguide.gif", "/static/img/button_showguide_select.gif"));
msf.register(new Component("althandshapeguide"   ,"none"        ,"althandshapeguidebtn" ,"on"          ,"althandshapeguide"   ,""));
msf.register(new Component("althandshape"        ,"selectbox"   ,"handform"             ,"290"         ,"althandshapediv"     ,"0"));
msf.register(new Component("locationguidebtn"    ,"imagebutton" ,"handform"             ,"179,180,290" ,"locationguidebtn"    ,"off" , "/static/img/button_showguide.gif", "/static/img/button_showguide_select.gif"));
msf.register(new Component("locationguide"       ,"none"        ,"locationguidebtn"     ,"on"          ,"locationguide"       ,""));
msf.register(new Component("location"            ,"selectbox"   ,"handform"             ,"179,180,290" ,"locationdiv"         ,"0"));
msf.register(new Component("rellocationguidebtn" ,"imagebutton" ,"handform"             ,"179,180,290" ,"rellocationguidebtn" ,"off" , "/static/img/button_showguide.gif", "/static/img/button_showguide_select.gif"));
msf.register(new Component("rellocationguide"    ,"none"        ,"rellocationguidebtn"  ,"on"          ,"rellocationguide"    ,""));
msf.register(new Component("relativelocation"    ,"selectbox"   ,"handform"             ,"180,290"     ,"relativelocationdiv" ,"0"));
msf.register(new Component("movementmessage"     ,"none"        ,"handform"             ,"179,180,290" ,"movementmessagep"    ,""));
msf.register(new Component("handbodycontact"     ,"selectbox"   ,"handform"             ,"179,180,290" ,"handbodycontactdiv"  ,"0"));
msf.register(new Component("handinteraction"     ,"selectbox"   ,"handform"             ,"180,290"     ,"handinteractiondiv"  ,"0"));
msf.register(new Component("direction"           ,"selectbox"   ,"handform"             ,"179,180,290" ,"directiondiv"        ,"0"));
msf.register(new Component("movementtype"        ,"selectbox"   ,"handform"             ,"179,180,290" ,"movementtypediv"     ,"0"));
msf.register(new Component("smallmovement"       ,"selectbox"   ,"handform"             ,"179,180,290" ,"smallmovementdiv"    ,"0"));
msf.register(new Component("repetition"          ,"selectbox"   ,"handform"             ,"179,180,290" ,"repetitiondiv"       ,"0"));
msf.register(new Component("meaning"             ,"textarea"    ,"handform"             ,"179,180,290" ,"meaningdiv"          ,"" ));
msf.register(new Component("video"               ,"filebox"     ,"handform"             ,"179,180,290" ,"videodiv"            ,"" ));
msf.register(new Component("comments"            ,"textarea"    ,"handform"             ,"179,180,290" ,"commentsdiv"         ,"" ));

// Change Event stubs
function changehandform(){msf.change('handform');}
function changehandshape(){msf.change('handshape');}
function changealthandshape(){msf.change('althandshape');}
function changelocation(){msf.change('location');}
function changerelativelocation(){msf.change('relativelocation');}
function changehandbodycontact(){msf.change('handbodycontact');}
function changehandinteraction(){msf.change('handinteraction');}
function changedirection(){msf.change('direction');}
function changemovementtype(){msf.change('movementtype');}
function changesmallmovement(){msf.change('smallmovement');}
function changerepetition(){msf.change('repetition');}
function changemeaning(){msf.change('meaning');}
function changevideo(){msf.change('video');}
function changecomments(){msf.change('comments');}

function clickhandshapeguidebtn(){msf.toggle('handshapeguidebtn');}
function clickalthandshapeguidebtn(){msf.toggle('althandshapeguidebtn');}
function clicklocationguidebtn(){msf.toggle('locationguidebtn');}
function clickrellocationguidebtn(){msf.toggle('rellocationguidebtn');}

function pageInit()
{
    var f = document.forms['missingsign'];
    var c;

    f.elements['handform'].onchange = changehandform;
    f.elements['handshape'].onchange = changehandshape;
    f.elements['althandshape'].onchange = changealthandshape;
    f.elements['location'].onchange = changelocation;
    f.elements['relativelocation'].onchange = changerelativelocation;
    f.elements['handbodycontact'].onchange = changehandbodycontact;
    f.elements['handinteraction'].onchange = changehandinteraction;
    f.elements['direction'].onchange = changedirection;
    f.elements['movementtype'].onchange = changemovementtype;
    f.elements['smallmovement'].onchange = changesmallmovement;
    f.elements['repetition'].onchange = changerepetition;
    f.elements['meaning'].onchange = changemeaning;
    f.elements['video'].onchange = changevideo;
    f.elements['comments'].onchange = changecomments;

    c = document.getElementById('handshapeguidebtn');
    c.onclick = clickhandshapeguidebtn;
    c = document.getElementById('althandshapeguidebtn');
    c.onclick = clickalthandshapeguidebtn;
    c = document.getElementById('locationguidebtn');
    c.onclick = clicklocationguidebtn;
    c = document.getElementById('rellocationguidebtn');
    c.onclick = clickrellocationguidebtn;

    msf.clearAll();
}

window.onload = pageInitx;
