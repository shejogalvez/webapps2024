const API_URL = "http://127.0.0.1:5000/api/"

var regionesData;
const selectRegion = document.getElementById('region');
const selectComuna = document.getElementById('comuna');

// function populateRegionSelect() {
//     fetch('https://gist.githubusercontent.com/rhernandog/7d055482f5cc803852a762de873bea62/raw/2bed9aed94ab644533b5e624a4e8f165a4650d48/regiones-provincias-comunas.json') // Replace this URL with your JSON endpoint
//     .then(response => response.json())
//     .then(data => {
//         regionesData = data;
        
//         // Populate select element with options from JSON data
//         data.forEach(option => {
//             const optionElement = document.createElement('option');
//             optionElement.value = option.region; // Set the value of the option
//             optionElement.textContent = option.region; // Set the label of the option
//             selectRegion.appendChild(optionElement);
//         });
//         selectRegion.selectedIndex = -1;
//     });
// }

function populateComunaSelect() {
    selectComuna.innerHTML = '';
    // const region = regionesData.filter((item) => {
    //     return item.region === selectRegion.value;
    // })[0];
    let region_selectedID = selectRegion.value;
    if (!region_selectedID && region_selectedID !== 0) return;
    fetch(API_URL + `get_comunas?region_id=${region_selectedID}`)
      .then((response) => response.json())
      .then( (data) => {
        data.data.forEach(comuna => {
          const optionElement = document.createElement('option');
          optionElement.value = comuna.id; // Set the value of the option
          optionElement.textContent = comuna.nombre; // Set the label of the option
          selectComuna.appendChild(optionElement);
        })
      });
    selectComuna.selectedIndex = -1;
}

function redirectSuccess() {
    
    form = document.getElementById("agregar-producto-form");
    form.submit();
}

populateComunaSelect();
selectRegion.addEventListener("click", populateComunaSelect);

function on_producto_checkbox_click(event) {
    const checkboxesProductoDiv = document.getElementById("producto");
    const selectedValuesSpan = document.getElementById('selectedValues');
    var selectedCheckboxCount = 0;
    checkboxesProductoDiv.childNodes.forEach( (option) => {
      if (option.checked) {
        selectedCheckboxCount++;
      }
    });
  
    if (selectedCheckboxCount > MAX_PRODUCTOS_SELECTED) {
      event.preventDefault(); // Prevent default checkbox behavior
      // Add your custom behavior here
      console.log("numero máximo alcanzado");
      return;
    }
  
    // Add producto to text span
    selectedValuesSpan.textContent = "";
    var i = 0;
    checkboxesProductoDiv.childNodes.forEach( (option) => {
      if (option.checked) {
        if (++i >= MAX_PRODUCTOS_SELECTED) {
          selectedValuesSpan.textContent += option.id;
        }
        else {
          selectedValuesSpan.textContent += option.id + ', ';
        }
      }
      
    });
  }
  
  function on_select_tipo() {
      let checkboxesProductoDiv = document.getElementById("producto");
      let select_tipo = document.getElementById("tipo_producto");
      const selectedValuesSpan = document.getElementById('selectedValues');
      checkboxesProductoDiv.innerHTML = '';
      selectedValuesSpan.innerText = '';
      data[select_tipo.value].forEach(function(option) {
        var checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = option;
        checkbox.name = "fruta_verdura_checkbox";
        checkbox.value = checkbox.id;
        
        var label = document.createElement("label");
        label.htmlFor = checkbox.id;
        label.appendChild(document.createTextNode(option));
        
        checkboxesProductoDiv.appendChild(checkbox);
        checkboxesProductoDiv.appendChild(label);
        checkboxesProductoDiv.appendChild(document.createElement("br"));
  
        // Add event listener to intercept checkbox click
        checkbox.addEventListener("click", on_producto_checkbox_click);
    });
  
  }