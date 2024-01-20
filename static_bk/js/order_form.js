document.addEventListener("DOMContentLoaded", function() {
  // Function to toggle the readonly state of 'termen' field
  function toggleDueDateAdjustable() {
    var checkBox = document.getElementById("id_is_due_date_adjustable");
    var dueDateField = document.getElementById("id_termen");
    dueDateField.readOnly = !checkBox.checked;
  }

  // Add event listener to the checkbox
  var checkBox = document.getElementById("id_is_due_date_adjustable");
  if (checkBox) {
    checkBox.addEventListener("change", toggleDueDateAdjustable);
  }

  // Call the function to set the initial state
  toggleDueDateAdjustable();
});
