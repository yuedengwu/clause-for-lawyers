#!/usr/bin/env python3
"""
build_brief.py — Render the "Daily Brief: US Privacy & AI Law" HTML from a content JSON.

Why a script instead of writing HTML by hand each time: the look of this brief (a
black-on-white print-newsletter style, the inline expand toggles, and the
jurisdiction-filtered compliance calendar) is fixed. Keeping the markup, CSS, and
JavaScript here means every edition comes out visually identical and the only thing
that changes run-to-run is the *content* you researched. The calendar's filter
checkboxes are generated from the deadline data, so the dropdown and the table rows
can never drift out of sync.

Usage:
    python build_brief.py content.json brief.html

See references/content_guide.md for the content.json schema and an example.
"""

import json
import sys
import html


# ---------------------------------------------------------------------------
# Static chrome: CSS and JS. Do not parameterize these — they are the fixed
# identity of the brief. (Kept as plain strings so CSS braces need no escaping.)
# ---------------------------------------------------------------------------

CSS = """
  :root{
    --ink:#111111;
    --rule:#111111;
    --hair:#cfcfcf;
    --bg:#ffffff;
    --serif:Georgia,"Times New Roman",serif;
    --sans:-apple-system,"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;
  }
  *{box-sizing:border-box;}
  html,body{background:var(--bg);}
  body{
    margin:0;color:var(--ink);
    font-family:var(--sans);
    font-size:15px;line-height:1.55;font-weight:400;
    -webkit-font-smoothing:antialiased;
  }
  a{color:var(--ink);}
  .wrap{max-width:820px;margin:0 auto;padding:40px 26px 72px;}

  .masthead{border-bottom:3px solid var(--rule);padding-bottom:16px;}
  .masthead h1{
    font-family:var(--serif);font-weight:700;font-size:46px;line-height:1;
    margin:0;letter-spacing:-0.5px;
  }
  .masthead .meta{
    font-family:var(--sans);font-size:12px;font-weight:700;
    text-transform:uppercase;letter-spacing:2px;margin-top:12px;
    display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;
  }
  .masthead .meta .reg{font-weight:400;letter-spacing:1.5px;}

  h2.sec{
    font-family:var(--serif);font-weight:700;font-size:24px;
    margin:46px 0 4px;padding-bottom:8px;border-bottom:1px solid var(--rule);
  }
  .sec-note{font-family:var(--sans);font-size:12px;font-weight:400;letter-spacing:0.3px;}

  .glance{margin-top:26px;border:1px solid var(--rule);padding:4px 22px 18px;}
  .glance .kicker{
    font-family:var(--sans);font-size:12px;font-weight:700;text-transform:uppercase;
    letter-spacing:2px;margin:16px 0 14px;
  }
  .glance .g-row{padding:13px 0;border-top:1px solid var(--hair);}
  .glance .g-row:first-of-type{border-top:none;}
  .glance .g-label{
    font-family:var(--sans);font-size:12px;font-weight:700;text-transform:uppercase;
    letter-spacing:1.2px;margin-bottom:4px;
  }
  .glance .g-body{font-size:15px;}

  .item{padding:20px 0;border-top:1px solid var(--hair);}
  .item:first-of-type{border-top:none;}
  .flags{
    font-family:var(--sans);font-size:11px;font-weight:700;
    text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px;
  }
  .flags .f{margin-right:14px;white-space:nowrap;}
  .item h3{
    font-family:var(--serif);font-weight:700;font-size:19px;line-height:1.3;
    margin:0 0 5px;
  }
  .item h3 a{text-decoration:none;}
  .item h3 a:hover{text-decoration:underline;}
  .pub{
    font-family:var(--sans);font-size:12px;font-weight:400;letter-spacing:0.3px;
    margin-bottom:6px;
  }
  .pub .src{font-weight:700;}
  .desc{margin:0;display:inline;}
  .desc-wrap{font-size:15px;}

  .exp{
    font-family:var(--sans);font-size:19px;font-weight:700;line-height:1;
    background:none;border:none;padding:0 0 0 6px;margin:0;cursor:pointer;
    color:var(--ink);vertical-align:baseline;
  }
  .exp:hover{text-decoration:underline;}
  .exp-body{
    display:none;margin-top:11px;padding:13px 16px;
    border-left:3px solid var(--ink);background:#f6f6f6;font-size:14px;
  }

  .empty-note{
    font-family:var(--sans);font-size:14px;font-style:italic;color:var(--ink);
    padding:14px 0;
  }

  .cal-bar{
    display:flex;align-items:center;justify-content:space-between;
    flex-wrap:wrap;gap:10px;margin:14px 0 12px;
  }
  .cal-window{font-family:var(--sans);font-size:12px;font-weight:400;letter-spacing:0.3px;}
  .filter{position:relative;font-family:var(--sans);}
  .filter-btn{
    font-family:var(--sans);font-size:12px;font-weight:700;text-transform:uppercase;
    letter-spacing:1px;background:#fff;border:1px solid var(--ink);
    padding:7px 12px;cursor:pointer;color:var(--ink);
  }
  .filter-panel{
    display:none;position:absolute;right:0;top:calc(100% + 4px);z-index:20;
    background:#fff;border:1px solid var(--ink);padding:10px 14px;min-width:210px;
  }
  .filter-panel.open{display:block;}
  .filter-panel .ph{
    font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;
    margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--hair);
  }
  .filter-panel label{
    display:flex;align-items:center;gap:8px;font-size:14px;padding:5px 0;cursor:pointer;
  }
  .filter-panel input{width:15px;height:15px;accent-color:#111;}
  .filter-actions{margin-top:8px;padding-top:8px;border-top:1px solid var(--hair);}
  .filter-actions button{
    font-family:var(--sans);font-size:11px;font-weight:700;text-transform:uppercase;
    letter-spacing:0.5px;background:none;border:none;cursor:pointer;color:var(--ink);
    text-decoration:underline;padding:0;margin-right:14px;
  }

  table.cal{width:100%;border-collapse:collapse;font-family:var(--sans);}
  table.cal th,table.cal td{
    text-align:left;vertical-align:top;padding:11px 12px 11px 0;
    border-bottom:1px solid var(--hair);font-size:13px;line-height:1.45;
  }
  table.cal th{
    font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;
    border-bottom:2px solid var(--ink);padding-top:0;
  }
  table.cal td.date{font-weight:700;white-space:nowrap;}
  table.cal td.juris{font-weight:700;white-space:nowrap;}
  table.cal a{font-weight:700;}
  .links a{display:block;margin-bottom:3px;white-space:nowrap;}
  .no-rows{font-family:var(--sans);font-size:13px;font-style:italic;padding:14px 0;display:none;}

  footer{
    margin-top:52px;padding-top:16px;border-top:3px solid var(--rule);
    font-family:var(--sans);font-size:12px;font-weight:400;line-height:1.6;color:var(--ink);
  }
  footer .legend{margin-bottom:8px;font-weight:700;letter-spacing:0.5px;}

  @media (max-width:640px){
    .masthead h1{font-size:36px;}
    table.cal th,table.cal td{font-size:12px;}
    .links a{white-space:normal;}
  }
"""

