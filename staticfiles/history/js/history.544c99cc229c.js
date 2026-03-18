const historyAccountSelector = document.querySelector(".history-acc-select");
const logDisplay = document.querySelector(".history-main");
const transferHistoryViewElement = document.querySelector(".transfers-view");
const withdrawalHistoryViewElement = document.querySelector(".withdrawals-view");
const depositHistoryViewElement = document.querySelector(".deposits-view");
const functionCaller = {
    'transfer-view': transferHistoryViewer,
    'withdrawal-view': withdrawalHistoryViewer,
    'deposit-view': depositHistoryViewer,
}
const dollarFormat = new Intl.NumberFormat("en-US",{
    style : "currency",
    currency : "USD"
});
let value;
let currentView;
let seeRedeemedCouponList = false;

historyAccountSelector.addEventListener("change",
    (event) => {
        value = event.target.value;
        logDisplay.innerHTML = "";
        if (currentView){
            func = functionCaller[currentView]
            func();
        };}
);
function getCSRFtoken(){
    let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0];
    return csrfToken.value;
};
function getAccountSelectorValue(){
    if (value !== 'Choose Account'){
        return value
    }
     return null;
};
function displayTransferHistory(data,value){
    if (value !== ("Choose Account" || null)){
        logs = data[value];
        logDisplay.innerHTML = `
        <p> Transfers </p>
        <div class="transfer-table">

        <table class="table table-striped">
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Sender</th>
                <th scope="col">Recepient</th>
                <th scope="col">Amount</th>
                <th scope="col"> Folio </th>
                <th scope="col">Date</th>
            </tr>
            </thead>
            <tbody class="js-logs">

            </tbody> 
        </table>
        </div>
        `
        for(i of logs){
            logText = `
            <tr>
            <th scope="row">${i.id}</th>
            <td>${i.sender}</td>
            <td>${i.recepient}</td>
            <td>${dollarFormat.format(i.amount)}</td>
            <td>${i.folio}</td>
            <td>${i.date}</td>
            </tr>
        `;
        document.querySelector('.js-logs').innerHTML += logText;}}
};
function displayWithdrawalHistory(data,value){
    if (value !== ("Choose Account" || null)){
    unclaimedLogs = data[value]["unclaimed"];
    claimedLogs = data[value]["claimed"]
     
    logDisplay.innerHTML = `
        <!--<div class="title-and-table">-->
            <div class="container">
                <div class="con-unclaimed con my-active" id="unclaimed"> UNCLAIMED WITHDRAWALS</div>
                <div class="con-claimed con" id="claimed"> CLAIMED WITHDRAWALS </div>
            </div>
            <div class="my-table1">
            <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Amount</th>
                    <th scope="col">Coupon Code</th>
                    <th scope="col">Redeemed</th>
                    <th scope="col"> Date </th>
                </tr>
                </thead>
                <tbody class="log-table">

                </tbody> 
            </table>
            </div>
        <!--</div>-->
        `
        document.querySelector(".log-table") .innerHTML = ""
        if(seeRedeemedCouponList){
            for(log of claimedLogs){
                logText = `
                <tr>
                    <th scope="row">${log.id}</th>
                    <td>${dollarFormat.format(log.amount)}</td>
                    <td class="coupon-display">${log["coupon_code"]}</td>
                    <td>${log.redeemed}</td>
                    <td>${log.date}</td>
                </tr>`
                document.querySelector(".log-table") .innerHTML += logText
            };
        } 
        else {
            for(log of unclaimedLogs){
                logText = `
                <tr>
                    <th scope="row">${log.id}</th>
                    <td>${dollarFormat.format(log.amount)}</td>
                    <td class="coupon-display">${log["coupon_code"]}</td>
                    <td>${log.redeemed}</td>
                    <td>${log.date}</td>
                </tr>`
                document.querySelector(".log-table") .innerHTML += logText
            };
        }

        const unclaimedViewElement= document.querySelector(".con-unclaimed");
        const claimedViewElement= document.getElementById("claimed");

        unclaimedViewElement.addEventListener("click",
            () => {
                seeRedeemedCouponList = false;
                json_data = sessionStorage.getItem("data");
                data = JSON.parse(json_data);
                displayWithdrawalHistory(data,getAccountSelectorValue());
            }
        )
        claimedViewElement.addEventListener("click",
            () => {
                seeRedeemedCouponList = true;
                json_data = sessionStorage.getItem("data");
                data = JSON.parse(json_data);
                displayWithdrawalHistory(data,getAccountSelectorValue());
                document.getElementById('claimed').classList.add("my-active");
                document.querySelector('.con-unclaimed').classList.remove("my-active");
            }
        )
}
};
function displayDepositHistory(data,value){
    if(value !== ("Choose Account"  || null)){
        logs = data[value];

        logDisplay.innerHTML = `
        <p> Deposits </p>
        <div class="deposit-table">

        <table class="table table-striped">
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Depositor Name</th>
                <th scope="col">Amount</th>
                <th scope="col">Date</th>
            </tr>
            </thead>
            <tbody class="js-logs">

            </tbody> 
        </table>
        </div>
        `
        for(i of logs){
            logText = `
            <tr>
            <th scope="row">${i.id}</th>
            <td>${i["depositor-name"]}</td>
            <td>${dollarFormat.format(i.amount)}</td>
            <td>${i.date}</td>
            </tr>
        `;
        document.querySelector('.js-logs').innerHTML += logText;}
        
    }
};

function transferHistoryViewer(){
    currentView = 'transfer-view';
    fetch("/history/js-transfer-history/",
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFtoken()
        },
        body: JSON.stringify({demand:"transfer-data"}),   
    })
    .then((response) => {return response.json()})
    .then((data) => {
        logDisplay.innerHTML = ""
           displayTransferHistory(data,getAccountSelectorValue())
        })
    .catch((error) => {console.log("Error",error)})
};
function withdrawalHistoryViewer(){
    currentView = 'withdrawal-view';
    fetch('/history/js-withdrawal-history/',
    {
        method: "post",
        headers: {
            "Content-Type":"application/json",
            "X-CSRFToken":getCSRFtoken()
        },
        body: JSON.stringify({"demand" : "withdrawal-data"})
        
    }
).then((response) => {
    return response.json()}
).then((data) => {
    logDisplay.innerHTML = "";
    sessionStorage.setItem('data',JSON.stringify(data))
    displayWithdrawalHistory(data,getAccountSelectorValue());
})
.catch((error) => {console.error("error",error)})
};
function depositHistoryViewer(){
    currentView = 'deposit-view'

    fetch("/history/js-deposit-history/",
        {
            method: "POST",
            headers: {
                "Content-Type":"application/json",
                "X-CSRFToken" : getCSRFtoken()
            },
            body:JSON.stringify({"demand":"deposit Logs"})
        }
    )
    .then((response) => {
        console.log(response)
        return response.json()
    })
    .then((data) => {
        logDisplay.innerHTML = "";
        displayDepositHistory(data,getAccountSelectorValue());
    })
    .catch((error) => {console.log(error)})
}

transferHistoryViewElement.addEventListener('click', transferHistoryViewer);
withdrawalHistoryViewElement.addEventListener("click", withdrawalHistoryViewer);
depositHistoryViewElement.addEventListener("click", depositHistoryViewer);
