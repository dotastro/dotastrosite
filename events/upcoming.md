---
layout: default
title: Upcoming Events
description: Future .Astronomy conferences.
---

<span class="section-label">// upcoming</span>
# Upcoming Events

<div class="upcoming-grid">

<div class="upcoming-card">
  <div class="upcoming-status">
    <span class="status-pill planned">Planned</span>
  </div>
  <div class="upcoming-num">.Astronomy 14</div>
  <h2 class="upcoming-title">London, UK</h2>
  <div class="upcoming-meta">
    <span>2027</span>
    <span>London, United Kingdom</span>
  </div>
  <p class="upcoming-desc">The fourteenth .Astronomy conference will be held in London. Dates and venue are yet to be confirmed. The event will be organised by Robert Simpson.</p>
  <p class="upcoming-desc">If you would like to help organise, suggest a venue, or get involved early, please get in touch.</p>
  <button class="btn btn-primary" id="contact-btn" onclick="revealContact()">Get in touch to help organise</button>
  <p class="upcoming-contact-note" id="contact-reveal" style="display:none"></p>
</div>

</div>

<div class="upcoming-none" style="margin-top:3rem">
  <p>Know of another upcoming .Astronomy event? <a href="https://github.com/dotastro/dotastrosite/issues/new?title=Upcoming+event&body=Please+add+this+upcoming+event+to+the+site">File an issue on GitHub</a> and we'll add it here.</p>
</div>

<script>
function revealContact() {
  // Email assembled client-side -- never in the HTML source
  var u = ['robert', '.', 'simpson', '@', 'dotastronomy', '.', 'com'].join('');
  var s = '.Astronomy 14 London';
  var link = document.createElement('a');
  link.href = 'mailto:' + u + '?subject=' + encodeURIComponent(s);
  link.textContent = u;
  link.style.fontFamily = 'var(--font-mono)';
  link.style.fontSize = '0.78rem';
  link.style.color = 'var(--blue)';

  var reveal = document.getElementById('contact-reveal');
  reveal.innerHTML = '';
  reveal.appendChild(document.createTextNode('Email: '));
  reveal.appendChild(link);
  reveal.style.display = 'block';

  // Replace button with a direct mailto link
  var btn = document.getElementById('contact-btn');
  btn.onclick = function() { window.location.href = link.href; };
  btn.textContent = 'Open email';
}
</script>
