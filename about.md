---
layout: default
title: About .Astronomy
description: What is .Astronomy? The conference series bringing together astronomers, developers, educators and science communicators since 2008.
---

<span class="section-label">// about</span>
# About .Astronomy

<p style="font-size:1.1rem; color:var(--text-muted); max-width:620px; margin-bottom:2.5rem;">A conference series that builds a dynamic community of scientists and educators, exploiting the potential of modern computing and the web in the era of data-driven astronomy.</p>

Rather than focusing on scientific questions, .Astronomy focuses on innovative use of the web to develop new research tools, and to communicate with a broad audience through online platforms and innovative engagement resources.

## What happens at .Astronomy?

Through talks, tutorials, unconferences and hack days, participants:

- Gain new coding or maker skills
- Learn about the latest data services and tools
- Learn how to communicate and collaborate more effectively using web platforms
- Broaden their views on what a career in astronomy can look like

## The Format

A typical .Astronomy event runs for 3-4 days:

- **Day 0** (optional): Tutorial day with introductory sessions on tools and technologies
- **Day 1**: Talks and lightning talks from participants
- **Day 2**: Hack Day, where participants collaborate on projects proposed at the meeting
- **Day 3**: Unconference sessions proposed and voted on by attendees

## History

.Astronomy was founded by Robert Simpson in 2008 at Cardiff University. What began as a small gathering of astronomers interested in the web has grown into a community of over 300 alumni spanning research, education, outreach, and industry.

The conference has been held across the globe: Cardiff, Leiden, Oxford, Heidelberg, Cambridge MA, Chicago, Sydney, Cape Town, Baltimore, Toronto, New York, and Madrid.

In 2017 we surveyed over 300 past participants: 90% came away with new ideas and inspiration, 67% said it impacted their day-to-day work. See the [Research page]({{ site.baseurl }}/research) for the full paper.

### Topics over time

How the themes of .Astronomy have shifted across 14 events. Hover or tap a line to highlight it.

<div class="trends-wrap">
  <div class="trends-legend" id="trends-legend"></div>
  <div class="trends-chart-outer">
    <canvas id="trends-canvas" height="300"></canvas>
  </div>
  <p class="trends-note">Scores derived from talk titles, speaker bios and hack descriptions across all event pages. Higher score = more prominent theme at that event.</p>
</div>

<script>
(function () {
  var BASE = document.querySelector('meta[name="site-baseurl"]').content;
  var COLORS = [
    '#ef4444','#f97316','#eab308','#84cc16','#22c55e',
    '#14b8a6','#06b6d4','#3b82f6','#6366f1','#a855f7',
    '#ec4899','#f472b6','#fb923c','#a3e635','#e879f9'
  ];

  fetch(BASE + '/assets/js/trends-data.json')
    .then(function(r) { return r.json(); })
    .then(function(data) { drawChart(data); })
    .catch(function(e) { console.error(e); });

  function drawChart(data) {
    var canvas = document.getElementById('trends-canvas');
    var legend = document.getElementById('trends-legend');
    if (!canvas) return;

    var events = data.events;
    var topics = data.topics;
    var W, H, PAD = { top: 16, right: 20, bottom: 40, left: 32 };

    var highlighted = null;

    function resize() {
      W = canvas.parentElement.clientWidth;
      H = 300;
      canvas.width = W * window.devicePixelRatio;
      canvas.height = H * window.devicePixelRatio;
      canvas.style.width = W + 'px';
      canvas.style.height = H + 'px';
      draw();
    }

    function draw() {
      var ctx = canvas.getContext('2d');
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      ctx.clearRect(0, 0, W, H);

      var isDark = document.documentElement.getAttribute('data-theme') !== 'light';
      var gridCol = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
      var labelCol = isDark ? 'rgba(200,200,220,0.5)' : 'rgba(60,60,90,0.55)';

      var chartW = W - PAD.left - PAD.right;
      var chartH = H - PAD.top - PAD.bottom;

      // Find max value
      var maxVal = 0;
      topics.forEach(function(t) { maxVal = Math.max(maxVal, Math.max.apply(null, t.data)); });
      maxVal = Math.ceil(maxVal / 10) * 10;

      var xStep = chartW / (events.length - 1);

      // Grid lines
      ctx.strokeStyle = gridCol;
      ctx.lineWidth = 1;
      for (var g = 0; g <= 4; g++) {
        var gy = PAD.top + chartH - (g / 4) * chartH;
        ctx.beginPath(); ctx.moveTo(PAD.left, gy); ctx.lineTo(PAD.left + chartW, gy); ctx.stroke();
      }

      // X axis labels (years)
      ctx.fillStyle = labelCol;
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      events.forEach(function(ev, i) {
        var x = PAD.left + i * xStep;
        ctx.fillText(String(ev.year).slice(2), x, H - PAD.bottom + 14);
      });

      // Draw lines
      topics.forEach(function(topic, ti) {
        var col = COLORS[ti % COLORS.length];
        var isHL = highlighted === ti;
        var alpha = highlighted === null ? 0.7 : (isHL ? 1.0 : 0.1);

        ctx.strokeStyle = col;
        ctx.globalAlpha = alpha;
        ctx.lineWidth = isHL ? 2.5 : 1.5;
        ctx.lineJoin = 'round';
        ctx.beginPath();

        topic.data.forEach(function(val, i) {
          var x = PAD.left + i * xStep;
          var y = PAD.top + chartH - (val / maxVal) * chartH;
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        });
        ctx.stroke();

        // Dots at data points when highlighted
        if (isHL) {
          topic.data.forEach(function(val, i) {
            if (val === 0) return;
            var x = PAD.left + i * xStep;
            var y = PAD.top + chartH - (val / maxVal) * chartH;
            ctx.beginPath();
            ctx.arc(x, y, 3.5, 0, Math.PI * 2);
            ctx.fillStyle = col;
            ctx.fill();
          });
        }

        ctx.globalAlpha = 1;
      });
    }

    // Build legend
    topics.forEach(function(topic, ti) {
      var col = COLORS[ti % COLORS.length];
      var btn = document.createElement('button');
      btn.className = 'trend-leg-btn';
      btn.style.setProperty('--tc', col);
      btn.textContent = topic.name;
      btn.addEventListener('mouseenter', function() { highlighted = ti; draw(); });
      btn.addEventListener('mouseleave', function() { highlighted = null; draw(); });
      btn.addEventListener('click', function() {
        highlighted = highlighted === ti ? null : ti;
        document.querySelectorAll('.trend-leg-btn').forEach(function(b, i) {
          b.classList.toggle('tl-active', highlighted === i);
        });
        draw();
      });
      legend.appendChild(btn);
    });

    // Redraw on theme change
    var themeObs = new MutationObserver(function() { draw(); });
    themeObs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    window.addEventListener('resize', function() { ctx = null; resize(); });
    resize();
  }
})();
</script>

