/* ============================================================
   Music of the 70s — Shared JavaScript Utilities
   ============================================================ */

/* Fisher-Yates in-place shuffle (returns the same array, shuffled). */
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

/* Fetch a single JSON file with error handling. */
async function loadJSON(path) {
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`Failed to load ${path} (HTTP ${res.status})`);
  }
  return res.json();
}

/* Load multiple JSON files in parallel. Returns array of parsed results
   in the same order as the input paths. */
async function loadJSONMultiple(paths) {
  return Promise.all(paths.map((p) => loadJSON(p)));
}

/* Copy text to clipboard with a graceful fallback for older browsers. */
async function copyToClipboard(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch (e) {
    /* fall through to fallback */
  }
  try {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(ta);
    return ok;
  } catch (e) {
    return false;
  }
}

/* Build a YouTube search URL from a free-text query. */
function youtubeSearchURL(query) {
  return `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
}

/* Native share with clipboard fallback. Returns a status string. */
async function shareOrCopy(shareData, fallbackText) {
  if (navigator.share) {
    try {
      await navigator.share(shareData);
      return 'shared';
    } catch (e) {
      if (e && e.name === 'AbortError') return 'cancelled';
      /* fall through to clipboard */
    }
  }
  const ok = await copyToClipboard(fallbackText);
  return ok ? 'copied' : 'failed';
}

/* Map era data values to human-friendly UI labels. */
const ERA_MAP = {
  'early-70s': 'Early 70s (1970–73)',
  'mid-70s':   'Mid 70s (1974–76)',
  'late-70s':  'Late 70s (1977–79)'
};

/* All artist genre data files (root-relative). */
const ARTIST_FILES = [
  '/data/artists/artists_classic_rock.json',
  '/data/artists/artists_hard_rock.json',
  '/data/artists/artists_soft_rock.json',
  '/data/artists/artists_soul_rnb.json',
  '/data/artists/artists_funk.json',
  '/data/artists/artists_disco.json',
  '/data/artists/artists_country.json',
  '/data/artists/artists_prog_rock.json',
  '/data/artists/artists_punk_new_wave.json',
  '/data/artists/artists_pop_crossover.json'
];

/* All year-end Hot 100 song data files (root-relative). */
const SONG_FILES = [
  '/data/songs/hot_100_songs_1970.json',
  '/data/songs/hot_100_songs_1971.json',
  '/data/songs/hot_100_songs_1972.json',
  '/data/songs/hot_100_songs_1973.json',
  '/data/songs/hot_100_songs_1974.json',
  '/data/songs/hot_100_songs_1975.json',
  '/data/songs/hot_100_songs_1976.json',
  '/data/songs/hot_100_songs_1977.json',
  '/data/songs/hot_100_songs_1978.json',
  '/data/songs/hot_100_songs_1979.json'
];

/* Mood label shown per genre on the random song tool. */
const GENRE_MOOD_LINE = {
  'rock':         'Windows down anthem',
  'classic-rock': 'Windows down anthem',
  'hard-rock':    'Turn it up to eleven',
  'prog-rock':    'Headphones, lights off',
  'disco':        'Pure dance floor',
  'soul':         'Feels right',
  'rnb':          'Feels right',
  'country':      'Made for driving',
  'funk':         "Can't sit still",
  'soft-rock':    'Perfect Sunday morning',
  'pop':          'Sing it out loud',
  'punk':         'Loud, fast and free'
};

function moodLineForGenre(genre) {
  return GENRE_MOOD_LINE[(genre || '').toLowerCase()] || 'A 70s classic';
}

/* Escape HTML for safe insertion into innerHTML. */
function escapeHTML(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/* Mobile navigation hamburger toggle — wired up on every page. */
function initNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
    nav.querySelectorAll('a').forEach((a) =>
      a.addEventListener('click', () => nav.classList.remove('open'))
    );
  }
}

/* localStorage helpers (safe — never throw if storage is unavailable). */
function lsGet(key, fallback) {
  try {
    const v = localStorage.getItem(key);
    return v === null ? fallback : v;
  } catch (e) { return fallback; }
}
function lsSet(key, value) {
  try { localStorage.setItem(key, value); } catch (e) { /* ignore */ }
}

document.addEventListener('DOMContentLoaded', initNav);
