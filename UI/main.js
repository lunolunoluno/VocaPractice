"use strict";

let target_sentences_list = [];

window.onload = function () {
    getParameters();
}


// MENU TAB

function getParameters() {
    fetch("http://127.0.0.1:5000/getparameters").then((response) => {
        const responseData = response.json();
        responseData.then((r) => {
            console.log(r);
            document.getElementById("nbSentencesSlider").value = r.nb_sentences;
            document.getElementById("nbSentencesSpan").innerText = r.nb_sentences;

            const vocabSelect = document.getElementById("selectedVoc");
            selectedVoc.innerHTML = "";
            r.vocab_list.forEach((element, index) => {
                const opt = document.createElement('option');
                opt.value = element[1];
                opt.innerHTML = element[0] + " - " + element[1];
                vocabSelect.appendChild(opt);
            });
            vocabSelect.value = r.selected_vocab;

            const selectedLLM = document.getElementById("selectedLLM");
            selectedLLM.innerHTML = "";
            r.llms.forEach((element, index) => {
                const opt = document.createElement('option');
                opt.value = element;
                opt.innerHTML = element;
                selectedLLM.appendChild(opt); 
            });
            selectedLLM.value = r.selected_llm;

            document.getElementById("nbSentencesBtn").innerText = r.nb_sentences;
            document.getElementById("infoNbSentences").innerText = r.nb_sentences;
            document.getElementById("infoVocab").innerText = r.selected_vocab;
            document.getElementById("infoLLM").innerText = r.selected_llm;
        });
    }).catch(() => {
        alert("Couldn't retreive parameters!");
    });
}


function nbSentencesSliderUpdated() {
    const nb = document.getElementById("nbSentencesSlider").value;
    document.getElementById("nbSentencesSpan").innerText = nb;
}


function updateParameters() {
    const nbSentences = document.getElementById("nbSentencesSlider").value;
    const selectedVocab = document.getElementById("selectedVoc").value;
    const selectedLLM = document.getElementById("selectedLLM").value;

    document.getElementById("nbSentencesBtn").innerText = nbSentences;
    document.getElementById("infoNbSentences").innerText = nbSentences;
    document.getElementById("infoVocab").innerText = selectedVocab;
    document.getElementById("infoLLM").innerText = selectedLLM;

    const bodyData = {
        "nb_sentences": nbSentences,
        "selected_llm": selectedLLM,
        "selected_vocab": selectedVocab 
    };
    console.log(bodyData);

    fetch("http://127.0.0.1:5000/updateparameters", {
        method: 'POST',
        body: JSON.stringify(bodyData),
        headers: {
            "Content-Type": "application/json",
        }
    }).then((response) => {
        const responseData = response.json();
        responseData.then((r) => {
            if (r.status === "nok") {
                let errorMsg = "Error(s) during the updating of the parameters: ";
                r.errors.forEach(e => {
                    errorMsg += e + "; ";
                }).then(() => {
                    alert(errorMsg);
                });
            }
        });
    });
}


// EXERCICES TAB

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


// RESULTS TAB

function checkAnswers() {
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
                    } else {
                        diffs += `<span style="background-color: red; border: 2px solid black;">
                        ${d[1]}${d[0]}
                        </span>`;
                    }
                });
                resultList.innerHTML += `<div id="result-sentence-${index}">
                    <h2>Sentence ${index + 1}</h2>
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


// GENERAL

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
    document.getElementById(tabName + "-btn").className += " active";

    scroll(0, 0);
} 
