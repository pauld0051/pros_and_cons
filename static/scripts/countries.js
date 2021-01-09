// Get the chosen country after change. First country is "not specified" 
// which means if any country is chosen, there will be a change. 
// Even if the original country was in the countries.json file and then 
// the user chooses to un-specify, they can then choose "not specified"
// from the dropdown list.
$('#state').on('contentChanged', function () {
  $(this).formSelect();
});

const selectTag = document.getElementById("state");
document.getElementById("country").addEventListener("change", function () {
  const country_change = document.getElementById("country").value;
  const statesArray = [];
  const Ind = countries.findIndex(e => {
      return e['name'] === country_change;
  })
  if (Ind != -1) {
      countries[Ind]['states'].forEach(e => statesArray.push(e['name']));
  }
  let str = "";
  statesArray.forEach(e => {
      str += `<option value="${e}">${e}</option>`;
  })
  selectTag.innerHTML = str;
  $("#state").trigger('contentChanged');
});

document.getElementById("country").addEventListener("load", function () {
  const state_change = document.getElementById("country").value;
  const states_changeArray = [];
  const Ind_state = countries.findIndex(e => {
      return e['name'] === state_change;
  })
  if (Ind_state != -1) {
      countries[Ind_state]['states'].forEach(e => states_changeArray.push(e['name']));
  }
  let str = "";
  states_changeArray.forEach(e => {
      str += `<option value="${e}">${e}</option>`;
  })
  selectTag.innerHTML = str;
  $("#state").trigger('contentChanged');
});

$(document).ready(function() { 
  const country_change = document.getElementById("country").value;
  console.log(country_change)
  const statesArray = [];
  const Ind = countries.findIndex(e => {
      return e['name'] === country_change;
  })
  if (Ind != -1) {
      countries[Ind]['states'].forEach(e => statesArray.push(e['name']));
  }
  let str = "";
  statesArray.forEach(e => {
      str += `<option value="${e}">${e}</option>`;
  })
  selectTag.innerHTML = str;
  $("#state").trigger('contentChanged');
});

document.getElementById("country").addEventListener("load", function () {
  const state_change = document.getElementById("country").value;
  const states_changeArray = [];
  const Ind_state = countries.findIndex(e => {
      return e['name'] === state_change;
  })
  if (Ind_state != -1) {
      countries[Ind_state]['states'].forEach(e => states_changeArray.push(e['name']));
  }
  let str = "";
  states_changeArray.forEach(e => {
      str += `<option value="${e}">${e}</option>`;
  })
  selectTag.innerHTML = str;
  $("#state").trigger('contentChanged');
});