const form = document.querySelector("#plan-form");
const subjectInput = document.querySelector("#subject");
const minutesInput = document.querySelector("#minutes");
const minuteLabel = document.querySelector("#minute-label");
const result = document.querySelector("#result");
const resultTitle = document.querySelector("#result-title");
const status = document.querySelector("#status");
const quizButton = document.querySelector("#quiz-button");

minutesInput.addEventListener("input", () => minuteLabel.textContent = minutesInput.value);

function showError(message) {
  status.textContent = message;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  status.textContent = "";
  const button = form.querySelector("button[type=submit]");
  button.disabled = true;
  button.textContent = "Creating your plan…";
  try {
    const response = await fetch("/api/plan", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({subject: subjectInput.value, minutes: Number(minutesInput.value), level: document.querySelector("#level").value})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not create plan.");
    resultTitle.textContent = `${data.subject} study plan`;
    result.className = "";
    result.innerHTML = `<p class="muted">A ${data.minutes_per_day}-minute session · ${escapeHtml(data.level)} level</p>
      <div class="steps">${data.steps.map((step, i) => `<article class="step"><div class="step-number">${i+1}</div><div><h3>${escapeHtml(step.title)}</h3><p>${escapeHtml(step.detail)}</p></div><span class="duration">${step.minutes} min</span></article>`).join("")}</div>
      <div class="tip"><strong>✦ Gentle reminder</strong><br>${escapeHtml(data.tip)}</div>`;
  } catch (error) { showError(error.message); }
  finally { button.disabled = false; button.innerHTML = 'Create my study plan <span>→</span>'; }
});

quizButton.addEventListener("click", async () => {
  status.textContent = "";
  const subject = subjectInput.value.trim();
  if (!subject) { showError("Enter a subject first, then generate practice questions."); subjectInput.focus(); return; }
  quizButton.disabled = true;
  quizButton.textContent = "Preparing questions…";
  try {
    const response = await fetch("/api/quiz", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({subject, count: 3})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not generate questions.");
    resultTitle.textContent = `${data.subject} practice`;
    result.className = "";
    result.innerHTML = `<p class="muted">Try answering without looking at your notes.</p><ol class="questions">${data.questions.map(q => `<li>${escapeHtml(q)}</li>`).join("")}</ol><div class="tip">✦ Say your answers out loud, then check them against your notes.</div>`;
  } catch (error) { showError(error.message); }
  finally { quizButton.disabled = false; quizButton.textContent = "Generate practice questions"; }
});

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}
