// --- Validation Functions ---

const validateLength = (confession) => confession && confession.length < 300;

const validateProfanity = (confession) => {
  const bannedWords = ["huevito rey", "sus", "mysterion"];
  return !bannedWords.some((word) => confession.includes(word)); // More efficient using some()
};

// --- Confession Validation ---

const validateConfession = (confession) => {
  const isValid = validateLength(confession) && validateProfanity(confession);
  return { confText: confession, isValid };
};

// --- DOM Elements ---

const confessionTextArea = document.getElementById("conf-text-area");
const confessionList = document.getElementById("conf-list");

// --- Add Confession Function ---

const addConfession = () => {
  const { confText, isValid } = validateConfession(confessionTextArea.value);

  if (!isValid) {
    return; // Early exit if validation fails
  }

  // Create confession container
  const confessionContainer = document.createElement("div");
  confessionContainer.className = "conf-container";

  // Create user image
  const userImage = document.createElement("img");
  userImage.src = "https://via.placeholder.com/75x75";
  userImage.alt = "Placeholder Image";

  // Create username paragraph
  const userNameParagraph = document.createElement("p");
  userNameParagraph.innerText = localStorage.getItem("username") || "Usuario Desconocido"; // Handle missing username

  // Create user container
  const confessionAuthor = document.createElement("div");
  confessionAuthor.className = "conf-author";
  confessionAuthor.append(userImage);
  confessionAuthor.append(userNameParagraph);

  // Create confession text
  const confessionTextElement = document.createElement("p");
  confessionTextElement.innerText = confText;

  // Append elements to confession container
  confessionContainer.append(confessionAuthor);
  confessionContainer.append(confessionTextElement);

  // Append confession container to list
  confessionList.prepend(confessionContainer);
};

// --- Event Listener ---

const submitConfButton = document.getElementById("submit-conf-btn");
submitConfButton.addEventListener("click", addConfession);
