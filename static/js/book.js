/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header(Scroll Spy)
3. Init SVG
4. Init Single Player

******************************/

$(document).ready(function()
{
	"use strict";

	/*********************************
	1. Vars and Inits
	*********************************/

	var ctrl = new ScrollMagic.Controller();

	setHeader();
	initSvg();
	initSinglePlayer();

	$(window).on('resize', function()
	{
		setHeader();

		setTimeout(function()
		{
			$(window).trigger('resize.px.parallax');
		}, 375);
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	/*********************************
	2. Set Header(Scroll Spy)
	 - 스크롤 움직임을 감지하여 상단 바의 높이와 위치를 조정
	*********************************/

	function setHeader()
	{
		var height = $(window).scrollTop();

		$('.header-container').css("height",
			(parseInt($('.header-container').css('max-height'))-height).toString()+"px")
		$('.header').css("top", (-height).toString()+"px")

	}

	/*********************************
	3. Init SVG
	*********************************/

	function initSvg()
	{
		if($('img.svg').length)
		{
			jQuery('img.svg').each(function()
			{
				var $img = jQuery(this);
				var imgID = $img.attr('id');
				var imgClass = $img.attr('class');
				var imgURL = $img.attr('src');

				jQuery.get(imgURL, function(data)
				{
					// Get the SVG tag, ignore the rest
					var $svg = jQuery(data).find('svg');

					// Add replaced image's ID to the new SVG
					if(typeof imgID !== 'undefined') {
					$svg = $svg.attr('id', imgID);
					}
					// Add replaced image's classes to the new SVG
					if(typeof imgClass !== 'undefined') {
					$svg = $svg.attr('class', imgClass+' replaced-svg');
					}

					// Remove any invalid XML tags as per http://validator.w3.org
					$svg = $svg.removeAttr('xmlns:a');

					// Replace image with new SVG
					$img.replaceWith($svg);
				}, 'xml');
			});
		}	
	}

	/*********************************
	4. Init Single Player
	 - 음악 플레이어 세부 설정
	*********************************/

	function initSinglePlayer()
	{
		if($(".jp-jplayer").length)
		{
			$("#jplayer_1").jPlayer({
				ready: function () {
					$(this).jPlayer("setMedia", {
						title:"기도훈련집",
						artist:"오병이어교회",
						mp3: $("#jplayer_1").attr("value")
					});
				},
				play: function() { // To avoid multiple jPlayers playing together.
					$(this).jPlayer("pauseOthers");
				},
			  	ended: function() { // The $.jPlayer.event.ended event
					$(this).jPlayer("play"); // Repeat the media
				},
				swfPath: "../static/plugins/jPlayer",
				supplied: "mp3",
				cssSelectorAncestor: "#jp_container_1",
				wmode: "window",
				globalVolume: false,
				useStateClassSkin: true,
				autoBlur: false,
				smoothPlayBar: true,
				keyEnabled: true,
				solution: 'html',
				preload: 'metadata',
				volume: 1,
				muted: false,
				backgroundColor: '#000000',
				errorAlerts: false,
				warningAlerts: false
			});
		}
	}

});