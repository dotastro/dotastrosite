---
layout: default
title: Hosting .Astronomy
description: Interested in hosting a future .Astronomy conference? Find out how.
---

<span class="section-label">// about</span>
# Hosting .Astronomy

People often contact us about wanting to host .Astronomy. Members of the Brain Trust actively support hosts as they prepare for events, and we try to run each event as a collaboration. Hosting .Astronomy is a significant demand on your time -- especially as the event draws near -- but it is a rewarding experience.

## What we look for in a host

A good .Astronomy host typically has:

- A venue that can accommodate 60-100 participants for talks, unconference sessions, and hack day work
- Local knowledge and connections to help with logistics, accommodation, and social events
- Energy and enthusiasm for the .Astronomy mission
- A team of local organisers willing to share the load

The Brain Trust will support you throughout the process: advising on format, helping with the programme, and drawing on experience from past events.

## Get in touch

If you are interested in hosting a future .Astronomy, please get in touch to start the conversation.

<button class="btn btn-primary" onclick="revealHostContact()">Contact us about hosting</button>
<p id="host-contact-reveal" style="display:none; margin-top:0.75rem"></p>

<script>
function revealHostContact() {
  var u = ['info', '@', 'dotastronomy', '.', 'com'].join('');
  var link = document.createElement('a');
  link.href = 'mailto:' + u + '?subject=' + encodeURIComponent('[.Astronomy Hosting Query]');
  link.textContent = u;
  var p = document.getElementById('host-contact-reveal');
  p.innerHTML = '';
  p.appendChild(document.createTextNode('Email: '));
  p.appendChild(link);
  p.style.display = 'block';
  document.querySelector('[onclick="revealHostContact()"]').textContent = 'Open email';
  document.querySelector('[onclick="revealHostContact()"]').onclick = function() { window.location.href = link.href; };
}
</script>
