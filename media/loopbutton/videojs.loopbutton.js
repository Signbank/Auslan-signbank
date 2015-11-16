/* ! Loopbutton v1.0.0 Copyright 2014 Charlotte Dunois https://github.com/CharlotteDunois/videojs-loopbutton/blob/master/LICENSE.md ! */
videojs.plugin('loopbutton', function(options) {
	var player = this;
	
	var LoopButton = vjs.Button.extend({
		init: function(player, options) {
			vjs.Button.call(this, player, options);
		}
	});
	
	LoopButton.prototype.buttonText = 'Loop';

	LoopButton.prototype.buildCSSClass = function() {
		return 'vjs-loop-button vjs-control';
	};

	LoopButton.prototype.onClick = function(e){
    	//I changed this part to use loop() function
		if(player.loop() == true) {
			player.loop(false);
			this.removeClass('vjs-control-active');
		} else {
			player.loop(true);
			this.addClass('vjs-control-active');
		}
	};

	player.ready(function(){
		var button = new LoopButton(player,  {
			el: vjs.Component.prototype.createEl('div', {
				className	: 'vjs-loop-button vjs-control',
				innerHTML: '<div class="vjs-control-content"><span class="vjs-control-text">Loop</span></div>',
				role: 'button'
			}) 
		});
		player.controlBar.addChild(button);
		
		//I removed "on ended" event
		//with loop() function there is no need to play the video every time it ends
	});
});