JS = """
  function tog(id, el){
    var d = document.getElementById(id);
    var open = d.style.display === 'block';
    d.style.display = open ? 'none' : 'block';
    el.textContent = open ? '[ + ]' : '[ – ]';
  }
  function toggleFilter(){
    document.getElementById('filterPanel').classList.toggle('open');
  }
  function setAll(state){
    document.querySelectorAll('.jbox').forEach(function(b){ b.checked = state; });
    filterRows();
  }
  function filterRows(){
    var on = {};
    document.querySelectorAll('.jbox').forEach(function(b){ if(b.checked) on[b.value] = true; });
    var anyVisible = false;
    document.querySelectorAll('#calBody tr').forEach(function(tr){
      var show = !!on[tr.getAttribute('data-juris')];
      tr.style.display = show ? '' : 'none';
      if(show) anyVisible = true;
    });
    var nr = document.getElementById('noRows');
    if(nr) nr.style.display = anyVisible ? 'none' : 'block';
  }
  document.addEventListener('click', function(e){
    var f = document.querySelector('.filter');
    if(f && !f.contains(e.target)){
      var p = document.getElementById('filterPanel');
      if(p) p.classList.remove('open');
    }
  });
"""


def esc(text):
    """HTML-escape any researched text before it goes into the page."""
    return html.escape(str(text if text is not None else ""), quote=True)


