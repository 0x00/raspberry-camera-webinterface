btn = document.getElementById("snapshot");
hider = document.getElementById("hider");
wait = document.getElementById("wait");
interval = document.getElementById("interval");
count = 0;
btn.onclick = function(e){
  console.log(this);
	count++;

	rotation = 0;
	rotrad = document.getElementsByName("rotation");
	for(var i=0; i<rotrad.length; i++){
		if(rotrad[i].checked)
			rotation = rotrad[i].value;
	}

	img = document.getElementById("screen");
	img.src = "/snapshot?rotation="+rotation+"&counter="+count;

	hider.style.display = "none";
  	wait.style.display = "";

}

imgtag = document.getElementById("screen");
imgtag.onload = function(e){  
  console.log(this);
  hider.style.display = "";
  wait.style.display = "none";

  nextAction = parseInt(interval.value);
  if(isNaN(nextAction))
    return;
  
  setTimeout(btn.click(), nextAction*1000);
}
wait.style.display = "none";
