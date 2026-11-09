/* Listen button that plays in place (Article Standard, L1 in scripts/check_standard.py).

   Markup, placed under the H1/byline, before the first H2:
     <p class="listen-row"><button type="button" class="btn-primary listen-btn"
        data-yt="VIDEOID" data-title="Song - Artist">&#9654; Listen to Song</button></p>
     <script src="/js/listen-button.js" defer></script>

   On click the button is replaced, in the same spot, by one visible 16:9
   YouTube player (at least 200x200, nothing on top, standard controls) that
   starts playing. Nothing loads before the click (youtube-compliance skill).
   Official or label uploads only: the ID must be in data/official-videos.json.

   Playlist pages: add data-playlist="#tableId" (a table[data-inline-player]).
   The click then starts that list's continuous player (/js/table-player.js)
   from its first playable song and scrolls the player into view, so the
   button plays the whole list. data-yt stays as the fallback if the table
   or its Play buttons are missing. */
(function () {
  var buttons = document.querySelectorAll('.listen-btn[data-yt]');
  Array.prototype.forEach.call(buttons, function (btn) {
    btn.addEventListener('click', function () {
      var sel = btn.getAttribute('data-playlist');
      var table = sel ? document.querySelector(sel) : null;
      if (table) {
        var plays = Array.prototype.filter.call(
          table.querySelectorAll('button.ohw-play[data-yt], button.n1-play[data-yt]'),
          function (b) { var tr = b.closest('tr'); return !tr || tr.offsetParent !== null; });
        if (plays.length) {
          plays[0].click();
          var row = table.querySelector('tr.ohw-player-row, tr.n1-player-row') || plays[0].closest('tr');
          if (row && row.scrollIntoView) row.scrollIntoView({ behavior: 'smooth', block: 'center' });
          return;
        }
      }
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
