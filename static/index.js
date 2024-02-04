window.onscroll = function() {scrollFunction()};

document.addEventListener("DOMContentLoaded", function() {
    window.onscroll = function() {scrollFunction()};
    
    function scrollFunction() {
      var navbar = document.getElementById("navbar");
      if (navbar && (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50)) {
        navbar.style.backgroundColor = "#333"; // Change background color on scroll
      } else if (navbar) {
        navbar.style.backgroundColor = "transparent"; // Reset background color
      }
    }
});

    