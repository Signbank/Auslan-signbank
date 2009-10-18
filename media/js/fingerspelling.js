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


 
/* base url of fingerspelling images */
/* needs to be set in client page */
/* var baseurl='{% auslan_static_prefix %}images/twohanded' */


var fsimages = Object()
fsimages["A"] =  "th_a.jpg";
fsimages["B"] =  "th_b.jpg";
fsimages["C"] =  "th_c.jpg";
fsimages["D"] =  "th_d.jpg";
fsimages["E"] =  "th_e.jpg";
fsimages["F"] =  "th_f.jpg";
fsimages["G"] =  "th_g.jpg";
fsimages["H"] =  ("th_h0.jpg", "th_h1.jpg",  "th_h2.jpg", "th_h3.jpg", "th_h4.jpg");
fsimages["I"] =  "th_i.jpg";
fsimages["J"] =  ("th_j0.jpg", "th_j1.jpg", "th_j2.jpg");
fsimages["K"] =  "th_k.jpg";
fsimages["L"] =  "th_l.jpg";
fsimages["M"] =  "th_m.jpg";
fsimages["N"] =  "th_n.jpg";
fsimages["O"] =  "th_o.jpg";
fsimages["P"] =  "th_p.jpg";
fsimages["Q"] =  "th_q.jpg";
fsimages["R"] =  "th_r.jpg";
fsimages["S"] =  "th_s.jpg";
fsimages["T"] =  "th_t.jpg";
fsimages["U"] =  "th_u.jpg";
fsimages["V"] =  "th_v.jpg";
fsimages["W"] =  "th_w.jpg";
fsimages["X"] =  "th_x.jpg";
fsimages["Y"] =  "th_y.jpg";
fsimages["Z"] =  "th_z.jpg";
fsimages["transition"] = "transition.jpg";

function update_image(imageid, letter) {
    $(imageid).attr('src', baseurl+fsimages[letter]);
}

/* display a fingerspelling sign image or image sequence */
/* TODO: display H and J image sequences */
function display_letter(letter) { 

    if (fsimages[letter] == undefined) {
        letter = "transition";
    }
    
    /* set up the back image with the new letter */
    update_image("#backimg", "transition");
    /* fade out the main image */    
    $("#mainimg").hide();
    /* now replace the main image */
    update_image("#mainimg", letter);
    /* and fade it in */
    $("#mainimg").fadeIn("slow");
}


function display_word(word) {
    /* set the alt attribute of the image to the word in upper case */
    $("#mainimg").attr('alt', word.toUpperCase());
    display_alt_attr();
}

function display_alt_attr() {
    word = $("#mainimg").attr('alt');
    if (word != undefined) { 
        display_letter(word[0]);
        $("#handimage").find("img").attr('alt', word.substring(1));    
        $.timer(1500, display_alt_attr);
    }
}


