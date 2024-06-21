document.addEventListener("DOMContentLoaded", () => {

    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    const header = document.querySelector("header");
  
    themeToggle.addEventListener("click", () => {
        body.classList.toggle("dark");
        header.classList.toggle("dark"); 
        themeToggle.textContent = body.classList.contains("dark") ? "🙂" : "😴";
    });
});