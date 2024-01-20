document.addEventListener("DOMContentLoaded", function() {
  // Function to toggle the readonly state of the 'termen' field
  function toggleTermenReadOnly() {
    var urgentCheckbox = document.getElementById("id_is_due_date_adjustable");
    var termenField = document.getElementById("id_termen");
    
    // If the urgent checkbox is checked, remove the readonly attribute
    if (urgentCheckbox.checked) {
      termenField.removeAttribute("readonly");
    } else {
      termenField.setAttribute("readonly", "readonly");
    }
  }

  // Attach the event listener to the urgent checkbox
  var urgentCheckbox = document.getElementById("id_is_due_date_adjustable");
  if (urgentCheckbox) {
    urgentCheckbox.addEventListener("change", toggleTermenReadOnly);

    // Call the function to set the initial state
    toggleTermenReadOnly();
  }
});
