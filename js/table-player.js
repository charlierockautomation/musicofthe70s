/* Continuous in-page player for every playable song list on the site.

   Works on any table marked <table data-inline-player> (and the older
   #oneHitWondersTable / #numberOnesTable ids). Each row has a Play button:
   button.ohw-play[data-yt] (or .n1-play), optional data-title.

   Behavior:
   - Pressing Play opens one YouTube player in a new row under that song and
     starts it.
   - When a song ends, the next playable song in the list starts in the same
     player, and so on down the list. On pages with more than one list, it
     carries on into the next list, then starts again from the top. It keeps
     going until the listener presses Stop (or the playing song's button).
   - Songs that are hidden by a filter, marked not embeddable / made for kids
     in data/youtube-status.json, already played this pass, or that YouTube
     refuses to play are skipped.
   - Next button skips ahead by hand.

   YouTube rules (youtube-compliance skill), same pattern as /radio/:
   - playback starts only from the listener's click; nothing loads before it
   - one visible, full-size player (16:9, at least 200x200), nothing on top,
     standard controls kept
   - an automatic next song starts only while the tab is visible and more
     than half of the player is on screen. If the listener has scrolled away
     when a song ends, the next song waits and starts by itself as soon as
     the player is back on screen (or when Next is pressed). */
