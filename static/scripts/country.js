// Get the chosen country after change. First country is "not specified" 
// which means if any country is chosen, there will be a change. 
// Even if the original country was in the countries.json file and then 
// the user chooses to un-specify, they can then choose "not specified"
// from the dropdown list.

document.getElementById("country").addEventListener("change", function() {
    const country_change = document.getElementById("country").value;
    console.log(country_change);
    console.log(countries);
    const statesArray = [];
    const Ind = countries.findIndex(e => {
      return e['name'] === country_change
})

if(Ind != -1){
      countries[Ind]['states'].forEach(e=> statesArray.push(e['name']))
}

const selectTag = document.getElementById("state")

statesArray.forEach(e => {
    const option = document.createElement('option')
    option.innerText = e;
    selectTag.appendChild(option)
    
})
});