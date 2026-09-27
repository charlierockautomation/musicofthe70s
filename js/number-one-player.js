/* In-page player for the 70s Number One Hits table.
   A Play button (button.n1-play[data-yt]) opens a YouTube player in a new
   row directly under the song and starts it. YouTube rules, same as
   /radio/ (see the youtube-compliance skill):
   - playback starts only from this click; nothing loads before it
   - one player at a time, full size (16:9, at least 200x200), nothing on top
     (.video-embed also makes the back-to-top button step aside)
   - a video marked not embeddable or made for kids in
     data/youtube-status.json is never played */
(function () {
  var table = document.getElementById('numberOnesTable');
  if (!table) return;
  var statusPromise = null;

  function loadStatus() {
    if (!statusPromise) {
      statusPromise = fetch('/data/youtube-status.json')
        .then(function (r) { return r.ok ? r.json() : {}; })
        .then(function (d) { return d.videos || {}; })
        .catch(function () { return {}; });
    }
    return statusPromise;
  }

  function closePlayer() {
    var open = table.querySelector('tr.n1-player-row');
    if (open) open.parentNode.removeChild(open);
    Array.prototype.forEach.call(table.querySelectorAll('.n1-play[aria-expanded="true"]'), function (b) {
      b.setAttribute('aria-expanded', 'false');
    });
  }

  // On phones the table scrolls sideways inside its wrapper. Keep the
  // player pinned to the wrapper's visible width so no part of it is ever
  // clipped off-screen (YouTube: a player must be fully visible).
  var wrap = table.closest('.data-table-wrap');
  function fitPlayer() {
    var inner = table.querySelector('.n1-player-inner');
    if (inner && wrap) inner.style.width = Math.max(200, wrap.clientWidth - 32) + 'px';
  }
  window.addEventListener('resize', fitPlayer);

  function openPlayer(btn, ok) {
    closePlayer();
    var row = btn.closest('tr');
    var song = row.querySelector('.n1-song').textContent.trim();
    var artist = row.querySelector('.n1-artist').textContent.trim();
    var tr = document.createElement('tr');
    tr.className = 'n1-player-row detail-row';
    var td = document.createElement('td');
    td.colSpan = row.cells.length;
    var inner = document.createElement('div');
    inner.className = 'n1-player-inner';
    td.appendChild(inner);
    if (ok) {
      var box = document.createElement('div');
      box.className = 'video-embed n1-player';
      var frame = document.createElement('iframe');
      // autoplay only because this player is created by the listener's own click
      frame.src = 'https://www.youtube.com/embed/' + encodeURIComponent(btn.getAttribute('data-yt')) + '?autoplay=1';
      frame.title = song + ' by ' + artist;
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      frame.allowFullscreen = true;
      box.appendChild(frame);
      inner.appendChild(box);
    } else {
      var msg = document.createElement('p');
      msg.className = 'n1-unavailable';
      msg.textContent = 'This video is unavailable to play here.';
      inner.appendChild(msg);
    }
    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'n1-close';
    close.textContent = 'Close player';
    close.addEventListener('click', function () { closePlayer(); btn.focus(); });
    inner.appendChild(close);
    tr.appendChild(td);
    row.parentNode.insertBefore(tr, row.nextSibling);
    if (wrap) wrap.scrollLeft = 0;
    fitPlayer();
    btn.setAttribute('aria-expanded', 'true');
    tr.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  table.addEventListener('click', function (e) {
    var btn = e.target.closest('.n1-play');
    if (!btn) return;
    if (btn.getAttribute('aria-expanded') === 'true') { closePlayer(); return; }
    loadStatus().then(function (videos) {
      var st = videos[btn.getAttribute('data-yt')];
      openPlayer(btn, !(st && (st.embeddable === false || st.madeForKids === true)));
    });
  });

  // Sorting moves rows around, so close the player first.
  Array.prototype.forEach.call(table.querySelectorAll('thead button'), function (b) {
    b.addEventListener('click', closePlayer);
  });
})();
