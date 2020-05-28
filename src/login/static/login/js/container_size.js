window.onload = function() {
	
	let c = document.getElementById('today-future-client').clientHeight;
	let l = document.getElementById('left-container').clientHeight;
	var p =0;
	
	// let footer = document.getElementById('footer').clientHeight;
	if(c>l){
		l=c+50;
		document.getElementById('left-container').style.height = String(l)+'px';
	}
	else{
		p=50;
	}
	let h = document.getElementById('move').clientHeight;
	let b = document.getElementById('body').clientHeight;
	let header = document.getElementById('header').scrollHeight;
	let header2 = document.getElementById('header2').scrollHeight;
	let row = document.getElementById('row').scrollHeight;
	let window_size=window.parent.screen.height;
	// let footer = document.getElementById('footer').clientHeight;
	if(window_size>row){
		footer=b-header-header2-113+50-p;
		console.log(window_size);
		document.getElementById('move').style.height = String(footer)+'px';
	}
 
}
window.onresize = function() {
	let c = document.getElementById('today-future-client').clientHeight;
	let l = document.getElementById('left-container').clientHeight;
	
	
	// let footer = document.getElementById('footer').clientHeight;
	if(c>l){
		l=c+50;
		document.getElementById('left-container').style.height = String(l)+'px';
	}
	let h = document.getElementById('move').clientHeight;
	let b = document.getElementById('body').clientHeight;
	let header = document.getElementById('header').scrollHeight;
	let header2 = document.getElementById('header2').scrollHeight;
	let window_size=window.parent.screen.height;
	let row = document.getElementById('row').scrollHeight;
	// let footer = document.getElementById('footer').clientHeight;
	if(window_size>row){
		footer=b-header-header2-113+50;
		console.log(window_size);
		document.getElementById('move').style.height = String(footer)+'px';
	}
 
}
