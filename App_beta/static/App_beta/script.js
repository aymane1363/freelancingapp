$(document).ready(function() {
  var today = new Date();
  var year = today.getFullYear();
  var month = String(today.getMonth() + 1).padStart(2, '0');
  var day = String(today.getDate()).padStart(2, '0');
  var date = `${year}-${month}-${day}`;
  document.getElementById("dateInput").value = date;

  var now = new Date();
  var hours = String(now.getHours()).padStart(2, '0');
  var minutes = String(now.getMinutes()).padStart(2, '0');
  var time = `${hours}:${minutes}`;
  document.getElementById("timeInput").value = time;

  // This line of code disactivate the remove-button in the onload-body
  $("#remove_btn").prop("disabled", true);
  // This line of code disactivate the apply-button in the onload-body
  $("#apply_btn").prop("disabled", true);
});

function addItems() {
  const selectElement = document.getElementById('exampleInputTools');
  const selectedItem = selectElement.options[selectElement.selectedIndex];

  if (document.getElementById("selected-items")) {
    var selectedItemsList = document.getElementById("selected-items");
  }
  else if (selectedItem.value !== ""){
    var selectedItemsList = document.createElement("ul");
    selectedItemsList.id = "selected-items";
    document.getElementById('tools_handler_div').appendChild(selectedItemsList);
  }
  
  const selectedValue = selectedItem.getAttribute('data-value');
  const existingTool = selectedItemsList.querySelector(`[data-value="${selectedValue}"]`);

  // Skip adding default option to the list
  if (selectedValue === "Choose tools") {
    return;
  }
  // Check if item is already selected
  else if (existingTool) {
    alert(`"${selectedItem.textContent}" is already selected.`);
    return;
  }
  // Otherwise add selected Item
  else {
    const newItem = document.createElement('li');
    newItem.textContent = selectedItem.textContent;
    newItem.setAttribute('data-value', selectedItem.value);
    selectedItemsList.appendChild(newItem);
    
    selectElement.selectedIndex = 0;
    selectedItemsList.style.color = "#14FF14";
    selectedItemsList.style.borderStyle = "solid";
    selectedItemsList.style.borderColor= "white";
    selectedItemsList.style.borderRadius = "5px";

    // Activate remove-btn when it was disactivated
    if (selectedItemsList.querySelectorAll("li").length == 1) {
      $("#remove_btn").prop("disabled", false);
    }
    // Disactivate add-btn when all existant tools are added
    if (selectedItemsList.querySelectorAll("li").length === selectElement.options.length - 1) { // here we substracted the first option which is the default one (choose tools)
      $("#add_btn").prop("disabled", true);
    }
  }
}

function removeItems() {
  const selectedItemsList = document.getElementById('selected-items');
  const selectElement = document.getElementById('exampleInputTools');

  // Activate add-btn when it was disactivated
  if (selectedItemsList.querySelectorAll("li").length === selectElement.options.length - 1) {
    $("#add_btn").prop("disabled", false);
  }

  // Remove the entire <ul> if it contains only 1 <li> else remove the last <li>
  if(selectedItemsList.querySelectorAll("li").length == 1){
    $("#remove_btn").prop("disabled", true);
    document.getElementById('tools_handler_div').removeChild(selectedItemsList);
  }
  else{
      selectedItemsList.removeChild(selectedItemsList.lastChild);
  }
}

function delivery_time_calculation() {
  // Get references to the date, time, and difference input fields
  const dateInput = document.getElementById('dateInput');
  const timeInput = document.getElementById('timeInput');
  var deliveryTimeInput = document.getElementById("delivery_time_readonly")

  const selectedDatetime = new Date(`${dateInput.value}T${timeInput.value}`);
  const currentDatetime = new Date();

  // Check if the selected date/time is in the past
  if (selectedDatetime.getTime() < currentDatetime.getTime()) {
    deliveryTimeInput.style.color = 'red';
    deliveryTimeInput.style.fontSize = '14px';

    // If it is, display an error message and clear the time input field
    deliveryTimeInput.value = 'Please select another date/time, the selected date/time should be in the future';
  } 
  else {
    deliveryTimeInput.style.color = '';
    deliveryTimeInput.style.fontSize = '';

    // Calculate the time deliveryTime in milliseconds
    var deliveryTimeInMs = selectedDatetime.getTime() - currentDatetime.getTime();
    var deliveryTimeInMinutes = Math.floor(deliveryTimeInMs / 60000);

    // Update the deliveryTimeInput field with the calculated deliveryTime
    if (deliveryTimeInMinutes >= 60) {
      var deliveryTimeInHours = Math.floor(deliveryTimeInMinutes / 60);
      deliveryTimeInMinutes = deliveryTimeInMinutes - deliveryTimeInHours*60
      if (deliveryTimeInHours >= 24) {
        var deliveryTimeInDays = Math.floor(deliveryTimeInHours / 24);
        deliveryTimeInHours = deliveryTimeInHours - deliveryTimeInDays*24
        if (deliveryTimeInDays >= 7 && deliveryTimeInDays < 30) {
          var deliveryTimeInWeeks = Math.floor(deliveryTimeInDays / 7);
          deliveryTimeInDays = deliveryTimeInDays - deliveryTimeInWeeks*7;
          deliveryTimeInput.value = `${deliveryTimeInWeeks} weeks ${deliveryTimeInDays} days ${deliveryTimeInHours} hours ${deliveryTimeInMinutes} minutes`;
        }
        else if (deliveryTimeInDays < 7) {
          deliveryTimeInput.value = `${deliveryTimeInDays} days ${deliveryTimeInHours} hours ${deliveryTimeInMinutes} minutes`;
        }
        else {
          var deliveryTimeInMonths = Math.floor(deliveryTimeInDays / 30);
            deliveryTimeInDays = deliveryTimeInDays - deliveryTimeInMonths*30
            deliveryTimeInput.value = `${deliveryTimeInMonths} months ${deliveryTimeInDays} days ${deliveryTimeInHours} hours ${deliveryTimeInMinutes} minutes`;  
        }
      }
      else {
        deliveryTimeInput.value = `${deliveryTimeInHours} hours ${deliveryTimeInMinutes} minutes`;
      }
    }
    else {
      deliveryTimeInput.value = `${deliveryTimeInMinutes} minutes`;
    }
  }
}

setInterval(() => {
  if(document.getElementById("selected-items")){
    var condition_1 = document.getElementById("selected-items").querySelectorAll('li').length !== 0;
  }
  else{
    var condition_1 = false;
  }

  var condition_2 = document.getElementById("exampleFormControlTextarea").value !== '';
  var condition_3 = document.getElementById("InputPricing").value !== '';
  var condition_4 = document.getElementById("delivery_time_readonly").value !== '';
  var condition_5 = document.getElementById("delivery_time_readonly").value !== 'Please select another date/time, the selected date/time should be in the future';

  // This line of code activate the apply-button when all required fields are filled
  if (condition_1 && condition_2 && condition_3 && condition_4 && condition_5) {
    $("#apply_btn").prop("disabled", false);
  }
  else{
    $("#apply_btn").prop("disabled", true);
  }
}, 10); 