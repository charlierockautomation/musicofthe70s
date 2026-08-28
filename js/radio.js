/* ============================================================
   Music of the 70s — Listen Now (radio + jukebox)
   Player engine ported directly from 1960smusic.net's Radio Dial
   (tools/radio/radio-player.js), which already works in production:
   a hidden, audio-only YouTube IFrame Player singleton, real
   onError/onReadyTimeout handling and auto-advance on ENDED.
   ============================================================ */

/* ---------- RadioPlayer: hidden audio-only YouTube IFrame Player singleton ---------- */
var RadioPlayer = (function () {
  var player = null;
  var apiReady = false;
  var pendingInit = null;
  var readyTimer = null;
  var hooks = {};

  window.onYouTubeIframeAPIReady = function () {
    apiReady = true;
    if (pendingInit) { var fn = pendingInit; pendingInit = null; fn(); }
  };

  function clearReadyTimer() {
    if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
  }

  function create(elementId, firstVideoId) {
    player = new YT.Player(elementId, {
      height: '1', width: '1',
      videoId: firstVideoId,
      playerVars: { autoplay: 1, controls: 0, disablekb: 1, fs: 0, modestbranding: 1, playsinline: 1 },
      events: {
        onReady: function (e) { clearReadyTimer(); if (hooks.onReady) hooks.onReady(e); },
        onStateChange: function (e) { if (hooks.onStateChange) hooks.onStateChange(e); },
        onError: function (e) { if (hooks.onError) hooks.onError(e); }
      }
    });
  }

  return {
    init: function (elementId, firstVideoId, opts) {
      hooks = opts || {};
      clearReadyTimer();
      readyTimer = setTimeout(function () {
        if (hooks.onReadyTimeout) hooks.onReadyTimeout();
      }, opts.readyTimeoutMs || 9000);
      var start = function () { create(elementId, firstVideoId); };
      if (apiReady && window.YT && window.YT.Player) start();
      else pendingInit = start;
    },
    setHooks: function (opts) {
      hooks = opts || {};
    },
    loadVideo: function (id) {
      if (player && player.loadVideoById) player.loadVideoById(id);
    },
    stop: function () {
      if (player && player.stopVideo) player.stopVideo();
    },
    destroy: function () {
      clearReadyTimer();
      pendingInit = null;
      if (player && player.destroy) { try { player.destroy(); } catch (e) {} }
      player = null;
    },
    isActive: function () { return !!player; },
    getState: function () { return (player && player.getPlayerState) ? player.getPlayerState() : null; },
    seekNearEnd: function () {
      if (player && player.getDuration && player.seekTo) {
        var d = player.getDuration();
        if (d) player.seekTo(Math.max(0, d - 1.5), true);
      }
    }
  };
})();

