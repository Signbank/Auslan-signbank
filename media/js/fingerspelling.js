/*
 * jQuery Timer Plugin
 * http://www.evanbot.com/article/jquery-timer-plugin/23
 *
 * @version      1.0
 * @copyright    2009 Evan Byrne (http://www.evanbot.com)
 */ 

jQuery.timer = function(time,func,callback){
        var a = {timer:setTimeout(func,time),callback:null}
        if(typeof(callback) == 'function'){a.callback = callback;}
        return a;
};

jQuery.clearTimer = function(a){
        clearTimeout(a.timer);
        if(typeof(a.callback) == 'function'){a.callback();};
        return this;
};


 
function fill_fstable () {
      /* fill the fingerspell table with images */
      $("#fstable td").each(function() {
      letter = $(this).attr("id");
      if ($(this).attr("class") != 'blank') { 
	if (typeof(fsimages[letter]) == 'object') {
	  imagesrc = fsimages[letter][0];
	} else {
	  imagesrc = fsimages[letter];
	}
	/* make a new image */
	var image = new Image();
	$(image).attr('src', baseurl+imagesrc);
	$(this).append(image); 
        $(this).append("<div>"+letter+"</div>");
	$(this).click(function() {
	    display_letter("#mainimg", $(this).attr("id"), 1500);
	});
      }
  });
}

function update_image(imageid, image) {

    $(imageid).attr('src', image); 
}

/* an animation plan is a sequence of objects
   with properties:
   'src' - image source url
   'time' -- time in milliseconds to display
   
    we have two procedures, one to build a plan given
    a word, another to animate a plan
*/

function plan_string(str, speed) {
    plan = [plan_transition(speed)];
    for(var i=0; i<str.length; i++) {
        plan = plan.concat(plan_letter(str[i], speed));
        /* insert a transition between letters */
        if (i<str.length-1) {
            plan = plan.concat(plan_transition(speed));
        }
    } 
    return plan;
}

function plan_transition(speed) {
    return( [{src: baseurl+fsimages["transition"], time: speed/5}]);
}

function plan_letter(letter, speed) { 
    
    letter = letter.toUpperCase();
    
    if (fsimages[letter] == undefined) {
        letter = "transition";
    }
    /* check if we have one or multiple images */ 
    if (typeof(fsimages[letter]) == 'object') {
        /* a sequence, we animate them */
        imglist = fsimages[letter];
        result = [];
        brieftime = speed/4;  /* ms time between images */
        
        for(var i=0; i<imglist.length; i++) {
            result.push({src: baseurl+imglist[i], time: brieftime});
        }
        
        return(result);
        
    } else {
        return([{src: baseurl+fsimages[letter], time: speed}]);
    }
}

/* animate a plan
   show the first image,
   schedule animation of the remainder after the given delay
*/
function animate_plan(imageid, plan) { 
    if (plan.length == 0) {
        return
    }
    step = plan.shift();
    update_image(imageid, step['src']);
    /* define a callback function to do the rest */
    var newfun = function () {
        animate_plan(imageid, plan);
    }
    /* schedule newfn in a bit */
    $.timer(step['time'], newfun);
}


function display_letter(imageid, letter, speed) {
    plan = plan_letter(letter, speed);
    animate_plan(imageid, plan);
}


function display_string(imageid, letter, speed) {
    /* TODO: interrupt any playing animations before starting */
    plan = plan_string(letter, speed); 
    animate_plan(imageid, plan);
}


