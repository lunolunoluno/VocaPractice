"use strict";

let target_sentences_list = [];

window.onload = function () {

}

function generateSentences() {
    fetch("http://127.0.0.1:5000/generatesentences").then((response) => {
        const responseData = response.json();
        responseData.then((r) => {
            target_sentences_list = [];
            const sentenceList = document.getElementById("sentenceList");
            sentenceList.innerHTML = "";
            r.forEach((element, index) => {
                target_sentences_list.push(element.sentence);
                sentenceList.innerHTML += `<div id="sentence-${index}">
                    <p id="englishsentence-${index}">${element.english}</p>
                    <input type="text" id="answer-${index}">
                </div>
                <hr>`;
            });
            document.getElementById("checkAnswersBtn").onclick = () => checkAnswers();
            openTab("Exercices");
        });
    }).catch(() => {
        alert("Error when generating sentences!");
    });
}

function checkAnswers(){
    const user_answer_list = [];
    for (let i = 0; i < target_sentences_list.length; i++) {
        user_answer_list.push({
            "sentence": target_sentences_list[i],
            "english": document.getElementById(`englishsentence-${i}`).innerText,
            "answer": document.getElementById(`answer-${i}`).value
        });
    }

    console.log(user_answer_list);
    //TODO: send this list to the backend
    //TODO: update Results tab with info from backend

    openTab("Results");
    document.getElementById("checkAnswersBtn").onclick = null;
}

// modified from https://www.w3schools.com/howto/howto_js_tabs.asp
function openTab(tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    // evt.currentTarget.className += " active";
    document.getElementById(tabName+"-btn").className += " active";
} 
