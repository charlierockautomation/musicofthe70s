/* ============================================================
   Music of the 70s: Listen Now player (YouTube IFrame Player API).

   The player is a VISIBLE, standard YouTube player (controls on, YouTube
   logo intact, fullscreen allowed) shown as the radio's "screen". It is
   never hidden, shrunk below 200x200, covered, or moved off screen.
   Playback starts only from a user action. Automatic advance is gated by
   ScreenWatch: it runs only while more than half of the player is on
   screen and the tab is visible.
   Rules and checklist: .claude/skills/youtube-compliance/SKILL.md
   ============================================================ */

/* ---------- RadioPlayer: shared YouTube IFrame Player singleton ---------- */
var RadioPlayer = (function () {
  var player = null;
  var apiReady = false;
  var apiRequested = false;
  var pendingInit = null;
  var readyTimer = null;
  var hooks = {};
  // Listener's volume (0-100) and mute choice. Kept here so they can be set
  // before the player exists, then applied the moment it is ready.
  var volume = 80;
  var muted = false;

  function applyAudio() {
    if (!player || !player.setVolume) return;
    try {
      player.setVolume(volume);
      if (muted) player.mute(); else player.unMute();
    } catch (err) { /* player not ready yet; onReady applies it */ }
  }

  window.onYouTubeIframeAPIReady = function () {
    apiReady = true;
    if (pendingInit) { var fn = pendingInit; pendingInit = null; fn(); }
  };

  function clearReadyTimer() {
    if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
  }

  function create(elementId, firstVideoId) {
    // width/height 100% fill the framed screen (see .radio-screen-frame in
    // css/style.css, which enforces a 200px minimum height and 16:9 shape).
    player = new YT.Player(elementId, {
      width: '100%', height: '100%',
      videoId: firstVideoId,
      playerVars: {
        autoplay: 1, controls: 1, playsinline: 1, rel: 0,
        origin: window.location.origin
      },
      events: {
        onReady: function (e) {
          clearReadyTimer();
          applyAudio();
          // create() only ever runs from a Play click or tap, so this
          // explicit call is user-initiated playback.
          if (e.target && e.target.playVideo) e.target.playVideo();
          if (hooks.onReady) hooks.onReady(e);
        },
        onStateChange: function (e) { if (hooks.onStateChange) hooks.onStateChange(e); },
        onError: function (e) { if (hooks.onError) hooks.onError(e); }
      }
    });
  }

  return {
    /* Load YouTube's IFrame API script once. Does not create a player. */
    loadApi: function () {
      if (apiRequested) return;
      apiRequested = true;
      var tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      document.head.appendChild(tag);
    },
    init: function (elementId, firstVideoId, opts) {
      hooks = opts || {};
      clearReadyTimer();
      readyTimer = setTimeout(function () {
        if (hooks.onReadyTimeout) hooks.onReadyTimeout();
      }, (opts && opts.readyTimeoutMs) || 9000);
      var start = function () { create(elementId, firstVideoId); };
      if (apiReady && window.YT && window.YT.Player) start();
      else pendingInit = start;
    },
    setHooks: function (opts) { hooks = opts || {}; },
    loadVideo: function (id) {
      if (player && player.loadVideoById) player.loadVideoById(id);
    },
    stop: function () {
      if (player && player.stopVideo) player.stopVideo();
    },
    isActive: function () { return !!player; },
    /* Volume controls (0-100). Work before the player exists. */
    setVolume: function (v) {
      volume = Math.max(0, Math.min(100, Math.round(v)));
      if (volume > 0) muted = false;
      applyAudio();
    },
    setMuted: function (m) { muted = !!m; applyAudio(); },
    getVolume: function () { return volume; },
    isMuted: function () { return muted; },
    /* Pick up a change made with YouTube's own volume control in the player. */
    syncFromPlayer: function () {
      if (!player || !player.getVolume || !player.isMuted) return false;
      try {
        var v = player.getVolume(), m = player.isMuted();
        if (typeof v !== 'number' || (v === volume && m === muted)) return false;
        volume = v; muted = m;
        return true;
      } catch (err) { return false; }
    },
    getState: function () {
      return (player && player.getPlayerState) ? player.getPlayerState() : null;
    },
    seekNearEnd: function () {
      if (player && player.getDuration && player.seekTo) {
        var d = player.getDuration();
        if (d) player.seekTo(Math.max(0, d - 1.5), true);
      }
    }
  };
})();

/* ---------- ScreenWatch: is the player on screen right now? ---------- */
var ScreenWatch = (function () {
  var el = null;
  var listeners = [];

  function notify() { listeners.forEach(function (fn) { fn(); }); }

  /* Share of the player's box inside the viewport, 0 to 1. */
  function ratio() {
    if (!el) return 0;
    var r = el.getBoundingClientRect();
    var area = r.width * r.height;
    if (!area) return 0;
    var w = Math.min(r.right, window.innerWidth) - Math.max(r.left, 0);
    var h = Math.min(r.bottom, window.innerHeight) - Math.max(r.top, 0);
    return (w > 0 && h > 0) ? (w * h) / area : 0;
  }

  return {
    init: function (element) {
      el = element;
      document.addEventListener('visibilitychange', notify);
      window.addEventListener('resize', notify);
      if ('IntersectionObserver' in window) {
        var steps = [];
        for (var i = 0; i <= 20; i++) steps.push(i / 20);
        steps.push(0.51);
        new IntersectionObserver(notify, { threshold: steps }).observe(el);
      } else {
        window.addEventListener('scroll', notify, { passive: true });
      }
    },
    /* True only when the tab is visible and MORE than half the player shows. */
    visible: function () {
      return document.visibilityState === 'visible' && ratio() > 0.5;
    },
    onChange: function (fn) { listeners.push(fn); }
  };
})();