def render_links(items):
    """items: list of {label, url}. Returns stacked anchor tags."""
    out = []
    for it in items or []:
        out.append('<a href="{url}">{label}</a>'.format(
            url=esc(it.get("url", "#")), label=esc(it.get("label", "link"))))
    return "\n          ".join(out)


def render_flags(item):
    tags = item.get("tags", []) or []
    parts = []
    for t in tags:
        parts.append('<span class="f">[ {} ]</span>'.format(esc(t)))
    if item.get("must_read"):
        parts.append('<span class="f must">&#9733; Must read</span>')
    if not parts:
        return ""
    return '<div class="flags">' + "".join(parts) + "</div>"


def render_item(item, toggle_id):
    flags = render_flags(item)
    title = esc(item.get("title", "Untitled"))
    url = esc(item.get("url", "#"))
    pub = esc(item.get("publisher", ""))
    meta = item.get("meta", "")
    pub_line = '<span class="src">{}</span>'.format(pub) if pub else ""
    if meta:
        pub_line = pub_line + (" &middot; " if pub_line else "") + esc(meta)
    summary = esc(item.get("summary", ""))
    toggle = item.get("toggle", "")

    block = []
    block.append('  <div class="item">')
    if flags:
        block.append('    ' + flags)
    block.append('    <h3><a href="{url}">{title}</a></h3>'.format(url=url, title=title))
    if pub_line:
        block.append('    <div class="pub">{}</div>'.format(pub_line))
    block.append('    <div class="desc-wrap"><p class="desc">{summary}</p>'.format(summary=summary))
    if toggle:
        block.append('<button class="exp" onclick="tog(\'{tid}\',this)" aria-label="Expand details">[ + ]</button>'.format(tid=toggle_id))
        block.append('      <div class="exp-body" id="{tid}">{body}</div>'.format(tid=toggle_id, body=esc(toggle)))
    block.append('    </div>')
    block.append('  </div>')
    return "\n".join(block)


def render_section(heading, note, items, counter, empty_msg):
    out = []
    note_html = ' <span class="sec-note">&mdash; {}</span>'.format(esc(note)) if note else ""
    out.append('  <h2 class="sec">{h}{n}</h2>'.format(h=esc(heading), n=note_html))
    if not items:
        out.append('  <div class="empty-note">{}</div>'.format(esc(empty_msg)))
        return "\n".join(out), counter
    for item in items:
        counter += 1
        out.append(render_item(item, "t{}".format(counter)))
    return "\n".join(out), counter


def render_calendar(cal):
    deadlines = (cal or {}).get("deadlines", []) or []
    window = esc((cal or {}).get("window", ""))
    out = []
    out.append('  <h2 class="sec">Compliance calendar</h2>')

    if not deadlines:
        out.append('  <div class="cal-bar"><span class="cal-window">{w}</span></div>'.format(w=window))
        out.append('  <div class="empty-note">No new compliance deadlines fall within this window.</div>')
        return "\n".join(out)

    # Unique jurisdictions, in order of first appearance, drive the filter UI.
    jurisdictions = []
    for d in deadlines:
        j = d.get("jurisdiction", "")
        if j and j not in jurisdictions:
            jurisdictions.append(j)

    checks = []
    for j in jurisdictions:
        checks.append(
            '        <label><input type="checkbox" class="jbox" value="{j}" checked '
            'onchange="filterRows()"> {j}</label>'.format(j=esc(j)))
    checks_html = "\n".join(checks)

    out.append('  <div class="cal-bar">')
    out.append('    <span class="cal-window">{w}</span>'.format(w=window))
    out.append('    <div class="filter">')
    out.append('      <button class="filter-btn" id="filterBtn" onclick="toggleFilter()">Filter by jurisdiction &#9662;</button>')
    out.append('      <div class="filter-panel" id="filterPanel">')
    out.append('        <div class="ph">Show jurisdictions</div>')
    out.append(checks_html)
    out.append('        <div class="filter-actions">')
    out.append('          <button onclick="setAll(true)">Select all</button>')
    out.append('          <button onclick="setAll(false)">Clear</button>')
    out.append('        </div>')
    out.append('      </div>')
    out.append('    </div>')
    out.append('  </div>')

    out.append('  <table class="cal">')
    out.append('    <thead><tr>'
               '<th>Date</th><th>Jurisdiction</th><th>Who is impacted</th>'
               '<th>Action required</th><th>Statute / guidance</th><th>Analysis</th>'
               '</tr></thead>')
    out.append('    <tbody id="calBody">')
    for d in deadlines:
        out.append('      <tr data-juris="{j}">'.format(j=esc(d.get("jurisdiction", ""))))
        out.append('        <td class="date">{}</td>'.format(esc(d.get("date", ""))))
        out.append('        <td class="juris">{}</td>'.format(esc(d.get("jurisdiction", ""))))
        out.append('        <td>{}</td>'.format(esc(d.get("impacted", ""))))
        out.append('        <td>{}</td>'.format(esc(d.get("action", ""))))
        out.append('        <td class="links">{}</td>'.format(render_links(d.get("statute", []))))
        analysis = d.get("analysis")
        analysis_list = [analysis] if isinstance(analysis, dict) else (analysis or [])
        out.append('        <td class="links">{}</td>'.format(render_links(analysis_list)))
        out.append('      </tr>')
    out.append('    </tbody>')
    out.append('  </table>')
    out.append('  <div class="no-rows" id="noRows">No jurisdictions selected.</div>')
    return "\n".join(out)


