document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("toggle-theme");
    const body = document.body;
    const toggleView = document.getElementById("toggle-view");
    const recipeContainer = document.getElementById("recipe-container");
    const viewIcon = document.getElementById("view-icon"); // Ensure this ID exists in HTML

    // 🔄 Theme Toggle
    if (themeToggle) {
        themeToggle.addEventListener("click", function () {
            body.classList.toggle("dark-theme");
            body.classList.toggle("light-theme");
        });
    }

    // 🔁 Grid/List View Toggle
    if (toggleView && recipeContainer) {
        toggleView.addEventListener("click", function () {
            recipeContainer.classList.toggle("grid-view");
            recipeContainer.classList.toggle("list-view");

            // 🔄 Change Icon Dynamically
            if (viewIcon) {
                if (recipeContainer.classList.contains("grid-view")) {
                    viewIcon.src = "/static/icons/list.png";
                } else {
                    viewIcon.src = "/static/icons/grid.png";
                }
            }
        });
    }

    // 🔍 Handle Search (only if on search page)
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");

    if (searchForm && searchInput) {
        searchForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const query = searchInput.value.trim();

            if (query === "") {
                recipeContainer.innerHTML = "<p>Please enter a recipe name.</p>";
                return;
            }

            fetch(`/get_recipe?name=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.recipe) {
                        recipeContainer.innerHTML = `
                            <h3>${data.recipe.name}</h3>
                            <p>${data.recipe.description}</p>`;
                    } else {
                        recipeContainer.innerHTML = "<p>Recipe not found.</p>";
                    }
                })
                .catch(error => {
                    console.error("Error fetching recipe:", error);
                    recipeContainer.innerHTML = "<p>Error fetching recipe.</p>";
                });
        });
    }
});
document.getElementById("generate-grocery-btn").addEventListener("click", function () {
    const checkboxes = document.querySelectorAll(".recipe-checkbox:checked");
    const grocerySet = new Set();

    checkboxes.forEach(checkbox => {
        const ingredients = checkbox.dataset.ingredients.split(",");
        ingredients.forEach(item => grocerySet.add(item.trim()));
    });

    const groceryList = document.getElementById("grocery-list");
    groceryList.innerHTML = "";

    if (grocerySet.size === 0) {
        groceryList.innerHTML = "<li>No recipes selected.</li>";
    } else {
        Array.from(grocerySet).forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            groceryList.appendChild(li);
        });
    }

    document.getElementById("grocery-list-modal").style.display = "block";
});

function closeGroceryList() {
    document.getElementById("grocery-list-modal").style.display = "none";
}
