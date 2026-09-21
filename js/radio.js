/* ============================================================
   Music of the 70s: Listen Now (radio + jukebox)

   Uses js/radio-player.js: ONE visible YouTube player (the radio's
   "screen") shared by the Stations panel and every Jukebox tile.
   - Playback starts only from a click or tap.
   - After that, continuous auto-advance runs only while more than half
     of the player is on screen and the tab is visible. Otherwise it holds
     until the player is back in view or the listener presses Continue
     (YouTube Required Minimum Functionality).
   - Songs whose stored YouTube status says made-for-kids are dropped from
     the radio and Jukebox; non-embeddable ones are shown as unavailable.
   Rules: .claude/skills/youtube-compliance/SKILL.md
   ============================================================ */

/* ---------- App ---------- */
(function () {
  var RADIO_DATA_PATH = '/data/radio/radio-songs.json';
  var STATUS_DATA_PATH = '/data/youtube-status.json';
  var IDLE_NOTE = 'Pick a station and press Play, or choose any song in the Jukebox Grid.';
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
  var screenEl = document.getElementById('ytPlayerHost');
  var screenNote = document.getElementById('screenNote');
  var continueBtn = document.getElementById('radioContinueBtn');

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
  var statusById = {};        // videoId -> {embeddable, madeForKids, checked_at, ...}
  var heldNext = false;       // auto-advance is waiting for the player to be on screen
  var gridPage = 1;

  /* ---------- YouTube status (data/youtube-status.json) ---------- */
  function isKids(s) {
    var st = s.youtube_id && statusById[s.youtube_id];
    return !!(st && st.madeForKids === true);
  }
  function isPlayable(s) {
    if (!s.youtube_id) return false;
    var st = statusById[s.youtube_id];
    return !(st && (st.embeddable === false || st.madeForKids === true));
  }
  async function loadStatus() {
    try {
      var data = await loadJSON(STATUS_DATA_PATH);
      statusById = (data && data.videos) || {};
    } catch (e) { statusById = {}; }
  }

  /* ---------- Screen note (sits under the player, never over it) ---------- */
  function setScreenNote(text) { if (screenNote) screenNote.textContent = text; }
  function renderScreenNote() {
    if (!currentSong || !source) { setScreenNote(IDLE_NOTE); return; }
    setScreenNote('Now playing: ' + (currentSong.title || 'Unknown Title') + ' by ' +
      (currentSong.artist || 'Unknown Artist') + (currentSong.year ? ' (' + currentSong.year + ')' : ''));
  }

  /* ---------- Hold auto-advance while the player is off screen ---------- */
  function holdNext() {
    heldNext = true;
    continueBtn.classList.remove('hidden');
    setScreenNote('Next song is ready. It starts when this player is back on screen, or press Continue.');
    if (stStatus) stStatus.textContent = 'Paused between songs';
  }
  function clearHold() {
    heldNext = false;
    continueBtn.classList.add('hidden');
  }
  /* auto=true: the player moves on by itself (song ended, error skip). */
  function advance(auto) {
    if (auto && !ScreenWatch.visible()) { holdNext(); return; }
    clearHold();
    nextTrack();
  }
  ScreenWatch.onChange(function () {
    if (heldNext && source && ScreenWatch.visible()) { clearHold(); nextTrack(); }
  });
  continueBtn.addEventListener('click', function () { clearHold(); nextTrack(); });

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
      if (candidate && isPlayable(candidate)) { song = candidate; break; }
    }
    if (!song) { stopPlayback(); return; }
    currentSong = song;
    if (source === 'station') activeGenre = song.genre;
    else activeRadioId = song.radio_id;
    renderNowPlaying(true);
    renderScreenNote();
    updateStationUI();
    updateGridActiveState();
    RadioPlayer.loadVideo(song.youtube_id);
  }

  function startPlayback(songs, shuffleIt, startIndex, src) {
    loadToken += 1;
    var token = loadToken;
    clearHold();
    source = src;
    consecutiveFails = 0;
    buildQueue(songs, shuffleIt);
    queueIdx = startIndex || 0;
    var song = queue[queueIdx++];
    currentSong = song;
    if (src === 'station') { activeGenre = song.genre; activeRadioId = null; }
    else { activeRadioId = song.radio_id; activeGenre = null; }
    renderNowPlaying(true);
    renderScreenNote();
    updateStationUI();
    updateGridActiveState();
    // A tile far down the grid can be clicked while the player is off screen:
    // scroll the player into view so the listener sees what is playing.
    if (!ScreenWatch.visible() && screenEl.scrollIntoView) {
      screenEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

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
    clearHold();
    RadioPlayer.stop();
    source = null;
    activeGenre = null;
    activeRadioId = null;
    currentSong = null;
    queue = [];
    queueIdx = 0;
    consecutiveFails = 0;
    renderNowPlaying(false);
    renderScreenNote();
    updateStationUI();
    updateGridActiveState();
  }

  /* ---------- Volume (own controls next to the player, never over it) ---------- */
  var VOL_KEY = 'radioVolume';
  var volSlider = document.getElementById('volSlider');
  var volMuteBtn = document.getElementById('volMuteBtn');
  var volIcon = document.getElementById('volIcon');
  var volValue = document.getElementById('volValue');

  function saveVolume() {
    try {
      localStorage.setItem(VOL_KEY, JSON.stringify({ v: RadioPlayer.getVolume(), m: RadioPlayer.isMuted() }));
    } catch (err) { /* storage blocked: the setting just isn't remembered */ }
  }

  function renderVolume() {
    if (!volSlider) return;
    var m = RadioPlayer.isMuted(), v = RadioPlayer.getVolume();
    var shown = m ? 0 : v;
    volSlider.value = shown;
    volValue.textContent = shown + '%';
    volIcon.textContent = shown === 0 ? '🔇' : (shown < 50 ? '🔉' : '🔊');
    volMuteBtn.setAttribute('aria-label', m || v === 0 ? 'Unmute' : 'Mute');
    volMuteBtn.setAttribute('aria-pressed', m || v === 0 ? 'true' : 'false');
  }

  function initVolume() {
    if (!volSlider) return;
    try {
      var saved = JSON.parse(localStorage.getItem(VOL_KEY) || 'null');
      if (saved && typeof saved.v === 'number') { RadioPlayer.setVolume(saved.v); RadioPlayer.setMuted(!!saved.m); }
    } catch (err) { /* ignore unreadable saved value */ }
    volSlider.addEventListener('input', function () {
      RadioPlayer.setVolume(Number(volSlider.value));
      renderVolume(); saveVolume();
    });
    volMuteBtn.addEventListener('click', function () {
      if (RadioPlayer.isMuted() || RadioPlayer.getVolume() === 0) {
        if (RadioPlayer.getVolume() === 0) RadioPlayer.setVolume(60);
        RadioPlayer.setMuted(false);
      } else {
        RadioPlayer.setMuted(true);
      }
      renderVolume(); saveVolume();
    });
    renderVolume();
  }

  function onPlayerReady() { /* the Play click that created the player starts the first track */ }

  function onPlayerStateChange(e) {
    // Keep our slider in step if the listener used YouTube's own volume control.
    if (RadioPlayer.syncFromPlayer()) { renderVolume(); saveVolume(); }
    if (e.data === YT.PlayerState.PLAYING) {
      consecutiveFails = 0;
      if (stStatus) stStatus.textContent = 'Playing';
      updateGridActiveState();
    } else if (e.data === YT.PlayerState.ENDED) {
      advance(true);
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
    advance(true);
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
    var count = allSongs.filter(function (s) { return s.genre === genre && isPlayable(s); }).length;
    var totalInGenre = allSongs.filter(function (s) { return s.genre === genre; }).length;
    stationCountEl.textContent = count + ' of ' + totalInGenre + ' songs in this station have a verified video';
  }
  stationSelect.addEventListener('change', updateStationCount);

  stationPlayBtn.addEventListener('click', function () {
    var genre = stationSelect.value;
    var pool = allSongs.filter(function (s) { return s.genre === genre && isPlayable(s); });
    if (!pool.length) {
      stationCountEl.textContent = 'No playable songs yet for "' + genreLabel(genre) + '" — video check still in progress.';
      return;
    }
    startPlayback(pool, true, 0, 'station');
  });
  stationSkipBtn.addEventListener('click', function () { if (source === 'station') advance(false); });
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
      var playable = isPlayable(s);
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
          : '  <p class="jt-pending">' + (s.youtube_id ? 'Video unavailable' : 'Video pending') + '</p>') +
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
          var pool = lastFiltered.filter(isPlayable);
          var startSong = lastFiltered[idx];
          if (!isPlayable(startSong)) return;
          var poolIdx = pool.findIndex(function (s) { return s.radio_id === radioId; });
          startPlayback(pool, false, poolIdx, 'grid');
        });
      }
      if (skipBtn) skipBtn.addEventListener('click', function () { if (source === 'grid') advance(false); });
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
    toolEl.classList.toggle('grid-mode', !isStations);
    stationsView.classList.toggle('hidden', !isStations);
    gridView.classList.toggle('hidden', isStations);
    viewStationsBtn.classList.toggle('active', isStations);
    viewStationsBtn.setAttribute('aria-selected', String(isStations));
    viewGridBtn.classList.toggle('active', !isStations);
    viewGridBtn.setAttribute('aria-selected', String(!isStations));
  }
  viewStationsBtn.addEventListener('click', function () { setView('stations'); });
  viewGridBtn.addEventListener('click', function () { setView('grid'); });

  /* ---------- Deep link: ?play=<radio_id> jumps straight to a song's
     jukebox tile from an external link (e.g. a blog post). Scrolls to
     and highlights the tile rather than auto-starting playback, since
     unmuted YouTube autoplay without a direct user gesture is blocked
     by browser autoplay policy in most cases anyway. ---------- */
  function applyDeepLink() {
    var radioId = new URLSearchParams(window.location.search).get('play');
    if (!radioId) return;
    var idx = allSongs.findIndex(function (s) { return s.radio_id === radioId; });
    if (idx === -1) return;
    setView('grid');
    filterGenre.value = '';
    filterYear.value = '';
    filterSearch.value = '';
    gridPage = Math.floor(idx / PAGE_SIZE) + 1;
    renderGrid();
    var tile = jukeboxGrid.querySelector('[data-radio-id="' + CSS.escape(radioId) + '"]');
    if (!tile) return;
    tile.classList.add('deep-link-target');
    tile.scrollIntoView({ behavior: 'smooth', block: 'center' });
    var playBtn = tile.querySelector('.jt-play');
    if (playBtn) playBtn.focus();
    setTimeout(function () { tile.classList.remove('deep-link-target'); }, 3200);
  }

  /* Sticky screen (desktop Jukebox view) sits just below the sticky site header. */
  function setHeaderHeightVar() {
    var header = document.querySelector('.site-header');
    if (header) document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }

  /* ---------- Init ---------- */
  (async function init() {
    try {
      allSongs = await loadJSON(RADIO_DATA_PATH);
      await loadStatus();
      allSongs = allSongs.filter(function (s) { return !isKids(s); });
      if (!Array.isArray(allSongs) || !allSongs.length) {
        throw new Error('Radio catalog is empty.');
      }
      buildStationOptions(allSongs);
      populateFilterOptions(allSongs);
      renderGrid();
      updateStationUI();
      loadingEl.classList.add('hidden');
      toolEl.classList.remove('hidden');
      ScreenWatch.init(screenEl);
      initVolume();
      setHeaderHeightVar();
      window.addEventListener('resize', setHeaderHeightVar);
      applyDeepLink();
      renderScreenNote();

      // Load YouTube's IFrame API script once the rest of the page is ready.
      // This loads the script only; no player exists until a Play click.
      RadioPlayer.loadApi();
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
        consecutiveFails: consecutiveFails, playerState: RadioPlayer.getState(),
        held: heldNext, screenVisible: ScreenWatch.visible()
      };
    },
    forceEnded: function () { onPlayerStateChange({ data: YT.PlayerState.ENDED }); },
    seekNearEnd: function () { RadioPlayer.seekNearEnd(); }
  };
})();
