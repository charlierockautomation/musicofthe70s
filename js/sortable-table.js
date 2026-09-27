/* Sortable data tables: any <table class="sortable-table"> whose header
   cells hold <button data-col data-type="text|num">. A cell's data-sort
   attribute, when present, is the value sorted on (e.g. an ISO date).
   Clicking a column sorts ascending, clicking again flips it; aria-sort
   on the <th> tells screen readers the current order. */
(function () {
  function cellValue(row, col, type) {
    var cell = row.cells[col];
    var raw = cell.getAttribute('data-sort');
    if (raw === null) raw = cell.textContent.trim();
    return type === 'num' ? parseFloat(raw) || 0 : raw.toLowerCase().replace(/^the /, '');
  }

  function sortBy(table, th, col, type) {
    var dir = th.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
    // Numbers read best biggest-first on the first click.
    if (type === 'num' && !th.hasAttribute('aria-sort')) dir = 'descending';
    var tbody = table.tBodies[0];
    var rows = Array.prototype.slice.call(tbody.rows);
    rows.forEach(function (r, i) { r._pos = i; });
    rows.sort(function (a, b) {
      var x = cellValue(a, col, type), y = cellValue(b, col, type);
      var c = x < y ? -1 : x > y ? 1 : 0;
      if (dir === 'descending') c = -c;
      return c || a._pos - b._pos;
    });
    rows.forEach(function (r) { tbody.appendChild(r); });
    Array.prototype.forEach.call(table.tHead.rows[0].cells, function (h) { h.removeAttribute('aria-sort'); });
    th.setAttribute('aria-sort', dir);
  }

  Array.prototype.forEach.call(document.querySelectorAll('table.sortable-table'), function (table) {
    Array.prototype.forEach.call(table.querySelectorAll('thead button[data-col]'), function (btn) {
      btn.addEventListener('click', function () {
        sortBy(table, btn.parentNode, Number(btn.getAttribute('data-col')), btn.getAttribute('data-type'));
      });
    });
  });
})();
