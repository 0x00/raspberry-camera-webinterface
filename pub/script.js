btn = document.getElementById("snapshot");
wait = document.getElementById("wait");
count = 0;
btn.onclick = function(e){
  console.log(this);
	count++;
	img = document.getElementById("screen");
	img.src = "/snapshot?"+count;

	btn.style.display = "none";
  	wait.style.display = "";

}

imgtag = document.getElementById("screen");
imgtag.onload = function(e){  
  console.log(this);
  btn.style.display = "";
  wait.style.display = "none";
}
wait.style.display = "none";
