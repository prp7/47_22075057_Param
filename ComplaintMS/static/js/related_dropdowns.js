const options = {
    Hostel: ["Aryabhatta", "Sateesh Dhawan", "Visvesvaraya", "Limbdi"],
    Department: ["CSE","APM","ECE","EEE"],
    Library: ["S.D. Library"]
};


// Get references to both dropdowns
const mainDropdown = document.getElementById("domain");
const subDropdown = document.getElementById("domain_name");


// Add an event listener to the mainDropdown
mainDropdown.addEventListener("change", function() {
    const selectedValue = mainDropdown.value;
    const subOptions = options[selectedValue] || [];


    // Clear existing options
    subDropdown.innerHTML = '';


    // Add new options based on the selection
    for (const option of subOptions) {
        const optionElement = document.createElement("option");
        optionElement.value = option;
        optionElement.textContent = option;
        subDropdown.appendChild(optionElement);
    }
});


// Trigger the event to populate the sub-dropdown initially
mainDropdown.dispatchEvent(new Event("change"));
