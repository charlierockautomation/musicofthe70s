/* Listen button that plays in place (Article Standard, L1 in scripts/check_standard.py).

   Markup, placed under the H1/byline, before the first H2:
     <p class="listen-row"><button type="button" class="btn-primary listen-btn"
        data-yt="VIDEOID" data-title="Song - Artist">&#9654; Listen to Song</button></p>
     <script src="/js/listen-button.js" defer></script>

   On click the button is replaced, in the same spot, by one visible 16:9
   YouTube player (at least 200x200, nothing on top, standard controls) that
   starts playing. Nothing loads before the click (youtube-compliance skill).
   Official or label uploads only: the ID must be in data/official-videos.json. */
(function () {
  var buttons = document.querySelectorAll('.listen-btn[data-yt]');
  Array.prototype.forEach.call(buttons, function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-yt');
      if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
      var box = document.createElement('div');
      box.className = 'video-embed listen-player';
      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube.com/embed/' + id + '?autoplay=1&rel=0';
      frame.title = btn.getAttribute('data-title') || 'YouTube video player';
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      frame.allowFullscreen = true;
      box.appendChild(frame);
      var row = btn.closest('.listen-row') || btn;
      row.parentNode.replaceChild(box, row);
    });
  });
})();
