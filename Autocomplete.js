// Select the input and results container
const resultsBox = document.querySelector(".result-box");
const movieInput = document.getElementById("movie_name");

// Trigger suggestions on keyup
movieInput.onkeyup = function () {
    const input = movieInput.value;

    if (input.length > 0) {
        // Fetch suggestions from the Flask autocomplete route
        fetch(`/autocomplete?q=${input}`)
            .then(response => response.json())
            .then(results => {
                displaySuggestions(results);
            })
            .catch(error => console.error("Error fetching autocomplete results:", error));
    } else {
        // Clear suggestions if the input is empty
        resultsBox.innerHTML = "";
    }
};

// Display the suggestions in the results box
function displaySuggestions(results) {
    resultsBox.innerHTML = ""; // Clear previous suggestions

    results.forEach(movieName => {
        const suggestionItem = document.createElement("div");
        suggestionItem.className = "suggestion-item";
        suggestionItem.textContent = movieName;

        // Add click listener to update input and clear suggestions
        suggestionItem.onclick = function () {
            movieInput.value = movieName;
            resultsBox.innerHTML = ""; // Clear suggestions after selection
        };

        resultsBox.appendChild(suggestionItem);
    });
}
