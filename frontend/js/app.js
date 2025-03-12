let selectedProblemId = null;
let allProblems = [];  // 전체 문제 저장
let questionHistory = []; // 질문 히스토리 저장

document.addEventListener("DOMContentLoaded", function () {
    fetchProblems();
});

function startGame() {
    // intro-section 숨기기
    document.getElementById("intro-section").style.display = "none";

    // 문제필터 보여주기
    document.getElementById("filter-section").style.display = "block";

    // 문제리스트 보여주기
    const problemSection = document.getElementById("problem-list");
    problemSection.style.display = "block";

    // 부드럽게 스크롤 이동 (선택사항)
    problemSection.scrollIntoView({ behavior: 'smooth' });
}

function fetchProblems() {
    document.getElementById("loading-msg").style.display = "block";

    fetch("http://172.16.200.83:8000/problems")
        .then(response => response.json())
        .then(data => {
            allProblems = data.problems;
            document.getElementById("loading-msg").style.display = "none";  // ✅ 여기!
            filterProblems();
        })
        .catch(err => {
            document.getElementById("loading-msg").textContent = "❌ 문제 리스트 로딩 실패";
            console.error("문제 리스트 로딩 실패", err);
        });
}

function filterProblems() {
    const selectedCategory = document.getElementById("category-select").value;
    const selectedDifficulty = document.getElementById("difficulty-select").value;
    const list = document.getElementById("problems");
    list.innerHTML = '';

    const filtered = allProblems.filter(problem => {
        const matchCategory = selectedCategory ? problem.category === selectedCategory : true;
        const matchDifficulty = selectedDifficulty ? problem.difficulty === selectedDifficulty : true;
        return matchCategory && matchDifficulty;
    });

    filtered.forEach(problem => {
        const li = document.createElement("li");
        li.textContent = `[${problem.difficulty}] ${problem.title} (${problem.category})`;
        li.style.cursor = "pointer";
        li.onclick = () => selectProblem(problem.id, problem.title);
        list.appendChild(li);
    });
}

function selectProblem(id, title) {
    selectedProblemId = id;
    questionHistory = [];  // ✅ 질문 히스토리 초기화!

    fetch(`http://172.16.200.83:8000/problems/${id}`)
        .then(response => response.json())
        .then(problem => {
            document.getElementById("modal-problem-title").textContent = problem.title;
            document.getElementById("modal-problem-description").textContent = problem.description;
            document.getElementById("modal-response").textContent = "";
            document.getElementById("modal-user-question").value = "";
            document.getElementById("modal-history").innerHTML = ""; // DOM 초기화도 함께

            document.getElementById("problem-modal").style.display = "flex";
        });
}


function closeModal() {
    document.getElementById("problem-modal").style.display = "none";
}

function giveUp() {
    fetch(`http://172.16.200.83:8000/problems/${selectedProblemId}`)
        .then(response => response.json())
        .then(problem => {
            const result = `${problem.answer}`;
            document.getElementById("modal-response").textContent = result;
        });
}

function submitFinalAnswer() {
    const userFinalAnswer = document.getElementById("modal-final-answer").value;
    if (!userFinalAnswer || !selectedProblemId) return;

    fetch("http://172.16.200.83:8000/submit_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            problem_id: selectedProblemId,
            user_id: "demo_user",
            final_answer: userFinalAnswer
        })
    })
    .then(response => response.json())
    .then(data => {
        let msg = data.message;
        if (data.is_correct) {
            msg += `\n\n정답: ${data.correct_answer}`;
        }
        document.getElementById("modal-response").textContent = msg;
    });
}


function submitModalQuestion() {
    const question = document.getElementById("modal-user-question").value;
    if (!question || !selectedProblemId) return;

    fetch("http://172.16.200.83:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            problem_id: selectedProblemId,
            user_id: "demo_user",
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        const aiResponse = data.response;
        document.getElementById("modal-response").textContent = `🐢: ${aiResponse}`;

        // 히스토리 저장
        questionHistory.push({ question, aiResponse });
        renderHistory();
    });
}

function renderHistory() {
    const container = document.getElementById("modal-history");
    container.innerHTML = "<h4>질문 히스토리</h4>";
    questionHistory.forEach((item, i) => {
        const p = document.createElement("p");
        p.textContent = `${i+1}. Q: ${item.question} → A: ${item.aiResponse}`;
        container.appendChild(p);
    });
}

function showHint() {
    const question = document.getElementById("modal-user-question").value;
    if (!question || !selectedProblemId) {
        alert("먼저 질문을 입력해주세요.");
        return;
    }

    fetch("http://172.16.200.83:8000/hint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            problem_id: selectedProblemId,
            user_id: "demo_user",
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        const hintText = data.hint || "힌트를 가져올 수 없습니다.";
        const hintElem = document.createElement("p");
        hintElem.textContent = "💡 힌트: " + hintText;
        document.getElementById("modal-history").appendChild(hintElem); // 힌트도 히스토리에 붙이기
    })
    .catch(err => {
        console.error("힌트 요청 실패", err);
        alert("힌트 가져오기 중 오류 발생");
    });
}

function goHome() {
    document.getElementById("intro-section").style.display = "block";
    document.getElementById("filter-section").style.display = "none";
    document.getElementById("problem-list").style.display = "none";
    document.getElementById("problem-modal").style.display = "none";
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
