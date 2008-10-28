// Debugging crap

function toggleDebug(currDebug) 
{
    if (document.all) 
    {
      thisDebug = eval("document.all." + currDebug + ".style")
      if (thisDebug.display == "block") 
      {
        thisDebug.display = "none"
      }
      else 
      {
        thisDebug.display = "block"
      }

      return false
    }
    else 
    {
      return true
    }
}

function handleKeypress(event)
{
    var key;
    if(document.layers)
    {
      key=event.which;
    }
    if(document.all)
    {
      event=window.event;
      key=event.keyCode;
    }

    if(key == 27 && event.shiftKey) 
    {
      return toggleDebug('debug');
    }
}

if(document.layers)
{
    window.captureEvents(Event.KEYPRESS);
    window.onkeydown=handleKeypress;
}

if(document.all)
{
    this.focus();
    document.onkeydown=handleKeypress;
} 


// Segment II
function GetStyle(StyleSheet, Selector, Type) 
{
    if(window.navigator.userAgent.indexOf('MSIE') >= 0) 
    {
      for(var i=0; i<document.styleSheets.length; i++) 
      {
        if(document.styleSheets[i].href == StyleSheet)
        {
          for(var j=0; j<document.styleSheets[i].rules.length; j++)
          {
            if(window.navigator.userAgent.indexOf('Windows') >= 0) 
            {
              if(document.styleSheets[i].rules[j].selectorText == Selector)
              {
                return eval('document.styleSheets[i].rules[j].style.' + Type);
              }
            }
            else 
            {
              if(document.styleSheets[i].rules[j].selectorText == '*' + Selector)
              {
                return eval('document.styleSheets[i].rules[j].style.' + Type);
              }
            }
          }
          alert('\'' + Selector + '\' does not exist in \'' + StyleSheet + '\'.');
          return '';
        }
      }
      window.status = '\'' + StyleSheet + '\' does not exist.';
      return '';
    }
    else 
    {
      for(var i=0; i<document.styleSheets.length; i++) 
      {
        if(document.styleSheets[i].href == document.location.href.replace(/[^\/]+$/, '') + StyleSheet) 
        {
          for(var j=0; j<document.styleSheets[i].cssRules.length; j++)
          {
            if((',' + document.styleSheets[i].cssRules[j].selectorText.replace(/ /g, '') + ',').indexOf(',' + Selector + ',') >= 0)
            {
              return eval('document.styleSheets[i].cssRules[j].style.' + Type);
            }
          }
          alert('\'' + Selector + '\' does not exist in \'' + StyleSheet + '\'.');
          return '';
        }
      }              
      window.status = '\'' + StyleSheet + '\' does not exist.';
      return '';
    }
}

// Segment III

function ForQuestion(QuestionNo) 
{
    if ('0' != '0' && '0' != '')
    {
      return forquestion = ' for question ' + QuestionNo + '.';
    }
    else
    {
      return forquestion = ' for the highlighted question.';
    }
}

function findPosition(list,value) 
{
    for (i=0; i<list.length; i++) 
    {
      if (list[i]==value) 
      {
        return i;
      }
    }
    
    return "not found";
}

if (document.images) 
{
    submitanswer_norm = new Image(); submitanswer_norm.src = "TIMELibrary/time/images/submitanswer_norm.gif";
    submitanswer_over = new Image(); submitanswer_over.src = "TIMELibrary/time/images/submitanswer_over.gif";
}

/* Function that swaps images. */
function di20(id, newSrc) 
{
    var theImage = FWFindImage(document, id, 0);
    if(theImage) 
    {
      theImage.src = newSrc;
    }
}

/* Functions that track and set toggle group button states. */
function FWFindImage(doc, name, j) 
{
    var theImage = false;
    if(doc.images) 
    {
      theImage = doc.images[name];
    }

    if (theImage) 
    {
      return theImage;
    }

    if (doc.layers) 
    {
      for(j = 0; j < doc.layers.length; j++) 
      {
        theImage = FWFindImage(doc.layers[j].document, name, 0);
        if(theImage) 
        {
          return (theImage);
        }
      }
    }

    return (false);
}

function isNum(passedVal) 
{
    for(z=0; z<passedVal.length; z++) 
    {
      if (passedVal.charAt(z) < "0") 
      {
        return false;
      }

      if (passedVal.charAt(z) > "9") 
      {
        return false;
      }
    }

    return true;
}

