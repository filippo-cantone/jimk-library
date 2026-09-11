/* Jim K library — client-side search + shelf filters. Zero dependencies. */
(function () {
  "use strict";
  var DATA = null;

  function el(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function norm(s) { return String(s == null ? "" : s).toLowerCase(); }

  function chips(n) {
    var out = [];
    if (n.s) out.push('<span class="chip">' + esc(n.s) + "</span>");
    if (n.k) out.push('<span class="chip">' + esc(n.k) + "</span>");
    if (n.g) out.push('<span class="chip">' + esc(n.g) + "</span>");
    if (n.y) out.push('<span class="chip">' + esc(n.y) + "</span>");
    return out.join("");
  }

  function score(n, q) {
    // title-weighted substring match across title + excerpt + tags
    var t = norm(n.t), x = norm(n.x || ""),
      tr = norm((n.tr || []).join(" ")), g = norm(n.g || "");
    var s = 0, i = t.indexOf(q);
    if (i === 0) s += 60; else if (i > 0) s += 40;
    if (x.indexOf(q) >= 0) s += 12;
    if (tr.indexOf(q) >= 0) s += 15;
    if (g.indexOf(q) >= 0) s += 10;
    return s;
  }

  function passFilters(n, f) {
    if (f.shelf && n.shelf !== f.shelf) return false;
    if (f.kind && n.k !== f.kind) return false;
    if (f.genre && norm(n.g) !== f.genre) return false;
    if (f.year && !(n.y || "").split(",").map(function (v) { return v.trim(); }).includes(f.year)) return false;
    return true;
  }

  function readFilters(scope) {
    return {
      shelf: scope ? null : (el("f-shelf") ? el("f-shelf").value : ""),
      kind: el("f-kind") ? el("f-kind").value : "",
      genre: el("f-genre") ? el("f-genre").value : "",
      year: el("f-year") ? el("f-year").value : ""
    };
  }

  function renderList(box, items, emptyMsg) {
    if (!items.length) {
      box.innerHTML = '<li class="hint">' + esc(emptyMsg) + "</li>";
      return;
    }
    box.innerHTML = items.map(function (n) {
      return '<li><a class="t" href="' + esc(n.u) + '">' + esc(n.t) + "</a>" +
        '<div class="meta">' + chips(n) + "</div></li>";
    }).join("");
  }

  // ---- home search ----
  function runHomeSearch() {
    var box = el("results"), q = el("q");
    if (!box || !q) return;
    var query = norm(q.value.trim());
    var count = el("count");
    if (query.length < 2) {
      box.innerHTML = "";
      if (count) count.textContent = "";
      return;
    }
    var f = readFilters(false);
    var hits = [];
    for (var i = 0; i < DATA.length; i++) {
      var n = DATA[i];
      if (!passFilters(n, f)) continue;
      var s = score(n, query);
      if (s > 0) hits.push([s, n]);
    }
    hits.sort(function (a, b) { return b[0] - a[0]; });
    var top = hits.slice(0, 60).map(function (h) { return h[1]; });
    renderList(box, top, "No matches — try fewer words, or clear the filters.");
    if (count) count.textContent = top.length + (top.length === 60 ? "+" : "") + " match" + (top.length === 1 ? "" : "es");
  }

  // ---- shelf page: text filter + kind filter over embedded list ----
  function runShelfFilter() {
    var box = el("shelf-results"), q = el("q2");
    if (!box || !window.SHELF_NOTES) return;
    var query = norm(q ? q.value.trim() : "");
    var kind = el("f-kind") ? el("f-kind").value : "";
    var items = window.SHELF_NOTES.filter(function (n) {
      if (kind && n.k !== kind) return false;
      if (query.length >= 2 && score(n, query) === 0) return false;
      return true;
    });
    if (query.length >= 2) {
      items = items.map(function (n) { return [score(n, query), n]; })
        .sort(function (a, b) { return b[0] - a[0]; }).map(function (h) { return h[1]; });
    }
    renderList(box, items.slice(0, 200), "Nothing on this shelf matches.");
  }

  function fillFilterOptions() {
    // populate genre/year dropdowns from DATA on the home page
    var gs = el("f-genre"), ys = el("f-year");
    if (!DATA || (!gs && !ys)) return;
    var genres = {}, years = {};
    DATA.forEach(function (n) {
      if (n.g) genres[n.g] = 1;
      (n.y || "").split(",").forEach(function (v) { v = v.trim(); if (v) years[v] = 1; });
    });
    if (gs && gs.options.length <= 1) {
      Object.keys(genres).sort().forEach(function (g) {
        var o = document.createElement("option"); o.value = g.toLowerCase(); o.textContent = g;
        gs.appendChild(o);
      });
    }
    if (ys && ys.options.length <= 1) {
      Object.keys(years).sort().forEach(function (y) {
        var o = document.createElement("option"); o.value = y; o.textContent = "Year " + y;
        ys.appendChild(o);
      });
    }
  }

  function bind() {
    var q = el("q");
    if (q) {
      q.addEventListener("input", runHomeSearch);
      ["f-shelf", "f-kind", "f-genre", "f-year"].forEach(function (id) {
        var s = el(id);
        if (s) s.addEventListener("change", runHomeSearch);
      });
    }
    var q2 = el("q2");
    if (q2) {
      q2.addEventListener("input", runShelfFilter);
      var fk = el("f-kind");
      if (fk) fk.addEventListener("change", runShelfFilter);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    fetch("search.json").then(function (r) { return r.json(); }).then(function (d) {
      DATA = d;
      fillFilterOptions();
      bind();
      runHomeSearch();
    }).catch(function () {
      // search.json sits next to shelf pages too — try one level up
      fetch("../search.json").then(function (r) { return r.json(); }).then(function (d) {
        DATA = d;
        fillFilterOptions();
        bind();
        runShelfFilter();
      }).catch(function () { bind(); });
    });
    // shelf pages embed their list inline; work even if fetch fails
    if (window.SHELF_NOTES) bind();
  });
})();
