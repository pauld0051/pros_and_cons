//Hide the state select and only show if a user wants to change their state. 
$(document).ready(function(){
  $("#btn_to_hide").click(function(){
    $("#hide_states").toggleClass("hide");
  });
});

// Get the chosen country and list of states of that country on change in the select dropdown
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
      str += `<option value="${e}" selected>${e}</option>`;
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
      str += `<option value="${e}" selected>${e}</option>`;
  })
  selectTag.innerHTML = str;
  $("#state").trigger('contentChanged');
});

// Allow user to change state even if they aren't changing country 
$(document).ready(function() { 
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
      str += `<option value="${e}" selected>${e}</option>`;
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
      str += `<option value="${e}" selected>${e}</option>`;
  })
  selectTag.innerHTML = str;
  $("#state").trigger('contentChanged');
});