function isNum2(passedVal) {
	var num_format = "+-.0123456789";
	for (index=0; index<passedVal.length; index++) {
		check_char = num_format.indexOf(passedVal.charAt(index))
		if (check_char < 0)
			return false;
		if (passedVal.charAt(index) == "+" || passedVal.charAt(index) == "-") {
			if (index == passedVal.length-1) {
				return false;
			}
			num_format = ".0123456789";
		}
		else if (passedVal.charAt(index) >= "0" && passedVal.charAt(index) <= "9")
			num_format = ".0123456789";
		else if (passedVal.charAt(index) == ".") {
			if (index == passedVal.length-1) {
				return false;
			}
			num_format = "0123456789";
		}
	}
	return true;
}

var moveID = "off"
var answers_left = new Array;
var answers_top = new Array;

function moveIt(index) 
{
    N=(document.all)?0:1;
    if (N) {
	var from = eval('document.a0_' + (index+1));
	var speed = 4;
	clearTimeout(moveID);
	if (Math.abs(from.left - answers_left[index]) < speed) {
		from.left = answers_left[index];
	}
	else if (from.left < answers_left[index]) {
		if (Math.abs(from.left - answers_left[index]) < Math.abs(from.top - answers_top[index])) {
			from.left += speed * (Math.round(Math.abs(from.left - answers_left[index])/Math.abs(from.top - answers_top[index])));
		}
		else {
			from.left += speed;
		}
	}
	else if (from.left > answers_left[index]) {
		if (Math.abs(from.left - answers_left[index]) < Math.abs(from.top - answers_top[index])) {
			from.left -= speed * (Math.round(Math.abs(from.left - answers_left[index])/Math.abs(from.top - answers_top[index])));
		}
		else {
			from.left -= speed;
		}
	}
	if (Math.abs(from.top - answers_top[index]) < speed) {
		from.top = answers_top[index];
	}
	else if (from.top < answers_top[index]) {
		if (Math.abs(from.left - answers_left[index]) < Math.abs(from.top - answers_top[index])) {
			from.top += speed;
		}
		else {
			from.top += speed * (Math.round(Math.abs(from.top - answers_top[index])/Math.abs(from.left - answers_left[index])));
		}
	}
	else if (from.top > answers_top[index]) {
		if (Math.abs(from.left - answers_left[index]) < Math.abs(from.top - answers_top[index])) {
			from.top -= speed;
		}
		else {
			from.top -= speed * (Math.round(Math.abs(from.top - answers_top[index])/Math.abs(from.left - answers_left[index])));
		}
	}
	if (from.left == answers_left[index] && from.top == answers_top[index]) {
		index++;
		if ((index < answers_left.length) && (index < answers_top.length)) {
			moveID = setTimeout("moveIt("+index+")",1);
		}
		else {
			for (i=0;i<(document.forms[0].NumberOfQuestions.value);i++) {
				eval('document.t0'+(i+1)+'.left=-100');
				eval('document.c0'+(i+1)+'.top=-100');
			}
			setTimeout("document.forms[0].submit()",1500);
		}
	}
	else {
		moveID = setTimeout("moveIt("+index+")",1);
	}
}
else {
	var from = eval('document.all.a0' + (index+1));
	var speed = 4;
	clearTimeout(moveID);
	if (Math.abs(from.style.pixelLeft - answers_left[index]) < speed) {
		from.style.pixelLeft = answers_left[index];
	}
	else if (from.style.pixelLeft < answers_left[index]) {
		if (Math.abs(from.style.pixelLeft - answers_left[index]) < Math.abs(from.style.pixelTop - answers_top[index])) {
			from.style.pixelLeft += speed * (Math.round(Math.abs(from.style.pixelLeft - answers_left[index])/Math.abs(from.style.pixelTop - answers_top[index])));
		}
		else {
			from.style.pixelLeft += speed;
		}
	}
	else if (from.style.pixelLeft > answers_left[index]) {
		if (Math.abs(from.style.pixelLeft - answers_left[index]) < Math.abs(from.style.pixelTop - answers_top[index])) {
			from.style.pixelLeft -= speed * (Math.round(Math.abs(from.style.pixelLeft - answers_left[index])/Math.abs(from.style.pixelTop - answers_top[index])));
		}
		else {
			from.style.pixelLeft -= speed;
		}
	}
	if (Math.abs(from.style.pixelTop - answers_top[index]) < speed) {
		from.style.pixelTop = answers_top[index];
	}
	else if (from.style.pixelTop < answers_top[index]) {
		if (Math.abs(from.style.pixelLeft - answers_left[index]) < Math.abs(from.style.pixelTop - answers_top[index])) {
			from.style.pixelTop += speed;
		}
		else {
			from.style.pixelTop += speed * (Math.round(Math.abs(from.style.pixelTop - answers_top[index])/Math.abs(from.style.pixelLeft - answers_left[index])));
		}
	}
	else if (from.style.pixelTop > answers_top[index]) {
		if (Math.abs(from.style.pixelLeft - answers_left[index]) < Math.abs(from.style.pixelTop - answers_top[index])) {
			from.style.pixelTop -= speed;
		}
		else {
			from.style.pixelTop -= speed * (Math.round(Math.abs(from.style.pixelTop - answers_top[index])/Math.abs(from.style.pixelLeft - answers_left[index])));
		}
	}
	if (from.style.pixelLeft == answers_left[index] && from.style.pixelTop == answers_top[index]) {
		index++;
		if ((index < answers_left.length) && (index < answers_top.length)) {
			moveID = setTimeout("moveIt("+index+")",1);
		}
		else {
			for (i=0;i<(document.forms[0].NumberOfQuestions.value);i++) {
				//eval('document.all.t0'+(i+1)+'.style.display="none"');
				eval('document.getElementById(\'t0'+(i+1)+'\').style.display="none"');
				//eval('document.all.c0'+(i+1)+'.style.display="none"');
				eval('document.getElementById(\'c0'+(i+1)+'\').style.display="none"');
			}
			setTimeout("document.forms[0].submit()",1500);
		}
	}
	else {
		moveID = setTimeout("moveIt("+index+")",1);
	}
}
}

