document.addEventListener("DOMContentLoaded", function() {


    const podCells = document.querySelectorAll("div.pod-cell");

    podCells.forEach(cell => {
        const cellId = cell.id;
        const clickListener = createClickListener(cell);
        cell.addEventListener("click", clickListener);
        cell.listener = clickListener;
    });

    const searchBar = document.querySelector(".search-bar");
    searchBar.addEventListener("keydown", function(event) {
        if (event.keyCode === 13 || event.which === 13) {
          handleSearchInput(event);
        }
    });

    // todo, refactor these click handler functions to separate files
    function handleClipClick(data) {
        fetch("/clip-clicked", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id: data })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
              }
            return response.json();
        })
        .then(data => {
            // Handle the response from the Python controller
            // Update the image elements on the page with the new image paths
            const podCells = document.querySelectorAll("div.pod-cell");
            const newData = data["data"];
            const userClicks = new Set(data["user_clicks"]);
            podCells.forEach((cell, index) => {
                const content_p = cell.querySelector("p");
                content_p.textContent = newData[index]["summary"];

                const speaker_h3 = cell.querySelector("h3");
                speaker_h3.textContent = "Speaker: " + newData[index]["speaker"];

                const podNum_h4 = cell.querySelector("h4");
                podNum_h4.textContent = "Podcast Number: " + newData[index]["podNum"];
    
                const id = newData[index]["id"];
                cell.id = id;

                if (userClicks.has(id)) {
                    cell.classList.add("clicked");
                } else {
                    cell.classList.remove("clicked")
                }
                
                const oldClickListener = cell.listener; // Retrieve the reference to the old listener
                cell.removeEventListener("click", oldClickListener);
                const newClickListener = createClickListener(cell);
                cell.addEventListener("click", newClickListener);
                cell.listener = newClickListener; // Store the reference to the new listener
            });
        })
        .catch(error => {
            console.error(error);
        });
    
    }

    function createClickListener(cell) {
        return function(event) {
            event.stopPropagation();
            handleClipClick(cell.id);
        }
    }

    // Function to handle the search input event
    function handleSearchInput(event) {
        // Get the search query entered by the user
        const searchQuery = event.target.value;

        // Call the function to handle the search query
        handleSearch(searchQuery);
    }

    function handleSearch(searchQuery) {
        // Here, you can process the search query as needed
        console.log(searchQuery);

        // Example: Send search query to the server using Fetch API
        fetch("/text-search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ searchQuery: searchQuery })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            // Handle the response from the Python controller
            // Update the image elements on the page with the new image paths
            const imageCells = document.querySelectorAll(".image-cell");
            const newData = data["data"];
            const userClicks = new Set(data["user_clicks"]);
            imageCells.forEach((cell, index) => {
                const image = cell.querySelector("img");
                const imagePath = newData[index]["image_path"];
                const distance = newData[index]["distance"];
                image.src = "/static/" + imagePath;
                image.id = imagePath;
    
                // Update the h2 element with the new image path
                const h2Element = cell.querySelector("h2");
                h2Element.textContent = "Distance to centroid: " + distance;
    
                if (userClicks.has(image.id)) {
                    image.classList.add("clicked-image");
                } else {
                    image.classList.remove("clicked-image")
                }
                
                const oldClickListener = image.listener; // Retrieve the reference to the old listener
                image.removeEventListener("click", oldClickListener);
                const newClickListener = createClickListener(image);
                image.addEventListener("click", newClickListener);
                image.listener = newClickListener; // Store the reference to the new listener
            });
            
            const searchBar = document.querySelector(".search-bar");
            searchBar.innerHTML = "";
            //clear out the text in the searchbar as well
        })
        .catch(error => {
            console.error(error);
        });
    }
});