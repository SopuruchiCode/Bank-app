const accountSelector = document.querySelector(".form-select");
const amountDisplay = document.querySelector(".amount-display");
const transferButton = document.querySelector(".transfer-button-js");
const dollarFormat = new Intl.NumberFormat("en-US",{
    style : "currency",
    currency : "USD"
})
const senderAcc = document.getElementById("id_acc_of_sender");

fetch('/transfer/acc-info/')
    .then((response) => {
        if(!response.ok){
            throw new Error("The response was not okay" + response.statusText);
        };
        return response.json();
    })
    .then((data) => {
        accountSelector.addEventListener("change",(event) => {
            accountNumber = event.target.value;
            balance = Number(data[accountNumber]);
            balance = dollarFormat.format(balance)
            amountDisplay.innerHTML = `${balance}`;
        })
    })
    .catch((error) =>
        {console.log("Failed data retrieval" + error)}
    );


senderAcc.addEventListener("change",(event)=>{
    value =  event.target.value;
    accountSelector.value = value;
    event = new Event("change",
        {"bubbles": false,
            "cancelable":true
        })
    accountSelector.dispatchEvent(event);
})