function validRank(ranks, maxRank, question, k) 
{
	for (var x=0; x<ranks.length; x++) {
		if (ranks[x].value == "" || !isNum(ranks[x].value) || !(ranks[x].value >= 1 && ranks[x].value <= maxRank)) {
			alert('Please enter a number between 1 and ' + maxRank + ForQuestion(k));
			document.location.href = '#anchor' + question;
			ranks[x].focus();
			ranks[x].select();
			return false;
		} else {
			for (var y=0; y<x; y++) {
				if (ranks[x].value == ranks[y].value) {
					alert('You have already entered ' + ranks[x].value + '.  Please enter another number' + ForQuestion(k));
					document.location.href = '#anchor' + question;
					ranks[x].focus();
					ranks[x].select();
					return false;
				}
			}
		}
	}
	return true;
}

function isNumeric(str) 
{
  var len= str.length;
  if (len==0)
    return false;
  var p=0;
  var ok= true;
  var ch= "";
  while (ok && p<len) {
    ch= str.charAt(p);
    if ('0'<=ch && ch<='9')
      p++;
    else
      ok= false;
  }
  return ok;
}

function util_setFocus(oElement, bDoSelect) 
{
	if (oElement && oElement.focus) {
		oElement.focus();
		if (bDoSelect != null && bDoSelect != false) { oElement.select(); }
		return true;
	} else {
		return false;
	}
}

