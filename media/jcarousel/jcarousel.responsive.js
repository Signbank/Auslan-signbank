(function($) {
    $(function() {
        var jcarousel = $('.jcarousel');

        jcarousel
            .on('jcarousel:reload jcarousel:create', function () {
                var carousel = $(this),
                    width = carousel.innerWidth();

                if (width >= 600) {
                    width = width / 3;
                } else if (width >= 350) {
                    width = width / 2;
                }

                //carousel.jcarousel('items').css('width', Math.ceil(width) + 'px');
            })
            .jcarousel({
                //wrap: 'circular'
            });
        
        $('.jcarousel-control-prev')
	        .on('jcarouselcontrol:active', function() {
	            $(this).removeClass('inactive');
	        })
	        .on('jcarouselcontrol:inactive', function() {
	            $(this).addClass('inactive');
	        })
	        .jcarouselControl({
	            target: '-=1'
	        })
	        .on('click', function() {
	            $(".thumbnailiframe").each(function(){
	            	$('#sign_html5_api', $(this).contents())[0].play();
	            });
	        });
	
	    $('.jcarousel-control-next')
	        .on('jcarouselcontrol:active', function() {
	            $(this).removeClass('inactive');
	        })
	        .on('jcarouselcontrol:inactive', function() {
	            $(this).addClass('inactive');
	        })
	        .jcarouselControl({
	            target: '+=1'
	        })
	        .on('click', function() {
	            $(".thumbnailiframe").each(function(){
	            	$('#sign_html5_api', $(this).contents())[0].play();
	            });
	        });
    });
})(jQuery);
