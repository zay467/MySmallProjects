var mode = "";
var modemsg = true;
function stat(element) {
  mode = element.id;
  modemsg = false;
  switch (element.id) {
    case "pre":
      swi(true, false, false);
      break;
    case "gold":
      swi(false, true, false);
      break;
    case "silver":
      swi(false, false, true);
      break;
    default:
      break;
  }
}
function swi(p, g, s) {
  var btnp = document.getElementById("pre");
  var btng = document.getElementById("gold");
  var btns = document.getElementById("silver");
  if (p) {
    btnp.style.backgroundColor = "#333";
    btnp.style.color = "#fff";
    btng.style.backgroundColor = "#f4f4f4";
    btng.style.color = "#333";
    btns.style.backgroundColor = "#f4f4f4";
    btns.style.color = "#333";
  } else if (g) {
    btnp.style.backgroundColor = "#f4f4f4";
    btnp.style.color = "#333";
    btng.style.backgroundColor = "#333";
    btng.style.color = "#fff";
    btns.style.backgroundColor = "#f4f4f4";
    btns.style.color = "#333";
  } else if (s) {
    btnp.style.backgroundColor = "#f4f4f4";
    btnp.style.color = "#333";
    btng.style.backgroundColor = "#f4f4f4";
    btng.style.color = "#333";
    btns.style.backgroundColor = "#333";
    btns.style.color = "#fff";
  }
  if (p && g && s) {
    btnp.style.backgroundColor = "#f4f4f4";
    btnp.style.color = "#333";
    btng.style.backgroundColor = "#f4f4f4";
    btng.style.color = "#333";
    btns.style.backgroundColor = "#f4f4f4";
    btns.style.color = "#333";
  }
}
var sub = document.querySelector('input[type="submit"]');
sub.addEventListener("click", function (e) {
  e.preventDefault();
  var fc = false;
  var lc = false;
  var n = document.querySelector("#name");
  var e = document.querySelector("#email");
  var p = document.querySelector("#phone");
  if (modemsg) {
    var mmsg = document.querySelector("#modemsg");
    const m = "Please select package!";
    mmsg.innerHTML = m;
    mmsg.classList.add("error");
    setTimeout(() => (mmsg.style.display = "none"), 3000);
    modemsg = false;
  } else {
    fc = true;
  }
  if (n.value === "" || e.value === "" || p.value === "") {
    var msg = document.querySelector("#msg");
    const m2 = "Please fill all field!";
    msg.innerHTML = m2;
    msg.classList.add("error");
    setTimeout(() => (msg.style.display = "none"), 3000);
  } else {
    lc = true;
  }
  if (fc && lc) {
    console.log(
      ` Mode : ${mode} \n Name : ${n.value} \n Email : ${e.value} \n Phone : ${p.value}`
    );
    n.value = "";
    e.value = "";
    p.value = "";
    swi(true, true, true);
    modemsg = true;
    sub.value = "Done!";
    var nmsg = document.getElementById("msg");
    nmsg.style.display = "none";
    var nmmsg = document.getElementById("modemsg");
    nmmsg.style.display = "none";
    setTimeout(() => (sub.value = "Sign Up"), 2500);
  }
});
