/* 70s Music Quiz — scored multiple-choice component.
   Plays all 50 questions from QUIZ_POOL (js/quiz-questions.js), shuffled
   fresh each round, one point per correct answer, running score shown
   throughout. Distinct from js/trivia-card.js (click-to-reveal, no score). */
(function () {
  const startScreen = document.getElementById('fqStartScreen');
  const playScreen = document.getElementById('fqPlayScreen');
  const resultScreen = document.getElementById('fqResultScreen');
  const startBtn = document.getElementById('fqStartBtn');
  const optionsGrid = document.getElementById('fqOptionsGrid');
  const feedback = document.getElementById('fqFeedback');
  const nextBtn = document.getElementById('fqNextBtn');
  const playAgainBtn = document.getElementById('fqPlayAgainBtn');
  const progressLabel = document.getElementById('fqProgressLabel');
  const progressBar = document.getElementById('fqProgressBar');
  const questionText = document.getElementById('fqQuestionText');
  const scoreHeadline = document.getElementById('fqScoreHeadline');
  const scoreText = document.getElementById('fqScoreText');
  const scoreMessage = document.getElementById('fqScoreMessage');

  if (!startBtn || typeof QUIZ_POOL === 'undefined') return;

  let questions = [];
  let qIndex = 0;
  let score = 0;
  let answered = false;

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function startRound() {
    const pool = shuffle(QUIZ_POOL.slice());
    questions = pool.map((item) => {
      const opts = item.options.map((text, i) => ({ text, correct: i === item.answer }));
      shuffle(opts);
      return { q: item.q, opts, explain: item.explain };
    });
    qIndex = 0;
    score = 0;
    startScreen.classList.add('hidden');
    resultScreen.classList.add('hidden');
    playScreen.classList.remove('hidden');
    renderQuestion();
  }

  function renderQuestion() {
    answered = false;
    const item = questions[qIndex];
    progressLabel.textContent = `Question ${qIndex + 1} of ${questions.length} — Score: ${score}`;
    progressBar.style.width = `${(qIndex / questions.length) * 100}%`;
    questionText.textContent = item.q;
    feedback.className = 'feedback hidden';
    feedback.textContent = '';
    nextBtn.classList.add('hidden');
    optionsGrid.innerHTML = '';
    item.opts.forEach((opt) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.type = 'button';
      btn.textContent = opt.text;
      btn.addEventListener('click', () => choose(btn, opt));
      optionsGrid.appendChild(btn);
    });
  }

  function choose(btn, opt) {
    if (answered) return;
    answered = true;
    const item = questions[qIndex];
    const buttons = optionsGrid.querySelectorAll('.option-btn');
    buttons.forEach((b) => {
      b.disabled = true;
      const match = item.opts.find((o) => o.text === b.textContent);
      if (match && match.correct) b.classList.add('correct');
    });
    if (opt.correct) {
      score += 1;
      feedback.className = 'feedback ok';
      feedback.textContent = '✓ Correct! ' + item.explain;
    } else {
      btn.classList.add('wrong');
      feedback.className = 'feedback no';
      feedback.textContent = '✗ Not quite. ' + item.explain;
    }
    progressLabel.textContent = `Question ${qIndex + 1} of ${questions.length} — Score: ${score}`;
    nextBtn.classList.remove('hidden');
    nextBtn.textContent = (qIndex + 1 < questions.length) ? 'Next Question' : 'See My Final Score';
  }

  function showResults() {
    playScreen.classList.add('hidden');
    resultScreen.classList.remove('hidden');
    progressBar.style.width = '100%';
    scoreHeadline.textContent = `${score} / ${questions.length}`;
    const pct = score / questions.length;
    let message;
    if (pct === 1) message = 'Perfect score. You ARE the 70s.';
    else if (pct >= 0.8) message = 'Almost perfect. The decade would be proud.';
    else if (pct >= 0.6) message = 'Solid. You clearly had the albums.';
    else if (pct >= 0.4) message = 'You caught a few of these on the radio at least.';
    else message = 'Time for a replay. The decade has more to teach you.';
    scoreText.textContent = `You scored ${score} out of ${questions.length}.`;
    scoreMessage.textContent = message;
  }

  startBtn.addEventListener('click', startRound);
  playAgainBtn.addEventListener('click', startRound);
  nextBtn.addEventListener('click', () => {
    qIndex += 1;
    if (qIndex < questions.length) renderQuestion();
    else showResults();
  });
})();
