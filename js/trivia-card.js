/* ============================================================
   Trivia Card Component — reveal/explain interaction
   Reusable across all trivia posts.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.trivia-reveal-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const card = btn.closest('.trivia-card');
      card.querySelector('.trivia-answer').hidden = false;
      card.querySelector('.trivia-explain-btn').hidden = false;
      btn.hidden = true;
    });
  });

  document.querySelectorAll('.trivia-explain-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const card = btn.closest('.trivia-card');
      card.querySelector('.trivia-explanation').hidden = false;
      btn.hidden = true;
    });
  });
});