function submitIt(passedForm, submitSilently) 
{

	passedForm.isHidden.value = isHidden;
	passedForm.questionNumber.value = questionNumber;

	var lQuestionType = passedForm.QuestionType.value + ',';
	var aQuestionType = new Array;
	aQuestionType[0] = 0;
	
	while (lQuestionType.indexOf(",") >= 0) {
		aQuestionType[0]++;
		aQuestionType[aQuestionType[0]] = lQuestionType.substring(0, lQuestionType.indexOf(","));
		lQuestionType = lQuestionType.substring(lQuestionType.indexOf(",") + 1, lQuestionType.length);
	}

	var lQuestion = passedForm.question.value + ',';
	var aQuestion = new Array;
	aQuestion[0] = 0;
	while (lQuestion.indexOf(",") >= 0) {
		aQuestion[0]++;
		aQuestion[aQuestion[0]] = lQuestion.substring(0, lQuestion.indexOf(","));
		lQuestion = lQuestion.substring(lQuestion.indexOf(",") + 1, lQuestion.length);
	}

	for (k=1; k<=aQuestionType[0]; k++) {
		if (isHidden[k] == "false") {	
			if (aQuestionType[k] == "calc") {
				if (eval('passedForm.calc'+k+'.value') == "" || !isNum2( eval('passedForm.calc'+k+'.value'))) {
					if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						alert('Please enter a numerical answer' + ForQuestion(k));
						document.location.href = '#anchor' + aQuestion[k];
						util_setFocus( eval('passedForm.calc' + k), true );	// Set focus and call .select()
						return false;
					}
					else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						if (document.forms[0].OptionalAndNotAnswered.value != '')
							document.forms[0].OptionalAndNotAnswered.value += ',';
						document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
					}
				}
			}
			else if (aQuestionType[k] == "open") {
				if (eval('passedForm.'+'answer'+aQuestion[k]+'.value') == '') {
					if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						alert('Please type in your response' + ForQuestion(k));
						document.location.href = '#anchor' + aQuestion[k];
						util_setFocus( eval('passedForm.'+'answer'+aQuestion[k]), true );
						return false;
					}
					else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						if (document.forms[0].OptionalAndNotAnswered.value != '')
							document.forms[0].OptionalAndNotAnswered.value += ',';
						document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
					}
				}
			}
			else if (aQuestionType[k] == "FileUpload") {
				if (eval('passedForm.FileList'+aQuestion[k]+'.options.length') == 0 && eval('passedForm.UploadedFile'+aQuestion[k]+'.value') == '') {
					if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						alert("Please select a file to upload.");
						util_setFocus( eval('passedForm.UploadedFile'+aQuestion[k]) );
						return false;
					}
					else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						if (document.forms[0].OptionalAndNotAnswered.value != '')
							document.forms[0].OptionalAndNotAnswered.value += ',';
						document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
					}
				}
			}
			else if (aQuestionType[k] == "true") {
				if (!eval('passedForm.truefalse'+aQuestion[k]+'[0].checked') && !eval('passedForm.truefalse'+aQuestion[k]+'[1].checked')) {
					if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						alert('Please select either True or False' + ForQuestion(k));
						document.location.href = '#anchor' + aQuestion[k];
						util_setFocus( eval('passedForm.truefalse' + aQuestion[k] + '[0]') );
						return false;
					}
					else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						if (document.forms[0].OptionalAndNotAnswered.value != '')
							document.forms[0].OptionalAndNotAnswered.value += ',';
						document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
					}
				}
			}
			else if (aQuestionType[k] == "multiplesingle") {
				if (isValidMultSg[k] == "false") {
					if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						alert('Please select one answer' + ForQuestion(k));
						
						elemName = eval('passedForm.multsg_' + k + '.value');
						document.location.href = '#anchor' + aQuestion[k];
						
						util_setFocus(eval('passedForm.answer' + aQuestion[k]));
						
						return false;
					}
					else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						if (document.forms[0].OptionalAndNotAnswered.value != '')
							document.forms[0].OptionalAndNotAnswered.value += ',';
						document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
					}
				} else if ( ! submitSilently && isValidMultSg[k] != "true") {
					
						alert('Please enter an explanation' + ForQuestion(k));
						document.location.href = '#anchor' + aQuestion[k];
						
						util_setFocus( eval("passedForm.openexplanation" + isValidMultSg[k]) , true )
						return false;
					
				}
			}
			else if (aQuestionType[k] == "multiplemultiple") {
				var currentQuestionChecked = false;
				var isFirstTime = true;
				for (i=0; i<passedForm.elements.length; i++) {
					if (passedForm.elements[i].type.toLowerCase() == "checkbox" && isNum(passedForm.elements[i].name)) {
					// Code to remove the checkbox in the element id (the 'gi' stands for a case-insensitive global match)
						var re = new RegExp ('checkbox', 'gi');
						var answerNumber = passedForm.elements[i].id.replace(re, '');
						if (answerNumber.indexOf(aQuestion[k]+"_") == 0) {
							if (isFirstTime) {
								var currentQuestion = passedForm.elements[i];
								isFirstTime = false;
							}
							if (passedForm.elements[i].checked) {
								currentQuestionChecked = true;
							}
						}
					}
				}
				if (!currentQuestionChecked) {
					if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						alert('Please select at least one answer' + ForQuestion(k));
						document.location.href = '#anchor' + aQuestion[k];
						util_setFocus( currentQuestion );
						return false;
					}
					else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						if (document.forms[0].OptionalAndNotAnswered.value != '')
							document.forms[0].OptionalAndNotAnswered.value += ',';
						document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
					}
				}
				for (i=1; i<multMultRequiredEx.length; i++) {
					if (! submitSilently) {
						if (multMultRequiredEx[i] != "true" && multMultRequiredEx[i] != "unchecked") {
						
							alert('Please enter an explaination' + ForQuestion(k));
							document.location.href = '#anchor' + aQuestion[k];
							
							util_setFocus( eval("passedForm.openexplanation" + multMultRequiredEx[i]), true );
							return false;
						
						}
					}
				}
			}
			else if (aQuestionType[k] == "multiplerating") {
				if (isHidden[k] == "false") {
					multRatingRows = isValidMultRating[k];
					if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						for (var i=1; i<multRatingRows.length; i++) {
							if (multRatingRows[i] != "true") {
								alert('Please select one answer' + ForQuestion(k));
								document.location.href = '#anchor' + aQuestion[k];
								util_setFocus( eval("passedForm.elements(\"" + multRatingRows[i] + "\")") );
								return false;
								break;
							}
						}
					}
					else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
						var NotAnswered = true;
						for (var i=1; i<multRatingRows.length; i++)
							if (multRatingRows[i] == "true")
								NotAnswered = false;
						if (NotAnswered) {
							if (document.forms[0].OptionalAndNotAnswered.value != '')
								document.forms[0].OptionalAndNotAnswered.value += ',';
							document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
						}
						else if  (! submitSilently) {
							for (var i=1; i<multRatingRows.length; i++) {
								if (multRatingRows[i] != "true") {
								
									alert('Please select one answer' + ForQuestion(k));
									document.location.href = '#anchor' + aQuestion[k];
									util_setFocus( eval("passedForm.elements(\"" + multRatingRows[i] + "\")") );
									return false;
									break;
								
								}
							}
						}
					}
				}
			}
			else if (aQuestionType[k] == "rating") {
				if (eval('passedForm.rating_'+k+'.value') != null) {
					if (eval('passedForm.rating_'+k+'.value') == 0 ) {
						if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
							alert('Please select a rating' + ForQuestion(k));
							document.location.href = '#anchor' + aQuestion[k];
							util_setFocus( eval("passedForm.ratingradio" + k) );
							return false;
						}
						else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
							if (document.forms[0].OptionalAndNotAnswered.value != '')
								document.forms[0].OptionalAndNotAnswered.value += ',';
							document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
						}
					}
				}
			}

	else if (aQuestionType[k] == "drag") {
		var done = true;
		var moved = new Array;
		var qcolor = new Array;
		var acolor = new Array;
	N=(document.all)?0:1;
	if (N) {
		for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
			moved[i] = false;
			qcolor[i] = eval('document.q0'+aQuestion[k]+'_'+(i+1)+'.bgColor');
			acolor[i] = eval('document.a0'+aQuestion[k]+'_'+(i+1)+'.bgColor');
		}
		for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
			if (eval('passedForm.Answer'+aQuestion[k]+'_'+(i+1)+'.value') != '') {
				moved[eval('passedForm.Answer'+aQuestion[k]+'_'+(i+1)+'.value')-1] = true;
			}
			else {
				eval('document.q0'+aQuestion[k]+'_'+(i+1)+'.bgColor="yellow"');
				done = false;
			}
		}
		for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
			if (!moved[i]) {
				eval('document.a0'+aQuestion[k]+'_'+(i+1)+'.bgColor="yellow"');
				done = false;
			}
		}
		if (!done) {

			if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
				alert('Please drag the correct answers to the above questions.');
				for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
					eval('document.all.dq0'+aQuestion[k]+'_'+(i+1)+'.style.color=qcolor['+i+']');
					eval('document.all.da0'+aQuestion[k]+'_'+(i+1)+'.style.color=acolor['+i+']');
				}
				return false;
			}
			else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
				if (document.forms[0].OptionalAndNotAnswered.value != '')
					document.forms[0].OptionalAndNotAnswered.value += ',';
				document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
			}
		}

	}
	else {
		for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
			moved[i] = false;
			qcolor[i] = eval('document.all.dq0'+aQuestion[k]+'_'+(i+1)+'.style.color');
			acolor[i] = eval('document.all.da0'+aQuestion[k]+'_'+(i+1)+'.style.color');
		}
		for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
			if (eval('passedForm.Answer'+aQuestion[k]+'_'+(i+1)+'.value') != '') {
				moved[eval('passedForm.Answer'+aQuestion[k]+'_'+(i+1)+'.value')-1] = true;
			}
			else {
				eval('document.all.dq0'+aQuestion[k]+'_'+(i+1)+'.style.color="red"');
				done = false;
			}
		}
		for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
			if (!moved[i]) {
				eval('document.all.da0'+aQuestion[k]+'_'+(i+1)+'.style.color="red"');
				done = false;
			}
		}
		if (!done) {

			if ( ! submitSilently && (',' + document.forms[0].Optional.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
				alert('Please drag the correct answers to the above questions.');
				for (i=0;i<(eval('document.forms[0].NumberOfQuestions'+aQuestion[k]+'.value'));i++) {
					eval('document.all.dq0'+aQuestion[k]+'_'+(i+1)+'.style.color=qcolor['+i+']');
					eval('document.all.da0'+aQuestion[k]+'_'+(i+1)+'.style.color=acolor['+i+']');
				}
				return false;
			}
			else if ((',' + document.forms[0].OptionalAndNotAnswered.value + ',').indexOf(',' + aQuestion[k] + ',') < 0) {
				if (document.forms[0].OptionalAndNotAnswered.value != '')
					document.forms[0].OptionalAndNotAnswered.value += ',';
				document.forms[0].OptionalAndNotAnswered.value += aQuestion[k];
			}
		}

	}
	}
	}
	}


	
	


	
	
	return true;
}