/* ---------- App ---------- */
(function () {
  var RADIO_DATA_PATH = '/data/radio/radio-songs.json';
  var PAGE_SIZE = 48;
  // Video error codes worth auto-skipping past (matches 1960smusic.net):
  // 2=invalid param, 5=HTML5 error, 100=not found/removed, 101/150=embed
  // disabled by the video owner. These can surface at real playback time
  // even after a video passed the embeddable/public check during
  // enrichment (the owner can disable embedding, region-lock, etc. later).
  var SKIP_CODES = { 2: 1, 5: 1, 100: 1, 101: 1, 150: 1 };

  var GENRE_LABELS = {
    'pop': 'Pop', 'soul': 'Soul', 'rnb': 'R&B', 'soft-rock': 'Soft Rock',
    'classic-rock': 'Classic Rock', 'hard-rock': 'Hard Rock', 'prog-rock': 'Prog Rock',
    'disco': 'Disco', 'country': 'Country', 'funk': 'Funk', 'punk': 'Punk'
  };
  function genreLabel(genre) {
    return GENRE_LABELS[genre] || (genre ? genre.replace(/-/g, ' ') : 'Unknown');
  }

  var loadingEl = document.getElementById('loading');
  var errorEl = document.getElementById('error');
  var toolEl = document.getElementById('radioTool');

  var viewStationsBtn = document.getElementById('viewStationsBtn');
  var viewGridBtn = document.getElementById('viewGridBtn');
  var stationsView = document.getElementById('stationsView');
  var gridView = document.getElementById('gridView');

  var stationSelect = document.getElementById('stationSelect');
  var stationPlayBtn = document.getElementById('stationPlayBtn');
  var stationSkipBtn = document.getElementById('stationSkipBtn');
  var stationStopBtn = document.getElementById('stationStopBtn');
  var stationCountEl = document.getElementById('stationCount');
  var stationNowPlaying = document.getElementById('stationNowPlaying');
  var stTitle = document.getElementById('stTitle');
  var stArtist = document.getElementById('stArtist');
  var stStatus = document.getElementById('stStatus');

  var filterGenre = document.getElementById('filterGenre');
  var filterYear = document.getElementById('filterYear');
  var filterSearch = document.getElementById('filterSearch');
  var jukeboxGrid = document.getElementById('jukeboxGrid');
  var jukeboxPagination = document.getElementById('jukeboxPagination');
  var jukeboxResultCount = document.getElementById('jukeboxResultCount');

  var allSongs = [];
  var gridPage = 1;

  // Playback state -- one shared RadioPlayer instance site-wide, so exactly
  // one thing plays at a time. `source` says whether the Stations panel or
  // a Jukebox Grid card currently owns it, and drives which UI shows
  // active controls.
  var source = null;          // null | 'station' | 'grid'
  var queue = [];
  var queueIdx = 0;
  var currentSong = null;
  var activeGenre = null;     // set when source === 'station'
  var activeRadioId = null;   // set when source === 'grid'
  var consecutiveFails = 0;
  var loadToken = 0;

  /* ---------- Queue + playback core (ported pattern) ---------- */
  function buildQueue(songs, shuffleIt) {
    queue = shuffleIt ? shuffle(songs.slice()) : songs.slice();
    queueIdx = 0;
  }

  function nextTrack() {
    if (!queue.length) return;
    // Defensive: queues are already built from youtube_id-having songs only
    // (see startPlayback), but never trust that a queue can't somehow end
    // up with a non-playable entry -- skip forward past any that lack a
    // verified id rather than trying to play one.
    var attempts = 0;
    var song = null;
    while (attempts < queue.length) {
      if (queueIdx >= queue.length) {
        // Station pools reshuffle on wrap (continuous radio); grid pools
        // just loop back to the start of the current filtered order.
        if (source === 'station') queue = shuffle(queue.slice());
        queueIdx = 0;
      }
      var candidate = queue[queueIdx++];
      attempts += 1;
      if (candidate && candidate.youtube_id) { song = candidate; break; }
    }
    if (!song) { stopPlayback(); return; }
    currentSong = song;
    if (source === 'station') activeGenre = song.genre;
    else activeRadioId = song.radio_id;
    renderNowPlaying(true);
    updateStationUI();
    updateGridActiveState();
    RadioPlayer.loadVideo(song.youtube_id);
  }

  function startPlayback(songs, shuffleIt, startIndex, src) {
    loadToken += 1;
    var token = loadToken;
    source = src;
    consecutiveFails = 0;
    buildQueue(songs, shuffleIt);
    queueIdx = startIndex || 0;
    var song = queue[queueIdx++];
    currentSong = song;
    if (src === 'station') { activeGenre = song.genre; activeRadioId = null; }
    else { activeRadioId = song.radio_id; activeGenre = null; }
    renderNowPlaying(true);
    updateStationUI();
    updateGridActiveState();

    var opts = {
      readyTimeoutMs: 9000,
      onReady: function () { if (token === loadToken) onPlayerReady(); },
      onStateChange: function (e) { if (token === loadToken) onPlayerStateChange(e); },
      onError: function (e) { if (token === loadToken) onPlayerError(e); },
      onReadyTimeout: function () { if (token === loadToken) onReadyTimeout(); }
    };

    if (!RadioPlayer.isActive()) {
      RadioPlayer.init('ytPlayer', song.youtube_id, opts);
    } else {
      // Re-bind hooks to this call's `token` every time -- without this,
      // any startPlayback after the very first one (Stop then Play again,
      // switching stations, picking a new grid tile) keeps the stale
      // closure from the first init, whose `token` never matches the
      // current loadToken again. ENDED/onError silently stop firing and
      // auto-advance dies for the rest of the page session.
      RadioPlayer.setHooks(opts);
      RadioPlayer.loadVideo(song.youtube_id);
    }
  }

  function stopPlayback() {
    loadToken += 1;
    RadioPlayer.stop();
    source = null;
    activeGenre = null;
    activeRadioId = null;
    currentSong = null;
    queue = [];
    queueIdx = 0;
    consecutiveFails = 0;
    renderNowPlaying(false);
    updateStationUI();
    updateGridActiveState();
  }

  function onPlayerReady() { /* first track autoplays via playerVars.autoplay */ }

  function onPlayerStateChange(e) {
    if (e.data === YT.PlayerState.PLAYING) {
      consecutiveFails = 0;
      if (stStatus) stStatus.textContent = 'Playing';
      updateGridActiveState();
    } else if (e.data === YT.PlayerState.ENDED) {
      nextTrack();
    }
  }

  function onPlayerError(e) {
    if (!SKIP_CODES[e.data]) return;
    consecutiveFails += 1;
    if (consecutiveFails >= 3) {
      if (stStatus) stStatus.textContent = 'Trouble playing this station right now. Stopped.';
      stopPlayback();
      return;
    }
    nextTrack();
  }

  function onReadyTimeout() {
    if (stStatus) stStatus.textContent = 'Player is taking a while to load. Try Stop and Play again.';
  }

  /* ---------- Stations panel UI ---------- */
  function renderNowPlaying(loading) {
    if (!currentSong || source !== 'station') {
      stationNowPlaying.classList.add('hidden');
      return;
    }
    stationNowPlaying.classList.remove('hidden');
    stTitle.textContent = currentSong.title || 'Unknown Title';
    stArtist.textContent = (currentSong.artist || 'Unknown Artist') + ' · ' + (currentSong.year || '');
    stStatus.textContent = loading ? 'Tuning in…' : 'Playing';
  }

  function updateStationUI() {
    var active = source === 'station';
    stationPlayBtn.disabled = false;
    stationSkipBtn.disabled = !active;
    stationStopBtn.disabled = !active;
    if (!active) stationNowPlaying.classList.add('hidden');
  }

  function updateStationCount() {
    var genre = stationSelect.value;
    var count = allSongs.filter(function (s) { return s.genre === genre && s.youtube_id; }).length;
    var totalInGenre = allSongs.filter(function (s) { return s.genre === genre; }).length;
    stationCountEl.textContent = count + ' of ' + totalInGenre + ' songs in this station have a verified video';
  }
  stationSelect.addEventListener('change', updateStationCount);

  stationPlayBtn.addEventListener('click', function () {
    var genre = stationSelect.value;
    var pool = allSongs.filter(function (s) { return s.genre === genre && s.youtube_id; });
    if (!pool.length) {
      stationCountEl.textContent = 'No playable songs yet for "' + genreLabel(genre) + '" — enrichment still in progress.';
      return;
    }
    startPlayback(pool, true, 0, 'station');
  });
  stationSkipBtn.addEventListener('click', function () { if (source === 'station') nextTrack(); });
  stationStopBtn.addEventListener('click', stopPlayback);

  /* ---------- Stations dropdown population ---------- */
  function buildStationOptions(songs) {
    var counts = {};
    songs.forEach(function (s) { counts[s.genre] = (counts[s.genre] || 0) + 1; });
    var genres = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; });
    stationSelect.innerHTML = genres
      .map(function (g) { return '<option value="' + escapeHTML(g) + '">' + escapeHTML(genreLabel(g)) + ' (' + counts[g] + ')</option>'; })
      .join('');
    stationSelect.selectedIndex = 0;
    updateStationCount();
  }

  /* ---------- Jukebox grid view ---------- */
  function populateFilterOptions(songs) {
    var genres = Array.from(new Set(songs.map(function (s) { return s.genre; }))).sort();
    genres.forEach(function (g) {
      var opt = document.createElement('option');
      opt.value = g;
      opt.textContent = genreLabel(g);
      filterGenre.appendChild(opt);
    });
    var years = Array.from(new Set(songs.map(function (s) { return s.year; }))).sort();
    years.forEach(function (y) {
      var opt = document.createElement('option');
      opt.value = String(y);
      opt.textContent = String(y);
      filterYear.appendChild(opt);
    });
  }

  var lastFiltered = [];
  function getFilteredSongs() {
    var genre = filterGenre.value;
    var year = filterYear.value;
    var search = filterSearch.value.trim().toLowerCase();
    return allSongs.filter(function (s) {
      if (genre && s.genre !== genre) return false;
      if (year && String(s.year) !== year) return false;
      if (search) {
        var hay = ((s.title || '') + ' ' + (s.artist || '')).toLowerCase();
        if (hay.indexOf(search) === -1) return false;
      }
      return true;
    });
  }

  function renderGrid() {
    var filtered = getFilteredSongs();
    lastFiltered = filtered;
    var totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    if (gridPage > totalPages) gridPage = totalPages;
    var start = (gridPage - 1) * PAGE_SIZE;
    var pageSongs = filtered.slice(start, start + PAGE_SIZE);

    jukeboxResultCount.textContent = filtered.length + ' song' + (filtered.length === 1 ? '' : 's') + ' found';

    jukeboxGrid.innerHTML = pageSongs.map(function (s) {
      var playable = !!s.youtube_id;
      return '' +
        '<div class="jukebox-tile" data-radio-id="' + escapeHTML(s.radio_id) + '">' +
        '  <div class="jt-top-row">' +
        '    <span class="badge">' + escapeHTML(genreLabel(s.genre)) + '</span>' +
        '    <span class="jt-year">' + escapeHTML(String(s.year)) + '</span>' +
        '  </div>' +
        '  <p class="jt-title">' + escapeHTML(s.title) + '</p>' +
        '  <p class="jt-artist">' + escapeHTML(s.artist) + '</p>' +
        '  <p class="jt-status hidden"></p>' +
        (playable
          ? '  <div class="jt-controls">' +
            '    <button class="jt-play np-btn" aria-label="Play">▶</button>' +
            '    <button class="jt-skip np-btn" aria-label="Skip" disabled>⏭</button>' +
            '    <button class="jt-stop np-btn" aria-label="Stop" disabled>⏹</button>' +
            '  </div>'
          : '  <p class="jt-pending">Video pending</p>') +
        '</div>';
    }).join('');

    jukeboxGrid.querySelectorAll('.jukebox-tile').forEach(function (tile) {
      var radioId = tile.getAttribute('data-radio-id');
      var playBtn = tile.querySelector('.jt-play');
      var skipBtn = tile.querySelector('.jt-skip');
      var stopBtn = tile.querySelector('.jt-stop');
      if (playBtn) {
        playBtn.addEventListener('click', function () {
          var idx = lastFiltered.findIndex(function (s) { return s.radio_id === radioId; });
          if (idx === -1) return;
          var pool = lastFiltered.filter(function (s) { return s.youtube_id; });
          var startSong = lastFiltered[idx];
          if (!startSong.youtube_id) return;
          var poolIdx = pool.findIndex(function (s) { return s.radio_id === radioId; });
          startPlayback(pool, false, poolIdx, 'grid');
        });
      }
      if (skipBtn) skipBtn.addEventListener('click', function () { if (source === 'grid') nextTrack(); });
      if (stopBtn) stopBtn.addEventListener('click', stopPlayback);
    });

    updateGridActiveState();

    jukeboxPagination.innerHTML = totalPages > 1
      ? '<button id="jpPrev" class="btn-secondary" ' + (gridPage <= 1 ? 'disabled' : '') + '>← Prev</button>' +
        '<span>Page ' + gridPage + ' of ' + totalPages + '</span>' +
        '<button id="jpNext" class="btn-secondary" ' + (gridPage >= totalPages ? 'disabled' : '') + '>Next →</button>'
      : '';
    var prevBtn = document.getElementById('jpPrev');
    var nextBtn = document.getElementById('jpNext');
    if (prevBtn) prevBtn.addEventListener('click', function () { gridPage -= 1; renderGrid(); window.scrollTo({ top: gridView.offsetTop - 80, behavior: 'smooth' }); });
    if (nextBtn) nextBtn.addEventListener('click', function () { gridPage += 1; renderGrid(); window.scrollTo({ top: gridView.offsetTop - 80, behavior: 'smooth' }); });
  }

  function updateGridActiveState() {
    jukeboxGrid.querySelectorAll('.jukebox-tile').forEach(function (tile) {
      var radioId = tile.getAttribute('data-radio-id');
      var isActive = source === 'grid' && radioId === activeRadioId;
      tile.classList.toggle('active', isActive);
      var playBtn = tile.querySelector('.jt-play');
      var skipBtn = tile.querySelector('.jt-skip');
      var stopBtn = tile.querySelector('.jt-stop');
      var status = tile.querySelector('.jt-status');
      if (playBtn) playBtn.disabled = isActive;
      if (skipBtn) skipBtn.disabled = !isActive;
      if (stopBtn) stopBtn.disabled = !isActive;
      if (status) {
        status.classList.toggle('hidden', !isActive);
        status.textContent = isActive ? 'Now Playing' : '';
      }
    });
  }

  filterGenre.addEventListener('change', function () { gridPage = 1; renderGrid(); });
  filterYear.addEventListener('change', function () { gridPage = 1; renderGrid(); });
  var searchDebounce;
  filterSearch.addEventListener('input', function () {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(function () { gridPage = 1; renderGrid(); }, 250);
  });

  /* ---------- View toggle ---------- */
  function setView(view) {
    var isStations = view === 'stations';
    stationsView.classList.toggle('hidden', !isStations);
    gridView.classList.toggle('hidden', isStations);
    viewStationsBtn.classList.toggle('active', isStations);
    viewStationsBtn.setAttribute('aria-selected', String(isStations));
    viewGridBtn.classList.toggle('active', !isStations);
    viewGridBtn.setAttribute('aria-selected', String(!isStations));
  }
  viewStationsBtn.addEventListener('click', function () { setView('stations'); });
  viewGridBtn.addEventListener('click', function () { setView('grid'); });

  /* ---------- Init ---------- */
  (async function init() {
    try {
      allSongs = await loadJSON(RADIO_DATA_PATH);
      if (!Array.isArray(allSongs) || !allSongs.length) {
        throw new Error('Radio catalog is empty.');
      }
      buildStationOptions(allSongs);
      populateFilterOptions(allSongs);
      renderGrid();
      updateStationUI();
      loadingEl.classList.add('hidden');
      toolEl.classList.remove('hidden');

      // Load the IFrame API script once the rest of the page is ready.
      var tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      document.head.appendChild(tag);
    } catch (err) {
      console.error('Radio failed to load:', err);
      loadingEl.classList.add('hidden');
      errorEl.textContent = 'Sorry — we couldn\'t load the radio catalog right now. Please refresh the page to try again.';
      errorEl.classList.remove('hidden');
    }
  })();

  // Diagnostic hook (QA/debugging only, no user-facing effect): lets
  // devtools/automated checks inspect playback state and simulate an
  // ENDED event without waiting out a real song.
  window.__radioDebug = {
    state: function () {
      return {
        source: source, activeGenre: activeGenre, activeRadioId: activeRadioId,
        currentSong: currentSong, queueLen: queue.length, queueIdx: queueIdx,
        consecutiveFails: consecutiveFails, playerState: RadioPlayer.getState()
      };
    },
    forceEnded: function () { onPlayerStateChange({ data: YT.PlayerState.ENDED }); },
    seekNearEnd: function () { RadioPlayer.seekNearEnd(); }
  };
})();