---

## Help build this archive

This site is an open archive of the .Astronomy conference series. If you were there, you can help fill in the gaps.

<div class="contribute-grid">

<a href="https://github.com/dotastro/dotastrosite/issues/new?template=missing_content.md&title=Missing+content:+[event+name]&labels=content" target="_blank" rel="noopener" class="contribute-card">
<div class="contribute-card-label">01</div>
<div class="contribute-card-title">Add missing content</div>
<p class="contribute-card-desc">Missing talks, hacks, participants or agenda items from an event you attended? File an issue and we'll add them.</p>
<span class="btn btn-outline btn-sm">Open an issue on GitHub</span>
</a>

<a href="https://github.com/dotastro/dotastrosite/issues/new?template=new_hack.md&title=Hack:+[hack+name]&labels=hack,content" target="_blank" rel="noopener" class="contribute-card">
<div class="contribute-card-label">02</div>
<div class="contribute-card-title">Submit a hack</div>
<p class="contribute-card-desc">Built something at a .Astronomy hack day that isn't in the archive? Tell us about it.</p>
<span class="btn btn-outline btn-sm">Submit via GitHub</span>
</a>

<a href="https://github.com/dotastro/dotastrosite/issues/new?template=correction.md&title=Correction:+[brief+description]&labels=correction" target="_blank" rel="noopener" class="contribute-card">
<div class="contribute-card-label">03</div>
<div class="contribute-card-title">Fix something</div>
<p class="contribute-card-desc">Spotted a mistake, wrong date, misspelled name, or broken link? File a correction.</p>
<span class="btn btn-outline btn-sm">File a correction</span>
</a>

<a href="https://github.com/dotastro/dotastrosite/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener" class="contribute-card">
<div class="contribute-card-label">04</div>
<div class="contribute-card-title">Submit a pull request</div>
<p class="contribute-card-desc">Comfortable with GitHub? Edit the files directly and open a PR. See CONTRIBUTING.md for the repo structure.</p>
<span class="btn btn-outline btn-sm">Read CONTRIBUTING.md</span>
</a>

</div>

---

## Contact

- Community: [Join the .Astronomy Slack](https://dotastronomyteam.slack.com)
- GitHub: [github.com/dotastro](https://github.com/dotastro)
- Twitter: [@dotastronomy](https://twitter.com/dotastronomy)
- Foundation: [foundation@dotastronomy.com](mailto:foundation@dotastronomy.com)
- Brain Trust nominations: [braintrust@dotastronomy.com](mailto:braintrust@dotastronomy.com)

---

## Background images

This site uses images from space telescopes as background images, changing each visit.

<div class="bg-credit-widget">
  <div class="bg-credit-preview">
    <div class="bg-credit-preview-img"></div>
  </div>
  <div class="bg-credit-info">
    <div class="bg-credit-info-title" id="bg-credit-title">Cosmic Cliffs, Carina Nebula</div>
    <div class="bg-credit-info-instrument" id="bg-credit-instrument">James Webb Space Telescope (NIRCam)</div>
    <p class="bg-credit-info-credit">Credits: <span id="bg-credit-text">NASA, ESA, CSA, and STScI</span></p>
    <div class="bg-credit-actions">
      <a href="https://science.nasa.gov/mission/webb/multimedia/images/" id="bg-credit-link" target="_blank" rel="noopener" class="btn btn-outline btn-sm">View image source</a>
      <button id="bg-rotate-btn" class="btn btn-outline btn-sm">Next image</button>
      <span class="bg-count-label" id="bg-count"></span>
    </div>
  </div>
</div>
