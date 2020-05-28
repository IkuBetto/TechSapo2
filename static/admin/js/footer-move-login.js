window.onresize = function() {
	
	let h = document.getElementById('move').clientHeight;
	let b = document.getElementById('body').clientHeight;
	let header = document.getElementById('header').scrollHeight;
	let header2 = document.getElementById('header2').scrollHeight;
	// let row = document.getElementById('row').scrollHeight;
	let window_size=window.parent.screen.height;
	// let footer = document.getElementById('footer').clientHeight;
	if(window_size>row){
		footer=b-header-header2-103.5;
		console.log(window_size);
		document.getElementById('move').style.height = String(footer)+'px';
	}
 
}
window.onload = function() {
	
	let h = document.getElementById('move').clientHeight;
	let b = document.getElementById('body').clientHeight;
	let header = document.getElementById('header').scrollHeight;
	let header2 = document.getElementById('header2').scrollHeight;
	// let row = document.getElementById('row').scrollHeight;
	let window_size=window.parent.screen.height;
	// let footer = document.getElementById('footer').clientHeight;
	if(window_size>row){
		footer=b-header-header2-103.5;
		console.log(window_size);
		document.getElementById('move').style.height = String(footer)+'px';
	}
 
}
