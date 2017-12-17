//	ajax load
/*
function load_lvl(link_id, value, template){
	$(document).ready(function(){
		$(link_id).click(function(){
			$.ajax({
			data: {select_level: value},
			type: 'GET',})
			$("#questions").load(template);
		});
	});
}
load_lvl("#i_lvl1", 1, "lvl1")
load_lvl("#i_lvl2", 2, "lvl2")
load_lvl("#i_lvl3", 3, "lvl3")
load_lvl("#i_lvl4", 4, "lvl4")
load_lvl("#i_lvl5", 5, "lvl5")
load_lvl("#i_lvl6", 6, "lvl6")
*/

//instant refresh
setInterval(function () {
		   $('#prog_barrus').load('prog_bar');
		   $('#table_mel_ans').load('table_mel_ans');
		   $('#table_pro_ans').load('table_pro_ans');
		}, 100); // milliseconds
		
//setInterval(function () {
//		   $('#playbutton').load('playbutton');
//		}, 500); // milliseconds
		
setInterval(function () {
	$('#left_column').load('left_column');
	$('#left_column_pro').load('left_column_pro');
	$('#table_int').load('table_int');
	$('#table_mel').load('table_mel');
	$('#table_tri').load('table_tri');
	$('#table_sev').load('table_sev');
	$('#table_ext').load('table_ext');
	$('#table_pro').load('table_pro');
	}, 4000); // milliseconds


function strt(interval, value){
	$(interval).on('click', function() {
		$.ajax({
		data: {play: value},
		type: 'GET',})
	});
	
}	
strt("#playbutton",'go')




//	play button
/*
$(document).ready( function(){
    $("#playbutton").click(
        function(){
			$('#playbutton').css("background-image", "url('../../static/images/playbutton.png')");
			$.ajax({data: {play: 'stop'}, type: 'GET',})
			},
		function(){$('#playbutton').css("background-image", "url('../../static/images/pausebutton.png')");
			$.ajax({data: {play: 'go'}, type: 'GET',})
		}
    ).click();
});
*/

//	volume control

//length: how many bars
//height: height of the tallest bar
//nowselected: which bar is selected
function drawvolumecontroller(length,height,nowselected){    
    document.getElementById("volumcontroller").innerHTML = "";
    for (i=0;i<length;i++){
        magassag = 9 + Math.round((1.4)*(length - 2*i)); 
        margintop = height-magassag;
        if (margintop <= 0) {margintop=0;}
        if (i >= nowselected){        
            document.getElementById("volumcontroller").innerHTML = 
            document.getElementById("volumcontroller").innerHTML + 
            '<div  onmouseup="volumecontrolchanged(' + i + 
            ')" style="background-color:#446379;height:' + magassag + 
            'px;margin-top:'+margintop+'px;" class="volumecontrollerbar"></div>';
        } else {
            document.getElementById("volumcontroller").innerHTML = 
            document.getElementById("volumcontroller").innerHTML + 
            '<div  onmouseup="volumecontrolchanged(' + i + 
            ')" style="height:'+magassag+'px;margin-top:' + margintop + 
            'px;"class="volumecontrollerbar"></div>';
        }        
    }    
}
function volumecontrolchanged(newvolume){
    drawvolumecontroller(5,25,newvolume);
		$.ajax({
		data: {new_volume: newvolume},
		type: 'GET',})
		;
	}

$(document).ready( function(){
    drawvolumecontroller(5,25,2);
		$.ajax({
		data: {new_volume: 2},
		type: 'GET',})
		;

});


$("#prac_expl").click(function(){   $("#prac_expl").html(ajax_load).load(loadUrl); 
    });

/*
$(document).ready( function(){
     $("#vol1").toggle(
        function(){$('#vol1').css("background-color", "#7e888f");},
		function(){$('#vol1').css("background-color", "#224662");}		
    ).click();
	 $("#vol2").toggle(
        function(){$('#vol1, #vol2').css("background-color", "#7e888f");},
		function(){$('#vol1, #vol2').css("background-color", "#224662");}		
    ).click();
	 $("#vol3").toggle(
        function(){$('#vol1, #vol2, #vol3').css("background-color", "#7e888f");},
		function(){$('#vol1, #vol2, #vol3').css("background-color", "#224662");}		
    ).click();
	 $("#vol4").toggle(
        function(){$('#vol1, #vol2, #vol3, #vol4').css("background-color", "#7e888f");},
		function(){$('#vol1, #vol2, #vol3, #vol4').css("background-color", "#224662");}		
    ).click();
	$("#vol5").toggle(
        function(){$('#vol1, #vol2, #vol3, #vol4, #vol5').css("background-color", "#7e888f");},
		function(){$('#vol1, #vol2, #vol3, #vol4, #vol5').css("background-color", "#224662");}		
    ).click();
});
*/

