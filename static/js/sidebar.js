// /* Set the width of the side navigation to 250px */
// function openNav() {
//   document.getElementById("mySidenav").style.width = "250px";
// }

// /* Set the width of the side navigation to 0 */
// function closeNav() {
//   document.getElementById("mySidenav").style.width = "0";
// }


function openNav() {
  document.getElementById("mySidenav").classList.add("open");
  document.getElementById("mySidenav").classList.remove("close");
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
  document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
function closeNav() {
  document.getElementById("mySidenav").classList.add("close");
  document.getElementById("mySidenav").classList.remove("open");
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
  document.body.style.backgroundColor = "white";
}
document.body.addEventListener('click', () => {
  if (document.getElementById("mySidenav").classList.contains('open')) {
      document.getElementById("mySidenav").classList.add("close");
      document.getElementById("mySidenav").classList.remove("open");
      closeNav();
  }
}, true)