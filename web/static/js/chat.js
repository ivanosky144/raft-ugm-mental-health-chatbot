document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("aspect-sidebar");
    const toggleBtn = document.getElementById("toggle-aspect-sidebar-btn");
        
    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("hidden");

        if (sidebar.classList.contains("hidden")) {
            toggleBtn.textContent = "⮜";
            toggleBtn.style.right = "40px";
        }
        else {
            toggleBtn.textContent = "⮞";
            toggleBtn.style.right = "300px";
        }
    });

});


