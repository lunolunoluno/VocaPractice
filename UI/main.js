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

    const bodyData = {
        "sentences": user_answer_list
    };
    fetch("http://127.0.0.1:5000/evaluatesentences", {
        method: 'POST',
        body: JSON.stringify(bodyData),
        headers: {
            "Content-Type": "application/json",
        }
    }).then((response) => {
        const responseData = response.json();
        responseData.then((r) => {
            const resultList = document.getElementById("resultList");
            resultList.innerHTML = "";
            r.forEach((element, index) => {
                let diffs = "";
                element.diff.forEach(d => {
                    if (d[1] === " ") {
                        diffs += `<span style="background-color: green;">
                        ${d[0]}
                        </span>`;
                    }else{
                        diffs += `<span style="background-color: red; border: 2px solid black;">
                        ${d[1]}${d[0]}
                        </span>`;
                    }
                });
                resultList.innerHTML += `<div id="result-sentence-${index}">
                    <h2>Sentence ${index+1}</h2>
                    <p><b>English</b>:&emsp;&emsp;&emsp;&emsp;&emsp;${element.english}</p>
                    <p><b>Your Answer</b>:&emsp;&emsp;&emsp;${element.answer}</p>
                    <p><b>Expected Answer</b>:&emsp;${element.sentence}</p>
                    <p>${diffs}</p>
                    <p><b>Score</b>: ${element.score}</p>
                </div>
                <hr>`;
            });
            openTab("Results");
            document.getElementById("checkAnswersBtn").onclick = null;
        });
    }).catch(() => {
        alert("Error when checking the sentences!");
    });
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

    scroll(0,0);
} 
