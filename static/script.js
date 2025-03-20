document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("toggle-theme");
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

document.getElementById("search-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevents page reload

    const query = document.getElementById("search-input").value.trim();
    const recipeContainer = document.getElementById("recipe-container");

    if (query === "") {
        recipeContainer.innerHTML = "<p>Please enter a recipe name.</p>";
        return;
    }

    fetch(`/get_recipe?name=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.recipe) {
                recipeContainer.innerHTML = `<h3>${data.recipe.name}</h3><p>${data.recipe.description}</p>`;
            } else {
                recipeContainer.innerHTML = "<p>Recipe not found.</p>";
            }
        })
        .catch(error => {
            console.error("Error fetching recipe:", error);
            recipeContainer.innerHTML = "<p>Error fetching recipe.</p>";
        });
});
