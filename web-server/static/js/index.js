const input = document.getElementById('autocompleteInput');
const optionsContainer = document.getElementById('optionsContainer');

function addMovieResult (movieName) {
    const newDiv = document.createElement('div');
    const textNode = document.createTextNode(movieName);
    newDiv.appendChild(textNode);
    optionsContainer.appendChild(newDiv);
}

function clearResults () {
    optionsContainer.innerHTML = '';
}

function searchMovie (movieName) {
    fetch(`http://localhost:8000/search-movie?name=${encodeURIComponent(movieName)}`)
        .then(response => response.json())
        .then(movies => {
            clearResults();
            movies.forEach(addMovieResult);
        });
}

input.addEventListener('focusin', function () {
    optionsContainer.style.opacity = 1;
});

input.addEventListener('focusout', function () {
    optionsContainer.style.opacity = 0;
});

let timeoutId;

input.addEventListener('keyup', function (event) {
    const searchTerm = event.target.value;

    if(timeoutId) {
        clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(function () {
        searchMovie(searchTerm);
    }, 200);
})

