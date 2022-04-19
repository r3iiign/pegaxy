// ==UserScript==
// @name         jogar v2
// @namespace    http://tampermonkey.net/
// @version      0.8
// @description  ...
// @author       ...
// @match        https://play.pegaxy.io/racing/finish*
// @match        https://play.pegaxy.io/racing/pick-pega*
// @match        https://play.pegaxy.io/racing/*
// @match        https://play.pegaxy.io/racing
// @icon         https://www.google.com/s2/favicons?domain=pegaxy.io
// @grant        none
// @license      MIT
// ==/UserScript==


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const $ = (elem) => {

  if (document.querySelector('iframe')){
    return document.querySelector(elem); // return document.querySelector('iframe').contentWindow.document.body.querySelector(elem);
  } else {
	  return document.querySelector(elem);
  }
};

const $a = (elem) => {
  if (document.querySelector('iframe')){
    return document.querySelectorAll(elem); // return document.querySelector('iframe').contentWindow.document.body.querySelectorAll(elem);
  } else {
	  return document.querySelectorAll(elem);
  }
};

const $remove = (elem) => {
  try{$(elem).style.display = "none";} catch(e){}
};

(async function() {
    var comingSoon = 0;
    var joinMatch = 0;
    var renting = 0;

    var pegaEnergy1 = "";
    var pegaEnergy2 = "";
    var pegaEnergy3 = "";
    var reloaded = true

    while(true){

      if ($('.navbar-nav')){
          while ($('.navbar-nav').children.length > 4){
              $('.navbar-nav').children[0].remove()
          }

          var element = document.createElement("template");
          element.innerHTML = "<li style='font-size: 26px;'>pega1 = "+ pegaEnergy1 + " pega2 = "+ pegaEnergy2 + " pega3 = "+ pegaEnergy2 + "</li>"
          $('.navbar-nav').prepend(element.content.children[0])
      }

      if (reloaded){
        await sleep(1000 * 3);
      }
      reloaded = false

      if (window.location.href == "https://play.pegaxy.io/racing") {
        window.location.href = "https://play.pegaxy.io/racing/pick-pega";
        await sleep(1000 * 2);
        location.reload(true);
      }

      if (window.location.href.startsWith("https://play.pegaxy.io/racing/live")) {
        await sleep(1000 * 2);
        await restart("Reiniciou");
      }

      await sleep(2000);

      try{$("div.bx-content.match-found").style.background =  'none';} catch(e){}
      $remove("div.race-track");
      $remove("div.thumb-cover");
      $remove("div.item-cover-img");
      $remove(".alert-icon-img");

      connect();

      if ($("span.content-name-title") && $("span.content-name-title").textContent == "Renting") {
        renting ++;
      } else {
        renting = 0;
      }

      if (renting > 3) {
        await restart("Sem cavalos - reloading")
      }

      if (isMatchingfreeze()) {
        await restart("Matchingfreeze - reloading")
      }

      if (isCommingSoon()) {
        comingSoon ++;
      } else {
        comingSoon = 0;
      }

      if (comingSoon > 0 && (comingSoon % 5 == 0) ) {

        console.log("comingSoon % 5 - CTRL + F5")
        await sleep(1000 * 1);
        location.reload(true);
      }
      if (comingSoon > 20) {
        await restart("ComingSoon - reloading")
      }


      if (isJoinMatch()) {
        joinMatch ++;
      } else {
        joinMatch = 0;
      }

      if (joinMatch > 30) {
        await restart("JoinMatch - reloading")
      }

      if(!$(".viewAlert")){

        var botaoNextMatch = $(".button-game.pinks");
        if(botaoNextMatch && (botaoNextMatch.innerText == "NEXT MATCH" || botaoNextMatch.innerText == "Find another match")){
          console.log("Vai clicar no next match");
          botaoNextMatch.click();
          await sleep(1000);
        }

        var pegaIndex = await getPegaWithMaxEnergy();

        if(pegaIndex >=0 ){

          try{ pegaEnergy1 = $(".pick-pega > .list-pick > div.item-pega:nth-of-type(1) div div div:nth-of-type(3) div:nth-of-type(2) div div:nth-of-type(2) div span").textContent.split("/25")[0] } catch(e){ pegaEnergy1 = ""}
          try{ pegaEnergy2 = $(".pick-pega > .list-pick > div.item-pega:nth-of-type(2) div div div:nth-of-type(3) div:nth-of-type(2) div div:nth-of-type(2) div span").textContent.split("/25")[0] } catch(e){ pegaEnergy2 = ""}
          try{ pegaEnergy3 = $(".pick-pega > .list-pick > div.item-pega:nth-of-type(3) div div div:nth-of-type(3) div:nth-of-type(2) div div:nth-of-type(2) div span").textContent.split("/25")[0] } catch(e){ pegaEnergy3 = ""}

          console.log("Vai clicar no pega");
          var pegaxy = $a(".item-pega")[pegaIndex];
          pegaxy.click();
          await sleep(1000 * 2);
          // console.log("Clicou no pega");


          var botaoStart = $(".viewButton");
          if(botaoStart && botaoStart.innerText == "START"){
            botaoStart.click();
            // console.log("Clicou no START");
          } else {
            // console.log("Não achou START");
          }
        }
      }
      else {

        if ( $(".alert-desc") && $(".alert-desc").textContent == "You don't have any available Pegas yet. Required at least one to join racing" ) {
            await restart("Não tem Pega na conta - reloading")
        }

        var botao = $(".button-game.pinks");
        if(botao){
          if ($(".alert-desc").textContent == "There are some matchmaking issues. Do you want to reload again or back to lobby?") {
            location.reload(true);
          }
          botao.click();
        }

        botao = $(".button-game.primary");
        if(botao && botao.innerText == "I understand"){
            await sleep(1000 * 1);
            location.reload(true);
        }
      }

    }

    async function getPegaWithMaxEnergy() {

      if (!$(".pick-pega > .list-pick div")){
        return undefined;
      }

      let maxEnergy = -1;
      let pegaMaxEnergy = -1;

      for (var i = 0; i <= 3; i++) {
        const pegaObject = $(".pick-pega > .list-pick > div.item-pega:nth-of-type(" + (i + 1) + ") div div div:nth-of-type(3) div:nth-of-type(2) div div:nth-of-type(2) div span");
        if (pegaObject){
          const actualEnergy = parseInt(pegaObject.textContent.split("/25")[0])
          if (actualEnergy > maxEnergy){
            maxEnergy = actualEnergy;
            if (actualEnergy > 0) {
                pegaMaxEnergy = i
            }
          }
        }
      }

      if (maxEnergy == 0 || pegaMaxEnergy < 0) {

        $(".navbar-assest .assest-inner:nth-of-type(3)").click()
        const subAccount = $("div.navdrop-inner div.sidebar.open div.sidebar-inner div.sidebar-header button span").textContent

        httpGetAsync("http://localhost:5000/account_empty_energy?sub_account=" + subAccount, async (result) => {
          result = JSON.parse(result)
          if (result["to_go_to_next_account"]) {
            await restart("Recarregando após energia zerada - reloading")
          } else {
            location.reload(true);
          }

        })
      }

      return pegaMaxEnergy;

    }

    async function connect() {
      const connect = $("li.nav-item.link-connect.active > span");

      if (!!(connect && connect.textContent == "Connect")){
        console.log("conectando na metamask");
        connect.click();
        await sleep(500);
        $("div.login-btn > div:nth-of-type(2)").click();
        await sleep(2000);
        console.log("fim da conexao");
      }
    }

    function isMatchingfreeze() {
      return  !!($("div.thumb-matching span:nth-of-type(2)") && $("div.thumb-matching span:nth-of-type(2)").textContent > 120)
    }

    function isCommingSoon() {
      return  !!($("div.commingsoon-title") && $("div.commingsoon-title").textContent == "Loading...")
    }

    function isJoinMatch() {
      return  !!($(".title-header") && $(".title-header").textContent == "Joining match")
    }


async function restart(description) {

    console.log("Restart: " + description)


    $(".navbar-assest .assest-inner:nth-of-type(3)").click()
    const subAccount = $("div.navdrop-inner div.sidebar.open div.sidebar-inner div.sidebar-header button span").textContent

    httpGetAsync("http://localhost:5000/pega_race_started?" +
    "sub_account=" + subAccount +
    "&energy_pega_1=" + pegaEnergy1 +
    "&energy_pega_2=" + pegaEnergy2 +
    "&energy_pega_3=" + pegaEnergy3 +
    "&last_race_started_description=" + description
    , ()=>{ pegaEnergy1 = "";pegaEnergy2 = "";pegaEnergy3 = ""; window.location.href = "https://play.pegaxy.io/racing/pick-pega";})

    pegaEnergy1 = "";
    pegaEnergy2 = "";
    pegaEnergy3 = "";
    await sleep(1000 * 5);
    location.reload(true);
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

})();
