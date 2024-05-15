// --- Validation Functions ---

const validateEmail = email => {
  // Email validation using a regular expression
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const validateUserName = userName => userName && userName.length > 4;

const validatePassword = password => {
  // Enforce stronger password rules
  const minLength = 8;
  const hasNumber = /\d/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasUppercase = /[A-Z]/.test(password);

  return password && password.length >= minLength && hasNumber && hasLowercase && hasUppercase;
};

// --- Form Handling ---

const handleFormSubmit = () => {
  console.log("Validating form...");

  const emailInput = document.getElementById("email");
  const userNameInput = document.getElementById("username");
  const passwordInput = document.getElementById("contrasenna");

  let isValid = true;
  let errorMessage = "";

  // Validate inputs
  if (!validateEmail(emailInput.value)) {
    isValid = false;
    errorMessage += "Por favor, ingresa un correo electrónico válido.\n";
    emailInput.style.borderColor = "red";
  } else {
    emailInput.style.borderColor = "";
  }

  if (!validateUserName(userNameInput.value)) {
    isValid = false;
    errorMessage += "Por favor, ingresa un nombre de usuario válido (5 caracteres mínimo).\n";
    userNameInput.style.borderColor = "red";
  } else {
    userNameInput.style.borderColor = "";
  }

  if (!validatePassword(passwordInput.value)) {
    isValid = false;
    errorMessage += "La contraseña debe tener al menos 8 caracteres, incluyendo un número, una minúscula y una mayúscula.\n";
    passwordInput.style.borderColor = "red";
  } else {
    passwordInput.style.borderColor = "";
  }

  // Handle errors or redirect to confessions page
  if (!isValid) {
    alert(errorMessage); // Replace with a user-friendly error display
  } else {
    // Store username in localStorage
    const username = userNameInput.value;
    localStorage.setItem("username", username);

    // Redirect to confessions page
    window.location.href = "../html/confesiones.html";
  }
};

// --- Event Listener ---

const submitButton = document.getElementById("envio");
submitButton.addEventListener("click", handleFormSubmit);