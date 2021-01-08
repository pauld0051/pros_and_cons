function updateSelect({ node, values }) {
    while (node.hasChildNodes()) node.removeChild(node.lastChild)
    for (const value of values) {
        const option = document.createElement("option")
        option.value = option.textContent = value
        node.appendChild(option)
    }
}

const countriesSelect = document.querySelector("#country")
const statesSelect = document.querySelector("#state")

updateSelect({
    node: countriesSelect,
    values: countries.map(country => country.name),
})
// Update it on initialization
updateStatesSelect()
countriesSelect.addEventListener("change", updateStatesSelect)

function updateStatesSelect() {
    const countryName = countriesSelect.value
    const country = countries.find(country => country.name === countryName)
    const states = country.states
    updateSelect({
        node: statesSelect,
        values: states
    })
}