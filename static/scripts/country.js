// Get the chosen country after change. First country is "not specified" 
// which means if any country is chosen, there will be a change. 
// even if the original country was in the countries.json file and then 
// the user chooses to un-specify, they can then choose "not specified"
// from the dropdown list. 
document.getElementById("country").addEventListener("change", function() {
    const country_chosen = document.getElementById("country").value; 
  });

// A user can not chose a state without first choosing a country. If "not specified"
// is chosen, the default, "not-specified" state will also be chosen. 

$.ajax({
  url: "countries.json",
  dataType: 'json',
  type: 'get',
  cache: false,
  success: function(data){
  for (let state of data.states) {
    console.log(state.name)
  }
  }
  });
