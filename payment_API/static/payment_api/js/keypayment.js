// const form = document.querySelector('form')
// form.addEventListener('submit',
//     (event) => {
//         event.preventDefault()
//         console.log(document.querySelector('.pin').value)
//     }
// )
// const pricePerDay = document.querySelector('#id_price').value;
const price = document.querySelector('#id_price');
const durationInput = document.querySelector('#id_duration');
const mapOfPaymentOptions = {
    '#id_payment_type_0' : '.acc-details0',
    '#id_payment_type_1' : '.acc-details1',
    // 'currentAbled' : '.acc-details0',
    'currentAbled' : ''              // empty initially and temporarily check the for the checked one in the form
    
};

function ChecknCorrectCurrentEnabledelement () {
    radioElements = document.querySelectorAll('.payment-options');
    for( i of radioElements) {
        if (i.nodeName.toLowerCase() === 'input' && i.type == 'radio'){
            if (i.checked){
                id = '#' + i.id;
                className = mapOfPaymentOptions[id];
                mapOfPaymentOptions['currentAbled'] = className
            }
        }
    }
    console.log(mapOfPaymentOptions);
}
ChecknCorrectCurrentEnabledelement();
function optionElementDisabler(elementSelector) {
    let option = document.querySelector(elementSelector);
    let id = option.id;
    option.addEventListener('change',
        () => {
            let newid = "#"+id
            elementsClassName = mapOfPaymentOptions[newid];        //sorry about the variable naming debugging stuff sorry again
            currentAbled = mapOfPaymentOptions['currentAbled'];

            let currentAbledElements = document.querySelectorAll(currentAbled);
            for (i of currentAbledElements) {
                i.value = '';
                i.disabled = true;
                
            }
            mapOfPaymentOptions['currentAbled'] = elementsClassName;

            let elementstobeabled = document.querySelectorAll(elementsClassName);
            for (i of elementstobeabled) {
                i.disabled = false;
            }
        }
    )
};
for(i of Object.keys(mapOfPaymentOptions)) {
    if (i === 'currentAbled'){
        continue
    }
    optionElementDisabler(i)
}

function getCSRFtoken() {
    const tokenElem = document.getElementsByName('csrfmiddlewaretoken')[0]
    return tokenElem.value
}
fetch ('/payment_api/price-per-day-inquiry/',
    {
        method : 'post',
        headers : {
            'Content-Type':'application/json',
            'X-CSRFToken' : getCSRFtoken(),
        },
        body : 'sup'
    }).then( (response) => {
        if(!response.ok){
            console.log(response.statusText)
        }
        console.log(response);
        return response.json()
    }).then( (data) => {
        const pricePerDay = data['price-per-day']
        durationInput.addEventListener('change',
            (event) => {
                value = event.target.value;
                value = Number(value);
                value = Math.ceil(value);
                durationInput.value = value
                newPriceValue = value * pricePerDay;
                price.value = newPriceValue;
        });
    })
