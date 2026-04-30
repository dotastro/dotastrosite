---
layout: default
title: The .Astronomy Foundation
description: The .Astronomy Foundation supports projects that use technology to advance the practice and communication of astronomy.
permalink: /foundation/
---

<span class="section-label">// foundation</span>
# The .Astronomy Foundation

<p style="font-size:1.05rem; color:var(--text); max-width:640px; margin-bottom:2.5rem;">A registered charitable trust, founded in 2019 to support not only the projects and collaborations that emerge from the .Astronomy conference series, but any work undertaken in that spirit -- wherever in the world it happens.</p>

## Our Purpose

"For the public benefit, the advancement of astronomy and related fields, in any part of the world, by people using technology to innovate the practice and communication of the subject, by facilitating and supporting work that has the potential to be transformative, interdisciplinary, or uniquely impactful, and the communication of such work in suitable venues."

This is the formal charitable object of The Dotastronomy Foundation, as set out in our <a href="https://docs.google.com/document/d/1FGJz6mdxrz3kI7U6fLn-Ybdvmz_FKqpTDVpLRYIqts8/edit" target="_blank" rel="noopener">Charitable Trust Deed</a> (signed 30 April 2019).

## What We Support

.Astronomy began as a way to encourage and facilitate new ideas in astronomy. We have always strived to be an open and inclusive environment for everyone to participate. We aim to encourage the innovative use of technology to further the practice and communication of astronomy around the world.

If you have a project that fits this mission, we want to hear from you.

<button class="btn btn-primary" onclick="revealFoundationContact()">Contact the Foundation</button>
<p id="foundation-contact-reveal" style="display:none; margin-top:0.75rem; font-family:var(--font-mono); font-size:0.8rem"></p>

<script>
function revealFoundationContact() {
  var u = ['foundation', '@', 'dotastronomy', '.', 'com'].join('');
  var link = document.createElement('a');
  link.href = 'mailto:' + u + '?subject=' + encodeURIComponent('[.Astronomy Foundation Enquiry]');
  link.textContent = u;
  var p = document.getElementById('foundation-contact-reveal');
  p.innerHTML = '';
  p.appendChild(document.createTextNode('Email: '));
  p.appendChild(link);
  p.style.display = 'block';
  document.querySelector('[onclick="revealFoundationContact()"]').textContent = 'Open email';
  document.querySelector('[onclick="revealFoundationContact()"]').onclick = function() { window.location.href = link.href; };
}
</script>

---

## Trustees

The Foundation is governed by three trustees, each bringing a distinct perspective to its work.

<div class="braintrust-grid" style="margin-top:1.5rem">

<div class="person-card" data-handle="orbitingfrog.bsky.social">
<div class="person-card-top">
<img class="person-avatar" src="https://cdn.bsky.app/img/avatar/plain/did:plc:az2aiwjbntp35xgkwtthznsm/bafkreihsqf7ajl3hnvfxalobyt6fd3fvwb5fu4453xgusmon5624jgnpla@jpeg" alt="Robert Simpson" loading="lazy">
<div>
<div class="person-name">Robert Simpson</div>
<div class="person-role">Chairperson</div>
<div class="person-handle"><a href="https://bsky.app/profile/orbitingfrog.bsky.social" target="_blank" rel="noopener">orbitingfrog.bsky.social</a></div>
</div>
</div>
<p class="person-bio">Rob founded .Astronomy in Cardiff in 2008 as a PhD student, and has been the driving force behind the series ever since. He has organised or co-organised more editions than anyone else, and is the keeper of the community's institutional memory. As Chairperson, he sets the direction for both the Foundation and the conference series.</p>
</div>

<div class="person-card" data-handle="sarahkendrew.bsky.social">
<div class="person-card-top">
<img class="person-avatar" src="https://cdn.bsky.app/img/avatar/plain/did:plc:tdhfbju5nml6p7goaye5iiqj/bafkreiaxo2xfee4vutmp7tkp67p4rnpuv3oe73npihpg4gtqoodfhnflfy@jpeg" alt="Sarah Kendrew" loading="lazy">
<div>
<div class="person-name">Sarah Kendrew</div>
<div class="person-role">Secretary</div>
<div class="person-handle"><a href="https://bsky.app/profile/sarahkendrew.bsky.social" target="_blank" rel="noopener">sarahkendrew.bsky.social</a></div>
</div>
</div>
<p class="person-bio">Sarah has helped run more .Astronomy events than anyone else, and is one of the most well-connected people in UK and European astronomy. As an instrument scientist on the James Webb Space Telescope at ESA and STScI, she brings both deep scientific credibility and an extraordinary network of researchers, communicators, and developers. She has been invaluable in finding scientific speakers and participants throughout the series, and serves as Secretary to the Foundation.</p>
</div>

<div class="person-card" data-handle="chrislintott.bsky.social">
<div class="person-card-top">
<img class="person-avatar" src="https://cdn.bsky.app/img/avatar/plain/did:plc:67bgg4j34njbopitm62cvddy/bafkreibbr2bl7ekp3ngvsko4khxyu73dcda2mfjobui35eu5ky57t5ljjq@jpeg" alt="Chris Lintott" loading="lazy">
<div>
<div class="person-name">Chris Lintott</div>
<div class="person-role">Treasurer</div>
<div class="person-handle"><a href="https://bsky.app/profile/chrislintott.bsky.social" target="_blank" rel="noopener">chrislintott.bsky.social</a></div>
</div>
</div>
<p class="person-bio">Professor of Astrophysics at Oxford University and lead of the Zooniverse citizen science group, Chris has been part of .Astronomy from the very beginning. His research on galaxy formation and his work building the world's largest citizen science platform make him a natural fit for the Foundation's mission. He serves as Treasurer.</p>
</div>

</div>

---

<p style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-dim)">The Dotastronomy Foundation is a charitable trust registered in England and Wales. Charitable Trust Deed signed 30 April 2019. <a href="https://docs.google.com/document/d/1FGJz6mdxrz3kI7U6fLn-Ybdvmz_FKqpTDVpLRYIqts8/edit" target="_blank" rel="noopener">Read the full deed.</a></p>
