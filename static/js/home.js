/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header(Scroll Spy)
3. Init SVG
4. Init Single Player

******************************/

$(document).ready(function() {
	"use strict";

	/*********************************
	1. Init Single Player
	 - 음악 플레이어 세부 설정
	*********************************/
	$("#jplayer_1").jPlayer({
		ready: function () {
			$(this).jPlayer("setMedia", {
				title:"기도훈련집",
				artist:"오병이어교회",
				mp3: $("#jplayer_1").attr("value")
			});
		},
		play: function() { // To avoid multiple jPlayers playing together.
			$("#jplayer_1").jPlayer("play");
			$("#jplayer_2").jPlayer("play");
		},
		ended: function() { // The $.jPlayer.event.ended event
			$("#jplayer_1").jPlayer("play");
			$("#jplayer_2").jPlayer("play");
		},
		pause: function() {
			$("#jplayer_1").jPlayer("pause");
			$("#jplayer_2").jPlayer("pause");
		},
		mute: function() {
			$("#jplayer_1").jPlayer("mute");
		},
		stop: function() {
			$("#jplayer_1").jPlayer("stop");
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

	$("#jplayer_2").jPlayer({
		ready: function () {
			$(this).jPlayer("setMedia", {
				title:"기도훈련집 배경음악",
				artist:"오병이어교회",
				mp3: $("#jplayer_2").attr("value")
			});
		},
		ended: function() { // The $.jPlayer.event.ended event
			$(this).jPlayer("play"); // Repeat the media
		},
		mute: function() {
			$("#jplayer_2").jPlayer("mute");
		},
		swfPath: "../static/plugins/jPlayer",
		supplied: "mp3",
		cssSelectorAncestor: "#jp_container_2",
		wmode: "window",
		globalVolume: false,
		useStateClassSkin: true,
		autoBlur: false,
		smoothPlayBar: true,
		keyEnabled: true,
		solution: 'html',
		preload: 'metadata',
		volume: 0.5,
		muted: false,
		backgroundColor: '#000000',
		errorAlerts: false,
		warningAlerts: false
	});
	
});