def render_glance(g):
    g = g or {}
    rows = [
        ("What's new", g.get("whats_new", "")),
        ("Ongoing", g.get("ongoing", "")),
        ("On the horizon", g.get("on_the_horizon", "")),
    ]
    out = ['  <div class="glance">', '    <div class="kicker">At a glance</div>']
    for label, body in rows:
        out.append('    <div class="g-row">')
        out.append('      <div class="g-label">{}</div>'.format(esc(label)))
        out.append('      <div class="g-body">{}</div>'.format(esc(body)))
        out.append('    </div>')
    out.append('  </div>')
    return "\n".join(out)


def build(data):
    date_str = esc(data.get("date", ""))
    window_label = esc(data.get("window_label", ""))
    sections = data.get("sections", {}) or {}

    counter = 0
    state_html, counter = render_section(
        "State laws", "privacy & AI", sections.get("state_laws", []),
        counter, "No qualifying development this period.")
    enf_html, counter = render_section(
        "State enforcement actions & settlements", None, sections.get("enforcement", []),
        counter, "No qualifying enforcement action or settlement this period.")
    fed_html, counter = render_section(
        "Federal", None, sections.get("federal", []),
        counter, "No qualifying federal development this period.")

    footer_window = " Coverage window: {}.".format(data.get("window_label")) if window_label else ""

    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append("<title>Daily Brief — US Privacy &amp; AI Law — {}</title>".format(date_str))
    parts.append("<style>{}</style>".format(CSS))
    parts.append("</head>")
    parts.append("<body>")
    parts.append('<div class="wrap">')

    # Masthead
    parts.append('  <div class="masthead">')
    parts.append('    <h1>Daily Brief</h1>')
    parts.append('    <div class="meta">')
    parts.append('      <span>US Privacy &amp; AI Law &middot; For Counsel</span>')
    parts.append('      <span class="reg">{}</span>'.format(date_str))
    parts.append('    </div>')
    parts.append('  </div>')

    parts.append(render_glance(data.get("at_a_glance", {})))
    parts.append(render_calendar(data.get("calendar", {})))
    parts.append(state_html)
    parts.append(enf_html)
    parts.append(fed_html)

    parts.append('  <footer>')
    parts.append('    <div class="legend">[ Privacy ] &nbsp; [ AI ] &nbsp; &#9733; Must read</div>')
    parts.append('    Tags appear on State-law items; the star flags the edition\'s most important reading.'
                 '{win} Buckets with no qualifying development are noted rather than padded. This brief is an '
                 'awareness tool for counsel, not legal advice; confirm details against primary sources before '
                 'relying on them.'.format(win=footer_window))
    parts.append('  </footer>')

    parts.append('</div>')
    parts.append("<script>{}</script>".format(JS))
    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts)


def main():
    if len(sys.argv) != 3:
        print("Usage: python build_brief.py <content.json> <output.html>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    html_out = build(data)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Wrote {}".format(sys.argv[2]))


if __name__ == "__main__":
    main()
