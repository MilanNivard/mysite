//	progression bars left column
function func_bar_2(id_element, expert, beginner)
{	var c = document.getElementById(id_element);
	var ctx = c.getContext("2d");
	
	var my_gradient=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.35;
	ctx.rect(0, 0, beginner * 2.2, 100);
	my_gradient.addColorStop(0,"#7cb5a1");
	my_gradient.addColorStop(0.5,"#86bca9");
	my_gradient.addColorStop(0.5,"#86bca9");
	my_gradient.addColorStop(1,"#7cb5a1");
	ctx.fillStyle=my_gradient;
	ctx.fill();

	var my_gradient2=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.5;
	ctx.rect(0, 0, expert * 2.2, 100);
	my_gradient2.addColorStop(0,"#7cb5a1");
	my_gradient2.addColorStop(0.5,"#86bca9");
	my_gradient2.addColorStop(0.5,"#86bca9");
	my_gradient2.addColorStop(1,"#7cb5a1");
	ctx.fillStyle=my_gradient2;
	ctx.fill();
	}
	
function func_bar(id_element, beginner)
{	var c = document.getElementById(id_element);
	var ctx = c.getContext("2d");
	
	var my_gradient=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.4;
	ctx.rect(0, 0, beginner * 2.2, 100);
	my_gradient.addColorStop(0,"#72b4eb");
	my_gradient.addColorStop(0.5,"#599ed9");
	my_gradient.addColorStop(0.5,"#559cd7");
	my_gradient.addColorStop(1,"#599ed9");
	ctx.fillStyle=my_gradient;
	ctx.fill();
	}

	
//	progression bars questions
function lvl_bar(id_element, progress)
{	var c = document.getElementById(id_element);
	var ctx = c.getContext("2d");
	var my_gradient2=ctx.createLinearGradient(0,0,0,50);

	ctx.beginPath();
	ctx.rect(0, 0, 612, 100);
	my_gradient2.addColorStop(1,"#455f74");
	my_gradient2.addColorStop(0,"#7ca3b5");
	ctx.fillStyle=my_gradient2;
	ctx.fill();

	ctx.beginPath();
	ctx.rect(0, 0, progress * 6.12, 100);
	my_gradient2.addColorStop(0,"#354552");
	ctx.fillStyle=my_gradient2;
	ctx.fill();
	}	
	
