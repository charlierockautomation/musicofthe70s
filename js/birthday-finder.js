/* Birthday #1 Song Finder (/pages/birthday-number-one).
   Reads the weekly Billboard Hot 100 file plus data/billboard/number-one-links.json
   (weeks counted from the weekly charts, official Play IDs, story pages, date pages).
   Each chart covers its Saturday issue date through the next Friday. January 1 and 2, 1970
   fall in the last chart of 1969 (dated December 27, 1969), handled as a fixed entry.
   The player is created only when the visitor presses Play, in a visible 16:9 frame. Play is hidden for
   any ID that data/youtube-status.json marks not embeddable or made for kids (same rule as table-player.js). */
(function () {
  const $ = (id) => document.getElementById(id);
  const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const LAST_OF_1969 = { week_start: '1969-12-27', week_end: '1970-01-02', title: "Someday We'll Be Together",
                         artist: 'Diana Ross & the Supremes', y1969: true };
  let weekly = null, links = null, status = {}, rows = [], current = null;

  function fmt(iso) {
    const d = new Date(iso + 'T00:00:00Z');
    return `${MONTHS[d.getUTCMonth()]} ${d.getUTCDate()}, ${d.getUTCFullYear()}`;
  }

  function populate() {
    const m = $('monthSel'), d = $('daySel'), y = $('yearSel');
    MONTHS.forEach((name, i) => m.add(new Option(name, String(i + 1))));
    for (let i = 1; i <= 31; i++) d.add(new Option(String(i), String(i)));
    for (let i = 1970; i <= 1979; i++) y.add(new Option(String(i), String(i)));
  }

  function lookup(iso) {
    if (iso < rows[0].week_start) return LAST_OF_1969;
    for (const e of rows) if (iso >= e.week_start && iso <= e.week_end) return e;
    return null;
  }

  function hide(id) { $(id).classList.add('hidden'); }
  function show(id) { $(id).classList.remove('hidden'); }

  function find() {
    hide('formError'); hide('result'); hide('rPlayer'); $('rPlayer').innerHTML = '';
    const year = +$('yearSel').value, month = +$('monthSel').value, day = +$('daySel').value;
    const dt = new Date(Date.UTC(year, month - 1, day));
    if (dt.getUTCMonth() !== month - 1) {
      $('formError').textContent = `${MONTHS[month - 1]} ${day}, ${year} isn't a real date. Please pick a valid day.`;
      show('formError');
      return;
    }
    const iso = dt.toISOString().slice(0, 10);
    const e = lookup(iso);
    if (!e) {
      $('formError').textContent = 'No chart found for that week. Please try another date.';
      show('formError');
      return;
    }
    current = e;
    $('rDate').textContent = `${MONTHS[month - 1]} ${day}, ${year}: Billboard Hot 100 dated ${fmt(e.week_start)}`;
    $('rTitle').textContent = e.title;
    $('rArtist').textContent = `by ${e.artist}`;
    const info = e.y1969 ? null : links.songs[`${e.title}|${e.artist}`];
    if (info) {
      const nth = rows.filter((r) => r.title === e.title && r.artist === e.artist && r.week_start <= e.week_start).length;
      $('rContext').textContent = `Week ${nth} of its ${info.weeks} week${info.weeks === 1 ? '' : 's'} at No. 1.`;
    } else {
      $('rContext').textContent = 'The last No. 1 of 1969, still on top for the first two days of 1970.';
    }
    const st = info && info.yt ? status[info.yt] : null;
    if (st && (st.embeddable === false || st.madeForKids === true)) info.yt = null;
    if (info && info.yt) { $('rPlay').dataset.yt = info.yt; show('rPlay'); } else { hide('rPlay'); }
    if (info && info.story) { $('rStory').href = info.story; show('rStory'); } else { hide('rStory'); }
    const dp = links.dates[`${month}-${day}`];
    if (dp) {
      $('rDatePage').href = dp;
      $('rDatePage').textContent = `Every 70s No. 1 on ${MONTHS[month - 1]} ${day}`;
      show('rDatePage');
    } else { hide('rDatePage'); }
    if (!(info && info.yt)) {
      $('rYouTube').href = youtubeSearchURL(`${e.title} ${e.artist}`);
      show('rYouTube');
    } else { hide('rYouTube'); }
    show('result');
  }

  function play() {
    const id = $('rPlay').dataset.yt;
    if (!id) return;
    const f = document.createElement('iframe');
    f.src = `https://www.youtube.com/embed/${encodeURIComponent(id)}?autoplay=1`;
    f.title = `${current.title} - ${current.artist}`;
    f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.allowFullscreen = true;
    $('rPlayer').innerHTML = '';
    $('rPlayer').appendChild(f);
    show('rPlayer');
    $('rPlayer').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  async function share() {
    if (!current) return;
    const btn = $('shareBtn');
    const text = `"${current.title}" by ${current.artist} was No. 1 the week I was born. Find yours at musicofthe70s.net`;
    const status = await shareOrCopy(
      { title: 'Music of the 70s', text, url: 'https://musicofthe70s.net/pages/birthday-number-one' }, text);
    btn.textContent = status === 'copied' ? 'Copied!' : status === 'shared' ? 'Shared' : status === 'failed' ? 'Copy failed' : btn.textContent;
    setTimeout(() => { btn.textContent = 'Copy & Share'; }, 1800);
  }

  (async function init() {
    try {
      [weekly, links] = await loadJSONMultiple(['/data/billboard/hot100_weekly.json', '/data/billboard/number-one-links.json']);
      try { const r = await fetch('/data/youtube-status.json'); if (r.ok) status = (await r.json()).videos || {}; } catch (e) { /* no status file: same rule as table-player.js */ }
      rows = Object.keys(weekly).sort().flatMap((y) => weekly[y]);
      populate();
      $('findBtn').addEventListener('click', find);
      $('rPlay').addEventListener('click', play);
      $('shareBtn').addEventListener('click', share);
      hide('loading'); show('tool');
    } catch (err) {
      console.error('Birthday finder failed to load data:', err);
      hide('loading');
      $('error').textContent = "Sorry, the chart data couldn't load right now. Please refresh the page to try again.";
      show('error');
    }
  })();
})();
