const my_symptoms = new Array(131).fill(false);


function toggle_symptom(symptom_id) {
    my_symptoms[symptom_id] = !my_symptoms[symptom_id]
}

const buttons = document.querySelectorAll('.grid button')
const result = document.getElementById('result')
buttons.forEach(button => {
    button.addEventListener('click', () => {
        button.classList.toggle('active')
        toggle_symptom(button.id)
        const counter = document.getElementById('counter')
        counter.innerHTML = 'sintomas seleccionados '+ count_symptoms()
    })
})

//coun number of symptoms selected
function count_symptoms() {
    let count = 0
    for (let i = 0; i < my_symptoms.length; i++) {
        if (my_symptoms[i]) {
            count++
        }
    }
    return count
}

//send symptoms to server
async function send_symptoms() {
    try {
        const response = await fetch('/symptoms', {
            method: 'POST',
            headers: {
                'content-Type': 'application/json',
            },
            body: JSON.stringify(my_symptoms),
        })
        const data = await response.text()
        result.innerHTML = 'resultado: '+ data
    }
    catch (err) {
        result.innerHTML = 'error: '+ err.message;
    }
}
