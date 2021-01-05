// Get the chosen country after change. First country is now "not specified" 
// which means if any country is chosen, there should be a change. 
function countries() {
    document.getElementById("country").addEventListener("change", function() {
    let country_chosen = document.getElementById("country").value;
    console.log(country_chosen);
  });
}

// Let the page load before the script is called.
let timeOut = setTimeout(countries, 2000);