(function () {
  var TABLES = 'table[data-inline-player], table#oneHitWondersTable, table#numberOnesTable';
  var BTN = '.ohw-play, .n1-play';
  var tables = Array.prototype.slice.call(document.querySelectorAll(TABLES));
  if (!tables.length) return;

  /* ---------- status data ---------- */
  var statusPromise = null;
  var videos = {};
  function loadStatus() {
    if (!statusPromise) {
      statusPromise = fetch('/data/youtube-status.json')
        .then(function (r) { return r.ok ? r.json() : {}; })
        .then(function (d) { videos = d.videos || {}; return videos; })
        .catch(function () { return videos; });
    }
    return statusPromise;
  }
  function playable(btn) {
    var st = videos[btn.getAttribute('data-yt')];
    return !(st && (st.embeddable === false || st.madeForKids === true));
  }

  /* ---------- YouTube IFrame API (loaded on first Play click only) ---------- */
  var apiReady = false, apiRequested = false, apiWaiters = [];
  var prevReady = window.onYouTubeIframeAPIReady;
  window.onYouTubeIframeAPIReady = function () {
    apiReady = true;
    if (typeof prevReady === 'function') { try { prevReady(); } catch (e) {} }
    var w = apiWaiters; apiWaiters = [];
    w.forEach(function (fn) { fn(); });
  };
  function whenApi(fn) {
    if (apiReady && window.YT && window.YT.Player) { fn(); return; }
    apiWaiters.push(fn);
    if (!apiRequested) {
      apiRequested = true;
      var tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      document.head.appendChild(tag);
    }
  }

  /* ---------- helpers ---------- */
  function prefixOf(btn) { return btn.classList.contains('n1-play') ? 'n1' : 'ohw'; }
  function titleOf(btn) {
    var t = btn.getAttribute('data-title');
    if (t) return t;
    var row = btn.closest('tr');
    var p = prefixOf(btn);
    var song = row.querySelector('.' + p + '-song');
    var artist = row.querySelector('.' + p + '-artist');
    if (song && artist) return song.textContent.trim() + ' by ' + artist.textContent.trim();
    if (song) return song.textContent.trim();
    return 'YouTube video';
  }
  function rowVisible(btn) {
    var row = btn.closest('tr');
    return !!row && !row.hidden && row.offsetParent !== null;
  }
  function allButtons() {
    var list = [];
    tables.forEach(function (t) {
      Array.prototype.forEach.call(t.querySelectorAll(BTN), function (b) { list.push(b); });
    });
    return list;
  }

  /* ---------- state ---------- */
  var player = null;        // YT.Player, or null when using the plain-iframe fallback
  var playerRow = null;     // <tr> holding the player
  var playerBox = null;     // .video-embed box (for the on-screen check)
  var nowEl = null;         // caption above the player
  var current = null;       // Play button of the song now playing
  var played = {};          // ids played this pass
  var waiting = null;       // next button held back because the player is off screen
  var errorsInRow = 0;
  var observer = null;
  var readyTimer = null;

  function setCaption(text) { if (nowEl) nowEl.textContent = text; }

  function markCurrent(btn) {
    Array.prototype.forEach.call(document.querySelectorAll('tr.tp-playing'), function (r) { r.classList.remove('tp-playing'); });
    Array.prototype.forEach.call(document.querySelectorAll(BTN), function (b) {
      if (b.getAttribute('aria-expanded') === 'true') {
        b.setAttribute('aria-expanded', 'false');
        if (b.hasAttribute('data-tp-label')) { b.innerHTML = b.getAttribute('data-tp-label'); b.removeAttribute('data-tp-label'); }
      }
    });
    current = btn;
    if (!btn) return;
    btn.closest('tr').classList.add('tp-playing');
    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('data-tp-label', btn.innerHTML);
    btn.innerHTML = '&#9632; Stop';
  }

  function positionText(btn) {
    var list = allButtons().filter(function (b) { return rowVisible(b) && playable(b); });
    var i = list.indexOf(btn);
    return i >= 0 ? ' (' + (i + 1) + ' of ' + list.length + ')' : '';
  }

  /* Next song after `from`, in page order, wrapping to the top once. */
  function findNext(from) {
    var list = allButtons();
    var start = list.indexOf(from);
    var fromId = from ? from.getAttribute('data-yt') : null;
    function ok(b) {
      var id = b.getAttribute('data-yt');
      return id && id !== fromId && !played[id] && rowVisible(b) && playable(b);
    }
    for (var i = start + 1; i < list.length; i++) if (ok(list[i])) return list[i];
    // End of the page's lists: start a new pass from the top.
    played = {};
    for (var j = 0; j < list.length; j++) if (ok(list[j])) return list[j];
    return null;
  }

  /* More than half the player on screen, tab visible (YouTube autoplay rule). */
  function onScreen() {
    if (!playerBox || document.visibilityState !== 'visible') return false;
    var r = playerBox.getBoundingClientRect();
    var area = r.width * r.height;
    if (!area) return false;
    var w = Math.min(r.right, window.innerWidth) - Math.max(r.left, 0);
    var h = Math.min(r.bottom, window.innerHeight) - Math.max(r.top, 0);
    return w > 0 && h > 0 && (w * h) / area > 0.5;
  }

  function checkWaiting() {
    if (waiting && onScreen()) { var b = waiting; waiting = null; playBtn(b); }
  }

  function playBtn(btn) {
    markCurrent(btn);
    played[btn.getAttribute('data-yt')] = true;
    setCaption('Now playing: ' + titleOf(btn) + positionText(btn));
    if (player && player.loadVideoById) player.loadVideoById(btn.getAttribute('data-yt'));
  }

  /* auto = true when a song ended or failed; false for the Next button. */
  function advance(auto) {
    if (!playerRow) return;
    var next = findNext(current);
    if (!next) { setCaption('End of the list.'); markCurrent(null); return; }
    if (auto && !onScreen()) {
      waiting = next;
      setCaption('Up next: ' + titleOf(next) + '. It starts as soon as the player is back on screen, or press Next.');
      return;
    }
    waiting = null;
    playBtn(next);
  }

  function closePlayer() {
    if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
    if (observer) { observer.disconnect(); observer = null; }
    if (player && player.destroy) { try { player.destroy(); } catch (e) {} }
    player = null;
    if (playerRow && playerRow.parentNode) playerRow.parentNode.removeChild(playerRow);
    playerRow = playerBox = nowEl = null;
    waiting = null;
    errorsInRow = 0;
    markCurrent(null);
  }

  function fitPlayer() {
    if (!playerRow) return;
    var inner = playerRow.querySelector('.' + playerRow.getAttribute('data-tp-prefix') + '-player-inner');
    var wrap = playerRow.closest('.data-table-wrap');
    if (inner && wrap) inner.style.width = Math.max(200, wrap.clientWidth - 32) + 'px';
  }
  window.addEventListener('resize', function () { fitPlayer(); checkWaiting(); });
  document.addEventListener('visibilitychange', checkWaiting);
  window.addEventListener('scroll', checkWaiting, { passive: true });

  function plainIframe(host, id, title) {
    // Fallback when YouTube's API script can't load (e.g. blocked by an
    // extension): same plain player as before, one song, no auto-advance.
    var frame = document.createElement('iframe');
    frame.src = 'https://www.youtube.com/embed/' + encodeURIComponent(id) + '?autoplay=1';
    frame.title = title;
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.allowFullscreen = true;
    host.parentNode.replaceChild(frame, host);
  }

  function button(cls, text, onClick) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = cls;
    b.textContent = text;
    b.addEventListener('click', onClick);
    return b;
  }

  /* Open the player under btn's row (always from the listener's click). */
  function openAt(btn) {
    closePlayer();
    var p = prefixOf(btn);
    var row = btn.closest('tr');
    var tr = document.createElement('tr');
    tr.className = p + '-player-row detail-row';
    tr.setAttribute('data-tp-prefix', p);
    var td = document.createElement('td');
    td.colSpan = row.cells.length;
    var inner = document.createElement('div');
    inner.className = p + '-player-inner';
    td.appendChild(inner);

    nowEl = document.createElement('p');
    nowEl.className = 'tp-now';
    nowEl.setAttribute('aria-live', 'polite');
    inner.appendChild(nowEl);

    var ok = playable(btn);
    var host = null;
    if (ok) {
      playerBox = document.createElement('div');
      playerBox.className = 'video-embed ' + p + '-player';
      host = document.createElement('div');
      playerBox.appendChild(host);
      inner.appendChild(playerBox);
    } else {
      var msg = document.createElement('p');
      msg.className = p + '-unavailable';
      msg.textContent = 'This video is unavailable to play here.';
      inner.appendChild(msg);
    }

    var controls = document.createElement('div');
    controls.className = 'tp-controls';
    controls.appendChild(button(p + '-close tp-next', 'Next song ▶▶', function () {
      if (!ok) { var n = findNext(btn); if (n) openAt(n); return; }  // fresh player, from this click
      if (player) advance(false);
    }));
    controls.appendChild(button(p + '-close', 'Stop', function () { var b = current || btn; closePlayer(); b.focus(); }));
    inner.appendChild(controls);

    tr.appendChild(td);
    row.parentNode.insertBefore(tr, row.nextSibling);
    playerRow = tr;
    var wrap = table0(btn).closest('.data-table-wrap');
    if (wrap) wrap.scrollLeft = 0;
    fitPlayer();
    markCurrent(btn);
    played = {};
    played[btn.getAttribute('data-yt')] = true;
    setCaption((ok ? 'Now playing: ' : '') + titleOf(btn) + positionText(btn));
    tr.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    if (!ok) return;

    if ('IntersectionObserver' in window) {
      var steps = [];
      for (var i = 0; i <= 20; i++) steps.push(i / 20);
      observer = new IntersectionObserver(checkWaiting, { threshold: steps });
      observer.observe(playerBox);
    }

    var id = btn.getAttribute('data-yt');
    var title = titleOf(btn);
    var thisRow = tr;
    readyTimer = setTimeout(function () {
      readyTimer = null;
      if (playerRow === thisRow && !player && host.parentNode) plainIframe(host, id, title);
    }, 8000);

    whenApi(function () {
      if (playerRow !== thisRow || !host.parentNode) return;  // closed or fell back meanwhile
      if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
      player = new YT.Player(host, {
        width: '100%', height: '100%',
        videoId: id,
        playerVars: { autoplay: 1, controls: 1, playsinline: 1, rel: 0, origin: window.location.origin },
        events: {
          // Created inside the listener's Play click, so this is user-started playback.
          onReady: function (e) { if (e.target && e.target.playVideo) e.target.playVideo(); },
          onStateChange: function (e) {
            if (e.data === YT.PlayerState.PLAYING) errorsInRow = 0;
            if (e.data === YT.PlayerState.ENDED) advance(true);
          },
          onError: function () {
            // Video removed or blocked from embedding: skip it, but don't spin forever.
            errorsInRow++;
            if (errorsInRow > 5) { setCaption('These videos can’t be played here right now.'); return; }
            advance(true);
          }
        }
      });
      var f = playerBox.querySelector('iframe');
      if (f) { f.title = title; f.referrerPolicy = 'strict-origin-when-cross-origin'; }
    });
  }

  function table0(btn) { return btn.closest('table'); }

  tables.forEach(function (table) {
    table.addEventListener('click', function (e) {
      var btn = e.target.closest(BTN);
      if (!btn || !table.contains(btn)) return;
      if (btn === current) { closePlayer(); return; }
      loadStatus().then(function () { openAt(btn); });
    });
    // Sorting moves rows around, so close the player first.
    Array.prototype.forEach.call(table.querySelectorAll('thead button'), function (b) {
      b.addEventListener('click', closePlayer);
    });
  });
})();
