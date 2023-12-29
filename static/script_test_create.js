let question_number = 1;
var option_number_dict = {};
let form = document.getElementById("questions");
// let questions = [];

function add_question() {
    var question = document.createElement("div");
    question.id = `question-${question_number}`;
    question.classList = ["question"];
    question.innerHTML = `
    <span class="container question-container">
        <textarea type="text" class="form-control question-input" name="question-${question_number}" id="Question-${question_number}-input" placeholder="Question-${question_number}" required></textarea>
        <span class="marks-del">
            <span class="marks-container">
                <input type="number" class="form-control marks" name="question-${question_number}/marks-correct" id="question-${question_number}/marks-correct" placeholder="correct" title="Marks on correct">
                <input type="number" class="form-control marks" name="question-${question_number}/marks-incorrect" id="question-${question_number}/marks-incorrect" placeholder="incorrect" title="marks on incorrect">
            </span>
            <button type="button" class="btn btn-primary m-1" onclick="del_que(${question_number})">Del
                question</button>
        </span>
    </span>
    <br>
    <div id="question-${question_number}-options">
        <span class="mb-3 option" id="question-${question_number}/option-1">
            <input type="text" class="form-control" name="question-${question_number}/option-1" placeholder="option-1" required>
            <span>
                <input type="checkbox" class="form-check-input-lg" name="question-${question_number}/option-1-correct">
                <button type="button" class="btn btn-primary m-1" onclick="del_option(${question_number},1)">Del
                    option</button>
            </span>
        </span>
        <span class="mb-3 option" id="question-${question_number}/option-2">
            <input type="text" class="form-control" name="question-${question_number}/option-2" placeholder="option-2" required>
            <span>
                <input type="checkbox" class="form-check-input-lg" name="question-${question_number}/option-2-correct">
                <button type="button" class="btn btn-primary m-1" onclick="del_option(${question_number},2)">Del
                    option</button>
            </span>
        </span>
    </div>
    <button onclick="add_option(${question_number})" type="button" class="btn btn-primary m-1">Add Option</button>
    `;
    option_number_dict[question_number] = 2;
    form.appendChild(question);
    question_number++;
}

function add_option(que_no) {
    Id = `question-${que_no}-options`
    ele = document.getElementById(Id);
    option_number_dict[que_no]++;
    option_number = option_number_dict[que_no];
    option = document.createElement("span");
    option.classList = ["option mb-3"];
    option.id = `question-${que_no}/option-${option_number}`;
    option.innerHTML = `
    <input type="text" class="form-control" name="question-${que_no}/option-${option_number}" placeholder="option-${option_number}" required>
    <span>
        <input type="checkbox" class="form-check-input-lg" name="question-${que_no}/option-${option_number}-correct">
        <button type="button" class="btn btn-primary m-1" onclick="del_option(${que_no},${option_number})">Del
            option</button>
    </span>
    `
    ele.appendChild(option);
}

function del_que(que_num) {
    no_ques = document.getElementById("questions").childElementCount;
    if(no_ques == 1){
        alert("Minimum 1 Question required");
        return;
    }
    document.getElementById(`question-${que_num}`).remove();
    if (que_num == (question_number - 1)) {
        question_number--;
    } else {
        for (let i = que_num + 1; i < question_number; i++) {
            ques = document.getElementById(`question-${i}`);
            regex = new RegExp(`question-${i}`, "g");
            ques.innerHTML = ques.innerHTML.replace(regex, `question-${i-1}`);
            document.getElementById(`Question-${i}-input`).placeholder = `Question-${i-1 }`;
        }
    }
}

function del_option(question_num, option_num) {
    // console.log(option_num+1);
    option = document.getElementById(`question-${question_num}/option-${option_num}`);
    options_no = document.getElementById(`question-${question_num}-options`).childElementCount;
    if (options_no <= 2) {
        alert("Minimum 2 Options required")
        return;
    }
    option.remove();
    for (let j = option_num + 1; j < options_no + 1; j++) {
        regex = new RegExp(`option-${j}`, "g");
        option_j = document.getElementById(`question-${question_num}/option-${j}`);
        option_j.innerHTML = option_j.innerHTML.replace(regex, `option-${j-1}`);
        option_j.id = `question-${question_num}/option-${j-1}`;
        option_j.innerHTML = option_j.innerHTML.replace(`del_option(${question_num},${j})`, `del_option(${question_num},${j-1})`);
    }
    option_number_dict[question_num]--;
}

async function create_test() {
    topic = document.getElementById("topic");
    if (topic.value == '') {
        topic.focus();
        topic.classList.add("incomplete");
        await new Promise(r => setTimeout(r, 0.5));
        alert("Enter Topic");
        return;
    }
    subject = document.getElementById("subject");
    if (subject.value == '') {
        subject.classList.add("incomplete");
        subject.focus();
        await new Promise(r => setTimeout(r, 0.5));
        alert("Select subject");
        return;
    }
    ques = document.getElementById("questions").children;
    for (let que_index = 0; que_index < ques.length; que_index++) {
        que = ques[que_index];
        inputs = que.getElementsByTagName("input");
        bg = que.style.backgroundColor;
        // console.log(inputs);
        let correct_selected = false;
        for (let input_index = 0; input_index < inputs.length; input_index++) {
            input = inputs[input_index];
            if (input.type == "text" ) {
                if (input.value == '') {
                    input.classList.add("incomplete");
                    input.focus();
                    await new Promise(r => setTimeout(r, 0.5));
                    alert("Enter value ")
                    return;
                }
            } else if(input.type == "number"){
                if (input.value == '') {
                    input.classList.add("incomplete");
                    input.focus();
                    await new Promise(r => setTimeout(r, 0.5));
                    alert("Enter value")
                    return;
                }
                if (input.value == '0') {
                    input.classList.add("incomplete");
                    input.focus();
                    await new Promise(r => setTimeout(r, 0.5));
                    alert("Value cannot be Zero")
                    return;
                }
            }
            else if(input.type == "checkbox"){
                // input.style.color = "rgba(256,36,36,0.5)";
                if(input.checked){
                    correct_selected = true;
                }
            }
        }
        if(!correct_selected){
            que.classList.add("incomplete");
            alert("Select correct option")
            return;
        }
    }
    document.getElementById("create_test").submit();
}
add_question()
function autoFill() {
    var form = document.getElementById("create_test");
    var inputFields = form.getElementsByTagName("input");
    var selectFields = form.getElementsByTagName("select");
    var textareaFields = form.getElementsByTagName("textarea");

    for (var i = 0; i < inputFields.length; i++) {
      inputFields[i].value = "1";
    }

    for (var i = 0; i < selectFields.length; i++) {
      selectFields[i].selectedIndex = 1;
    }

    for (var i = 0; i < textareaFields.length; i++) {
      textareaFields[i].value = "1";
    }
  }