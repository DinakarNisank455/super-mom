document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    const toggleView = document.getElementById("toggle-view");
    const recipeContainer = document.getElementById("recipe-container");

    // Theme Toggle
    themeToggle.addEventListener("click", function () {
        body.classList.toggle("dark-theme");
        body.classList.toggle("light-theme");
    });

    // View Toggle (Grid / List)
    toggleView.addEventListener("click", function () {
        recipeContainer.classList.toggle("grid-view");
        recipeContainer.classList.toggle("list-view");
    });

    if (recipeContainer.classList.contains("grid-view")) {
        viewIcon.src = "static/icons/list.png"; // Show List Icon
    } else {
        viewIcon.src = "static/icons/grid.png"; // Show Grid Icon
    }
});

