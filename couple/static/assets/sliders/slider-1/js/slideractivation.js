/*=============== One ==============*/
	
function setREVStartSize(e){
	//window.requestAnimationFrame(function() {				 
		window.RSIW = window.RSIW===undefined ? window.innerWidth : window.RSIW;	
		window.RSIH = window.RSIH===undefined ? window.innerHeight : window.RSIH;	
		try {								
			var pw = document.getElementById(e.c).parentNode.offsetWidth,
				newh;
			pw = pw===0 || isNaN(pw) ? window.RSIW : pw;
			e.tabw = e.tabw===undefined ? 0 : parseInt(e.tabw);
			e.thumbw = e.thumbw===undefined ? 0 : parseInt(e.thumbw);
			e.tabh = e.tabh===undefined ? 0 : parseInt(e.tabh);
			e.thumbh = e.thumbh===undefined ? 0 : parseInt(e.thumbh);
			e.tabhide = e.tabhide===undefined ? 0 : parseInt(e.tabhide);
			e.thumbhide = e.thumbhide===undefined ? 0 : parseInt(e.thumbhide);
			e.mh = e.mh===undefined || e.mh=="" || e.mh==="auto" ? 0 : parseInt(e.mh,0);		
			if(e.layout==="fullscreen" || e.l==="fullscreen") 						
				newh = Math.max(e.mh,window.RSIH);					
			else{					
				e.gw = Array.isArray(e.gw) ? e.gw : [e.gw];
				for (var i in e.rl) if (e.gw[i]===undefined || e.gw[i]===0) e.gw[i] = e.gw[i-1];					
				e.gh = e.el===undefined || e.el==="" || (Array.isArray(e.el) && e.el.length==0)? e.gh : e.el;
				e.gh = Array.isArray(e.gh) ? e.gh : [e.gh];
				for (var i in e.rl) if (e.gh[i]===undefined || e.gh[i]===0) e.gh[i] = e.gh[i-1];
									
				var nl = new Array(e.rl.length),
					ix = 0,						
					sl;					
				e.tabw = e.tabhide>=pw ? 0 : e.tabw;
				e.thumbw = e.thumbhide>=pw ? 0 : e.thumbw;
				e.tabh = e.tabhide>=pw ? 0 : e.tabh;
				e.thumbh = e.thumbhide>=pw ? 0 : e.thumbh;					
				for (var i in e.rl) nl[i] = e.rl[i]<window.RSIW ? 0 : e.rl[i];
				sl = nl[0];									
				for (var i in nl) if (sl>nl[i] && nl[i]>0) { sl = nl[i]; ix=i;}															
				var m = pw>(e.gw[ix]+e.tabw+e.thumbw) ? 1 : (pw-(e.tabw+e.thumbw)) / (e.gw[ix]);					
				newh =  (e.gh[ix] * m) + (e.tabh + e.thumbh);
			}				
			if(window.rs_init_css===undefined) window.rs_init_css = document.head.appendChild(document.createElement("style"));					
			document.getElementById(e.c).height = newh+"px";
			window.rs_init_css.innerHTML += "#"+e.c+"_wrapper { height: "+newh+"px }";				
		} catch(e){
			console.log("Failure at Presize of Slider:" + e)
		}					   
	//});
  };


  /*=============== Two ==============*/

  if(typeof revslider_showDoubleJqueryError === "undefined") {
	function revslider_showDoubleJqueryError(sliderID) {
		var err = "<div class='rs_error_message_box'>";
		err += "<div class='rs_error_message_oops'>Oops...</div>";
		err += "<div class='rs_error_message_content'>";
		err += "You have some jquery.js library include that comes after the Slider Revolution files js inclusion.<br>";
		err += "To fix this, you can:<br>&nbsp;&nbsp;&nbsp; 1. Set 'Module General Options' -> 'Advanced' -> 'jQuery & OutPut Filters' -> 'Put JS to Body' to on";
		err += "<br>&nbsp;&nbsp;&nbsp; 2. Find the double jQuery.js inclusion and remove it";
		err += "</div>";
	err += "</div>";
		var slider = document.getElementById(sliderID); slider.innerHTML = err; slider.style.display = "block";
	}
}	

  /*=============== Three ==============*/
	
  var	revapi1,
  tpj;
function revinit_revslider11() {
jQuery(function() {
  tpj = jQuery;
  revapi1 = tpj("#rev_slider_1_1");
  if(revapi1==undefined || revapi1.revolution == undefined){
	  revslider_showDoubleJqueryError("rev_slider_1_1");
  }else{
	  revapi1.revolution({
		  sliderLayout:"fullwidth",
		  visibilityLevels:"1240,1024,778,480",
		  gridwidth:1920,
		  gridheight:940,
		  perspective:600,
		  perspectiveType:"global",
		  editorheight:"940,768,960,720",
		  responsiveLevels:"1240,1024,778,480",
		  progressBar:{disableProgressBar:true},
		  navigation: {
			  wheelCallDelay:1000,
			  onHoverStop:false,
			  arrows: {
				  enable:true,
				  style:"custom",
				  left: {
					  container:"layergrid",
					  h_offset:197,
					  v_offset:266
				  },
				  right: {
					  h_align:"left",
					  h_offset:243,
					  v_offset:268
				  }
			  }
		  },
		  fallbacks: {
			  allowHTML5AutoPlayOnAndroid:true
		  },
	  });
  }
  
  if(typeof RevSliderSlicey !== "undefined") RevSliderSlicey(revapi1);

});
} // End of RevInitScript


var once_revslider11 = false;
if (document.readyState === "loading") {document.addEventListener('readystatechange',function() { if((document.readyState === "interactive" || document.readyState === "complete") && !once_revslider11 ) { once_revslider11 = true; revinit_revslider11();}});} else {once_revslider11 = true; revinit_revslider11();}