function changeBox(box) 
{
	//eval('document.all.' + box + '.checked = !document.all.' + box + '.checked');
	eval('document.getElementById(\'' + box + '\').checked = !document.getElementById(\'' + box + '\').checked');
}

function changeRadio(button) 
{
	if (!document.forms[0].answer[button-1].checked) {
		document.forms[0].answer[button-1].checked = true;
	}
}

function changeRadio2(button, radio) 
{
	if (!radio[button-1].checked) {
		radio[button-1].checked = true;
	}
}

function closeallexplanations(questionid) 
{
	//var alltrs = document.all.tags('tr');
	if (window.navigator.userAgent.indexOf('MSIE') >= 0)
		var alltrs = document.getElementsByTagName('tr');
	else
		var alltrs = document.getElementsByTagName('div');
	for (i=0; i<alltrs.length; i++) {
		if (alltrs[i].id != '' && alltrs[i].id.substring(0,alltrs[i].id.indexOf('_')) == 'openexplanationdisplay'+questionid) {
			alltrs[i].style.display = 'none';
				eval('document.forms[0].' + alltrs[i].id.replace(/^openexplanationdisplay/, 'openexplanation') + '.value = \'\'');
		}
	}
}

// Segment IV

var multMultRequiredEx = new Array(0);
var isValidMultSg = new Array(1);
var isHidden = new Array(1);
var questionNumber = new Array(1);
var isValidTrueFalse = new Array(1);
var isValidOpenResponse = new Array(1);
var isValidMultRating = new Array(1);
//var isValidRanking = new Array(1);

function checkValid(questionandanswernumber, positionnumber, openexplaination, isOpenExEntered) {

	if (openexplaination == "1") {
		if (isOpenExEntered == "false") {
			isValidMultSg[positionnumber] = questionandanswernumber;
		} else {
			isValidMultSg[positionnumber] = "true";
		}
	} else {
		isValidMultSg[positionnumber] = "true";
	}

}


function checkMultMultOpenEx(questionAndAnswerid,counter) {
 
	if (eval('questionnaire.checkbox'+questionAndAnswerid+'.checked') == true) {

		if (eval('questionnaire.elements("openexplanation' + questionAndAnswerid+ '").value') == '') {	
			multMultRequiredEx[counter]= questionAndAnswerid;
		} else {
			multMultRequiredEx[counter]= "true";
		}
	} else {
		multMultRequiredEx[counter]= "unchecked";
	}
}