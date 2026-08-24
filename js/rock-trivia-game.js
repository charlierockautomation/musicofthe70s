/* Rock Trivia Game — engine. Depends on shuffle/lsGet/lsSet/shareOrCopy from
   main.js and ROCK_TRIVIA_POOL/ROCK_TRIVIA_GENRE_LABELS from rock-trivia-data.js. */
(function () {
  const startScreen = document.getElementById('startScreen');
  const quizScreen = document.getElementById('quizScreen');
  const resultScreen = document.getElementById('resultScreen');
  const optionsGrid = document.getElementById('optionsGrid');
  const feedback = document.getElementById('feedback');
  const nextBtn = document.getElementById('nextBtn');
  const shareBtn = document.getElementById('shareBtn');
  const dailyBtn = document.getElementById('dailyBtn');
  const streakText = document.getElementById('streakText');
  const bestScoreText = document.getElementById('bestScoreText');
  const categoryGrid = document.getElementById('categoryGrid');
  const quizCategoryGrid = document.getElementById('quizCategoryGrid');
  const startBtn = document.getElementById('startBtn');
  const resultStreakText = document.getElementById('resultStreakText');

  const ROUND_SIZE = 10;
  const BEST_KEY = 'rockTriviaBest';
  const STREAK_KEY = 'rockTriviaStreak';

  let questions = [];
  let qIndex = 0;
  let score = 0;
  let answered = false;
  let selectedCategory = 'all';
  let mode = 'category'; // 'category' | 'daily'

  /* ---- date / seeded-random helpers (Daily Challenge) ---- */
  function todayStr() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }
  function daysBetween(a, b) {
    return Math.round((new Date(b + 'T00:00:00') - new Date(a + 'T00:00:00')) / 86400000);
  }
  function dateSeed(str) {
    let h = 0;
    for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) | 0;
    return h >>> 0;
  }
  function mulberry32(seed) {
    let a = seed;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function seededShuffle(array, seed) {
    const rand = mulberry32(seed);
    const arr = array.slice();
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(rand() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function getStreak() {
    try {
      return JSON.parse(lsGet(STREAK_KEY, '{"count":0,"lastDate":""}'));
    } catch (e) {
      return { count: 0, lastDate: '' };
    }
  }
  function displayStreakCount(streak, today) {
    if (!streak.lastDate) return 0;
    if (streak.lastDate === today) return streak.count;
    if (daysBetween(streak.lastDate, today) === 1) return streak.count; // alive, at risk today
    return 0; // broken
  }
  function dailyCompletedToday(streak, today) {
    return streak.lastDate === today;
  }
  function recordDailyCompletion() {
    const today = todayStr();
    const streak = getStreak();
    if (streak.lastDate === today) return streak; // already recorded
    if (streak.lastDate && daysBetween(streak.lastDate, today) === 1) {
      streak.count += 1;
    } else {
      streak.count = 1;
    }
    streak.lastDate = today;
    lsSet(STREAK_KEY, JSON.stringify(streak));
    return streak;
  }

  function refreshStartScreen() {
    const today = todayStr();
    const streak = getStreak();
    const shown = displayStreakCount(streak, today);
    const done = dailyCompletedToday(streak, today);

    if (done) {
      streakText.textContent = shown > 0
        ? `Completed for today. 🔥 ${shown}-day streak — come back tomorrow for a new challenge.`
        : 'Completed for today. Come back tomorrow for a new challenge.';
      dailyBtn.textContent = '✓ Completed Today';
      dailyBtn.disabled = true;
    } else {
      streakText.textContent = shown > 0
        ? `🔥 ${shown}-day streak. Play today's round to keep it alive.`
        : 'Play today’s 10-question round. Come back daily to build a streak.';
      dailyBtn.textContent = 'Play Today’s Challenge';
      dailyBtn.disabled = false;
    }

    const best = parseInt(lsGet(BEST_KEY, '0'), 10) || 0;
    bestScoreText.textContent = best > 0 ? `Personal best: ${best}/10` : '';
  }

  function poolForCategory(cat) {
    return cat === 'all' ? ROCK_TRIVIA_POOL : ROCK_TRIVIA_POOL.filter((q) => q.genre === cat);
  }

  function toRenderable(item) {
    const opts = item.options.map((text, i) => ({ text, correct: i === item.answer }));
    shuffle(opts);
    return { q: item.q, opts, explain: item.explain };
  }

  function startRound(chosenMode) {
    mode = chosenMode;
    let source;
    if (mode === 'daily') {
      source = seededShuffle(ROCK_TRIVIA_POOL, dateSeed(todayStr()));
    } else {
      source = shuffle(poolForCategory(selectedCategory).slice());
    }
    questions = source.slice(0, ROUND_SIZE).map(toRenderable);
    qIndex = 0; score = 0;
    startScreen.classList.add('hidden');
    resultScreen.classList.add('hidden');
    quizScreen.classList.remove('hidden');
    renderQuestion();
  }

  function renderQuestion() {
    answered = false;
    const item = questions[qIndex];
    document.getElementById('progressLabel').textContent = `Question ${qIndex + 1} of ${questions.length}`;
    document.getElementById('progressBar').style.width = `${(qIndex / questions.length) * 100}%`;
    document.getElementById('questionText').textContent = item.q;
    feedback.className = 'feedback hidden';
    nextBtn.classList.add('hidden');
    optionsGrid.innerHTML = '';
    item.opts.forEach((opt) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.textContent = opt.text;
      btn.addEventListener('click', () => choose(btn, opt));
      optionsGrid.appendChild(btn);
    });
  }

  function choose(btn, opt) {
    if (answered) return;
    answered = true;
    const buttons = optionsGrid.querySelectorAll('.option-btn');
    buttons.forEach((b) => {
      b.disabled = true;
      const isCorrect = questions[qIndex].opts.find((o) => o.text === b.textContent).correct;
      if (isCorrect) b.classList.add('correct');
    });
    if (opt.correct) {
      score += 1;
      feedback.className = 'feedback ok';
      feedback.textContent = '✓ Correct! ' + questions[qIndex].explain;
    } else {
      btn.classList.add('wrong');
      feedback.className = 'feedback no';
      feedback.textContent = '✗ Not quite. ' + questions[qIndex].explain;
    }
    nextBtn.classList.remove('hidden');
    nextBtn.textContent = (qIndex + 1 < questions.length) ? 'Next Question' : 'See My Score';
  }

  nextBtn.addEventListener('click', () => {
    qIndex += 1;
    if (qIndex < questions.length) renderQuestion();
    else showResults();
  });

  const MESSAGES = {
    0: 'Time to dig through the record crates.', 1: 'Time to dig through the record crates.',
    2: 'Time to dig through the record crates.', 3: 'A few of those rang a bell.',
    4: 'A few of those rang a bell.', 5: 'Solid casual-fan showing.',
    6: 'Solid casual-fan showing.', 7: 'You know your rock.',
    8: 'You know your rock.', 9: 'Almost perfect. Serious collection energy.',
    10: 'Perfect score. You were there.'
  };

  function showResults() {
    quizScreen.classList.add('hidden');
    resultScreen.classList.remove('hidden');
    document.getElementById('scoreHeadline').textContent = `${score} / ${questions.length}`;
    document.getElementById('scoreText').textContent = `You scored ${score} out of ${questions.length}.`;
    document.getElementById('scoreMessage').textContent = MESSAGES[score] || '';

    const best = parseInt(lsGet(BEST_KEY, '0'), 10) || 0;
    if (score > best) lsSet(BEST_KEY, String(score));

    if (mode === 'daily') {
      const streak = recordDailyCompletion();
      resultStreakText.textContent = `🔥 ${streak.count}-day streak`;
      resultStreakText.classList.remove('hidden');
    } else {
      resultStreakText.classList.add('hidden');
    }
  }

  shareBtn.addEventListener('click', async () => {
    const label = mode === 'daily'
      ? `today's Rock Trivia Game Daily Challenge`
      : `the Rock Trivia Game (${ROCK_TRIVIA_GENRE_LABELS[selectedCategory] || 'All Rock'})`;
    const text = `I scored ${score}/${questions.length} on ${label}! Can you beat me? musicofthe70s.net/pages/rock-trivia-game.html`;
    const status = await shareOrCopy(
      { title: 'Rock Trivia Game', text, url: 'https://musicofthe70s.net/pages/rock-trivia-game.html' },
      text
    );
    if (status === 'copied') shareBtn.textContent = '✓ Copied!';
    else if (status === 'shared') shareBtn.textContent = '✓ Shared';
    else if (status === 'failed') shareBtn.textContent = 'Copy failed';
    setTimeout(() => { shareBtn.textContent = '↗ Share my score'; }, 1800);
  });

  function syncCategoryButtons() {
    [categoryGrid, quizCategoryGrid].forEach((grid) => {
      grid.querySelectorAll('.option-btn').forEach((b) => {
        b.classList.toggle('selected', b.getAttribute('data-value') === selectedCategory);
      });
    });
  }

  function selectCategory(value) {
    selectedCategory = value;
    syncCategoryButtons();
  }

  categoryGrid.querySelectorAll('.option-btn').forEach((btn) => {
    btn.addEventListener('click', () => selectCategory(btn.getAttribute('data-value')));
  });

  quizCategoryGrid.querySelectorAll('.option-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      selectCategory(btn.getAttribute('data-value'));
      startRound('category');
    });
  });

  syncCategoryButtons();

  startBtn.addEventListener('click', () => startRound('category'));
  dailyBtn.addEventListener('click', () => { if (!dailyBtn.disabled) startRound('daily'); });
  document.getElementById('playAgainBtn').addEventListener('click', () => {
    resultScreen.classList.add('hidden');
    startScreen.classList.remove('hidden');
    refreshStartScreen();
  });

  refreshStartScreen();
})();