function chal_bar(id_element, expert, beginner, correct, mode)
{	var c = document.getElementById(id_element);
	var ctx = c.getContext("2d");
	var my_gradient=ctx.createLinearGradient(0,0,0,50);

	ctx.beginPath();
	ctx.rect(0, 0, 612, 100);
	my_gradient.addColorStop(0,"#e9eceb");
	my_gradient.addColorStop(1,"#FFF");
	ctx.fillStyle=my_gradient;
	ctx.fill();

	ctx.beginPath();
	ctx.rect(0, 0, beginner * 6.12, 100);
	my_gradient.addColorStop(0,"#c2e3d8");
	ctx.fillStyle=my_gradient;
	ctx.fill();

	ctx.beginPath();
	ctx.rect(0, 0, expert * 6.12, 100);
	my_gradient.addColorStop(0,"#99cebc");
	ctx.fillStyle=my_gradient;
	ctx.fill();


	ctx.beginPath();
	ctx.font = 'bold 10pt Helvetica';
	ctx.fillStyle="#395770";
	ctx.fillText(correct, 40, 20);

	ctx.beginPath();
	ctx.font = 'bold 10pt Helvetica';
	ctx.fillStyle="#395770";
	ctx.fillText(mode, 497, 20);
	}

	


	/*
	function func_bar(id_element, expert, beginner)
{	var c = document.getElementById(id_element);
	var ctx = c.getContext("2d");
	
	var my_gradient=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.4;
	ctx.rect(0, 0, beginner * 2.2, 100);
	my_gradient.addColorStop(0,"#72b4eb");
	my_gradient.addColorStop(0.5,"#599ed9");
	my_gradient.addColorStop(0.5,"#559cd7");
	my_gradient.addColorStop(1,"#599ed9");
	ctx.fillStyle=my_gradient;
	ctx.fill();

	var my_gradient4=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 1;
	ctx.rect(0, 0, expert * 2.2, 100);
	my_gradient4.addColorStop(0,"#386691");
	my_gradient4.addColorStop(0.5,"#3b5f81");
	my_gradient4.addColorStop(0.5,"#35597a");
	my_gradient4.addColorStop(1,"#294a69");
	ctx.fillStyle=my_gradient4;
	ctx.fill();
	}

	
	
	
	
	function func_bar_2(id_element, expert, advanced, intermediate, beginner)
{	var c = document.getElementById(id_element);
	var ctx = c.getContext("2d");
	
	var my_gradient=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.2;
	ctx.rect(0, 0, beginner * 2.2, 100);
	my_gradient.addColorStop(0,"#7cb5a1");
	my_gradient.addColorStop(0.5,"#86bca9");
	my_gradient.addColorStop(0.5,"#86bca9");
	my_gradient.addColorStop(1,"#7cb5a1");
	ctx.fillStyle=my_gradient;
	ctx.fill();

	var my_gradient2=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.25;
	ctx.rect(0, 0, intermediate * 2.2, 100);
	my_gradient2.addColorStop(0,"#7cb5a1");
	my_gradient2.addColorStop(0.5,"#86bca9");
	my_gradient2.addColorStop(0.5,"#86bca9");
	my_gradient2.addColorStop(1,"#7cb5a1");
	ctx.fillStyle=my_gradient2;
	ctx.fill();

	var my_gradient3=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.3;
	ctx.rect(0, 0, advanced * 2.2, 100);
	my_gradient3.addColorStop(0,"#7cb5a1");
	my_gradient3.addColorStop(0.5,"#86bca9");
	my_gradient3.addColorStop(0.5,"#86bca9");
	my_gradient3.addColorStop(1,"#7cb5a1");
	ctx.fillStyle=my_gradient3;
	ctx.fill();

	var my_gradient4=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.5;
	ctx.rect(0, 0, expert * 2.2, 100);
	my_gradient4.addColorStop(0,"#7cb5a1");
	my_gradient4.addColorStop(0.5,"#86bca9");
	my_gradient4.addColorStop(0.5,"#86bca9");
	my_gradient4.addColorStop(1,"#7cb5a1");
	ctx.fillStyle=my_gradient4;
	ctx.fill();
	}
	
	function func_bar(id_element, expert, advanced, intermediate, beginner)
{	var c = document.getElementById(id_element);
	var ctx = c.getContext("2d");
	
	var my_gradient=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.5;
	ctx.rect(0, 0, beginner * 2.2, 100);
	my_gradient.addColorStop(0,"#9fcfea");
	my_gradient.addColorStop(0.5,"#a2d1ec");
	my_gradient.addColorStop(0.5,"#9fcfea");
	my_gradient.addColorStop(1,"#6ebce9");
	ctx.fillStyle=my_gradient;
	ctx.fill();

	var my_gradient2=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.5;
	ctx.rect(0, 0, intermediate * 2.2, 100);
	my_gradient2.addColorStop(0,"#386691");
	my_gradient2.addColorStop(0.5,"#2b4d6d");
	my_gradient2.addColorStop(0.5,"#2a4663");
	my_gradient2.addColorStop(1,"#294a69");
	ctx.fillStyle=my_gradient2;
	ctx.fill();

	var my_gradient3=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 0.5;
	ctx.rect(0, 0, advanced * 2.2, 100);
	my_gradient3.addColorStop(0,"#386691");
	my_gradient3.addColorStop(0.5,"#2b4d6d");
	my_gradient3.addColorStop(0.5,"#2a4663");
	my_gradient3.addColorStop(1,"#294a69");
	ctx.fillStyle=my_gradient3;
	ctx.fill();

	var my_gradient4=ctx.createLinearGradient(0,0,0,20);
	ctx.beginPath();
	ctx.globalAlpha = 1;
	ctx.rect(0, 0, expert * 2.2, 100);
	my_gradient4.addColorStop(0,"#386691");
	my_gradient4.addColorStop(0.5,"#3b5f81");
	my_gradient4.addColorStop(0.5,"#35597a");
	my_gradient4.addColorStop(1,"#294a69");
	ctx.fillStyle=my_gradient4;
	ctx.fill();
	}
	*/