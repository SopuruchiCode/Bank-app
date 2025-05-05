console.log("Thank God.")
const accountSelector = document.querySelector(".form-select");
const balanceDisplay = document.querySelector(".amount-display");
const dollarFormat = new Intl.NumberFormat('en-US',
    {
        style : 'currency',
        currency : 'USD'
    });
fetch("/acc-info")
    .then(response => {
        if(!response.ok){
            throw new Error("Network response was not ok" + response.statusText);
        }
        return response.json();})
//data = {acc-no:balance}
    .then(data => {
        accountSelector.addEventListener("change",(event) => {
            account = event.target.value;
            if (data[account] !== "Choose account"){
                balance = Number(data[account]);
                balance = dollarFormat.format(balance);
                console.log(balance);
                balanceDisplay.innerHTML = `${balance}`;
            }
        })
    })
    .catch(error => {console.log(`error fetching data:${error}`)})