// Get the chosen country after change. First country is now "not specified" 
// which means if any country is chosen, there should be a change. 
document.getElementById("country").addEventListener("change", function() {
    let country_chosen = document.getElementById("country").value;
    console.log(country_chosen);
  });