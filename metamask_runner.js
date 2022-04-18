

(async function () {

while(true){

  try{
    var actualSubaccount = $(".selected-account__address").textContent
    httpGetAsync("http://localhost:5000/metamask_get_next_sub_account?actual_sub_account=" + actualSubaccount, callback)
  } catch(e){
    console.log("Erro ao chamar servidor ", e);
  }


   if ($(".popover-content button")){
     $(".popover-content button").click();
   }
    var a = document.getElementsByTagName("div");
    var queue;
    for (var i = 0; i < a.length; i++) {
      if (a[i].classList.contains("transaction-list-item--unconfirmed")) {
        queue = a[i];
        break;
      }
    }

    if (typeof queue !== 'undefined') {
      if (queue.getElementsByTagName("h3")[0].getElementsByTagName("div")[0].textContent == "Unapproved") {
        // console.log("New transaction found");
        queue.click();
        await sleep(700);
      }
    }

    var c = document.getElementsByTagName("button");
    var btnConfirm;
    for (var i = 0; i < c.length; i++) {
      if (c[i].textContent == "Confirm" || c[i].textContent == "Sign") {
        btnConfirm = c[i];
        break;
      }
    }
    var btnReject;
    for (var j = 0; j < c.length; j++) {
      if (c[j].textContent == "Reject" || c[j].textContent == "Cancel") {
        btnReject = c[j];
        break;
      }
    }

    if (typeof btnConfirm !== 'undefined' && typeof btnReject !== 'undefined') {
      if (!btnConfirm.disabled) {
        btnConfirm.click();
        await sleep(1000);
      }
      else {
        btnReject.click();
        await sleep(1000);
      }
    }

    await sleep(1000);
  }


})();



async function changeSubaccount(subaccountIndex) {

  try{
    $(".identicon__address-wrapper").click();
  } catch(e){
    console.log("Erro no click inicial ", e);
  }

  await sleep(500); // 1/2 segundos

  try{
    $("div.account-menu__accounts").children[subaccountIndex].click();
  } catch(e){
    // console.log("Erro ao clicar na conta", e);
  }
}

function callback(result) {

  result = JSON.parse(result)
  if (result["to_change"]) {
    var subaccountIndex = result['next_sub_account_index']
    console.log("Sub conta será mudada para " + (subaccountIndex + 1));
    changeSubaccount(subaccountIndex)
  } else {
    // console.log("Ainda não jogou");
  }

}

function httpGetAsync(theUrl, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  }
  xmlHttp.open("GET", theUrl, true); // true for asynchronous
  xmlHttp.send(null);
}


function $(elem) {
	return document.querySelector(elem);
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}