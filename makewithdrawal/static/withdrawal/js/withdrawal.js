const withdrawButton = document.querySelector(".withdraw-button");
const accountInput = document.getElementById("id_account_no");
const amountInput = document.getElementById("id_amount");
const pinInput = document.getElementById("id_pin");
const form = document.getElementById("withdrawal-form");

function getCSRFtoken(){
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0];
    return csrf_token.value;
}

form.addEventListener("submit",(event) => {
    accountVal = accountInput.value;
    amountVal = amountInput.value;
    pinVal = pinInput.value;
    event.preventDefault();

    if(accountVal && amountVal && pinVal){
            const formData = new FormData(form);
            fetch("/withdrawal/",{
                method: "POST",
                headers: {
                    // "Content-Type": "application/json",
                    "Accept" : "application/json",
                    "X-CSRFToken" : getCSRFtoken()
                },
                body: formData
            })
                        .then((response) => {
                            if (!(response.ok)){
                                console.log("error: package not recieved")
                            }
                            return response.json()
                        })
                        .then((data) => {
                            if(data.status === "success"){
                                    alert(
                                    `Account: ${accountVal}\nAmount: ${amountVal}\nCode: ${data["coupon-code"]}
                                        `); 
                               console.log(data);
                                location.reload();}
                            else{
                                console.log(Object.entries(data.errors));
                                for(const [field,errorList] of  Object.entries(data.errors)){
                                    document.getElementById(`${field}ErrorList`).innerHTML = "";
                                    for(error of errorList){
                                        document.getElementById(`${field}ErrorList`).innerHTML += `<li> ${error} </li>`
                                    }
                                }
                            }})
                        .catch((error) => {console.log(error)})}    
        else{
            console.log("no value")
        }});
