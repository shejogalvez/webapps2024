// data from data.js file

const MAX_PRODUCTOS_SELECTED = 5

function validateTextInputLength(textInput, minLength=0, maxLength=9999) {
  var inputValue = textInput.value.trim();
  
  if (inputValue.length < minLength) {
      errorMsg+= textInput.id + " must be at least " + minLength + " characters long." + "\n"
      valid = false; // Prevent form submission
  }
  if (inputValue.length > maxLength) {
      errorMsg+= textInput.id + " input must be at most " + maxLength + " characters long." + "\n"
      valid = false; // Prevent form submission
  }
}

function validateEmail(emailInput) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(emailInput.value)) {
      errorMsg+= "Must input a valid email" + "\n"
      valid = false; // Prevent form submission
  }
}

function validatePhoneNumber(phoneNumberInput) {
  const regex = /^(\+\d{1,3}\d{9})?$/
  if  (!regex.test(phoneNumberInput.value)) {
    errorMsg+= "Must input a correct phone number" + "\n"
    valid = false; // Prevent form submission
  }
}

function validateCheckBoxesSelected(checkboxesDiv, minLength=0, maxLength=Infinity) {
  var selectedCheckboxCount = 0;
  checkboxesDiv.childNodes.forEach( (option) => {
    if (option.checked) {
      selectedCheckboxCount++;
    }
  });

  if (selectedCheckboxCount > maxLength || selectedCheckboxCount < minLength) {
    errorMsg+= "checkboxes selected in "+checkboxesDiv.id+" must be between "+minLength+" and "+maxLength + "\n"
    valid = false; 
    return;
  }
}

function validateNonNullInput(inputElement) {
  console.log(inputElement.value);
  if (!inputElement.value) {
    valid = false;
    errorMsg+= inputElement.name + " is required" + "\n"
  }
}

function validateFileInput(fileInput, minSize=0, maxSize=Infinity) {
  if (!fileInput) return; 
  
  files = fileInput.files;
  if (files.length < minSize || files.length > maxSize) {
      valid = false;
      errorMsg += "Please select between "+minSize+" and "+maxSize+" files." + "\n"
  }
}

var valid = true;
var errorMsg = "";

// validate data upon submitting
document.getElementById("submit-producto-btn").addEventListener("click", function(event) {
  valid = true;
  errorMsg = "";
  validateNonNullInput(document.getElementById("tipo_producto"));
  validateCheckBoxesSelected(document.getElementById("producto"), 1, MAX_PRODUCTOS_SELECTED);
  validateTextInputLength(document.getElementById("nombre_productor"), 5, 80)
  validateEmail(document.getElementById("email_productor"))
  validatePhoneNumber(document.getElementById("celular_productor"))
  validateNonNullInput(document.getElementById("region"));
  validateNonNullInput(document.getElementById("comuna"));
  validateFileInput(document.getElementById("foto_producto"), 1, 3);
  
  // si form es válido abrir confirmación
  if (valid) {
    document.getElementById("modal").style.display = "block";
  }
  // si no alertar errores
  else {
    alert(errorMsg);
    return
  }
  // no se quiere submitear el form pues no hay backend
  event.preventDefault();
});



