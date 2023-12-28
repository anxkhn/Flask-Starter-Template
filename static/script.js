"use strict";

const bodyElement = document.body;
const darkModeToggle = document.getElementById("selector");
const navbar = document.getElementById("navbar");
const bottomBar = document.getElementById("btbar");
const loginForm = document.getElementById("loginForm"); // Add this line

// Check the initial state of the toggle
if (darkModeToggle.checked) {
  bodyElement.classList.add("dark-mode");
  navbar.classList.add("navbar-dark", "bg-dark");
  bottomBar.classList.add("navbar-dark", "bg-dark");
  loginForm.classList.add("dark-mode"); // Add this line
}

// Listen for changes to the toggle
darkModeToggle.addEventListener("change", function () {
  bodyElement.classList.toggle("dark-mode", darkModeToggle.checked);
  navbar.classList.toggle("navbar-dark", darkModeToggle.checked);
  navbar.classList.toggle("bg-dark", darkModeToggle.checked);
  bottomBar.classList.toggle("navbar-dark", darkModeToggle.checked);
  bottomBar.classList.toggle("bg-dark", darkModeToggle.checked);
  loginForm.classList.toggle("dark-mode", darkModeToggle.checked); // Add this line
});
