---
layout: default
title: Nominate Someone for .Astronomy
description: Know someone who would be great at .Astronomy? Tell us about them.
---

<span class="section-label">// community</span>
# Nominate Someone

Organising .Astronomy and making it a successful event relies a lot on our own experiences as organisers and word-of-mouth recommendations. To ensure we cast a wide net for future .Astronomy or hack day stars, we'd like to invite you to tell us who we should be inviting.

Do you have a friend or colleague who would benefit from attending .Astronomy? Someone who has awesome things to contribute? A top speaker you saw at another event who would be great for the .Astronomy community? Tell us about them below and we'll reach out.

<div class="form-card">

<form id="nominate-form" action="https://formspree.io/f/FORMSPREE_ID" method="POST" novalidate>

  <input type="hidden" name="_subject" value="[.Astronomy] New Nomination">
  <input type="hidden" name="_next" value="https://dotastro.github.io/dotastrosite/nominate/thanks/">

  <div class="form-group">
    <label for="your-name">Your name <span class="required">*</span></label>
    <input type="text" id="your-name" name="your_name" required placeholder="Your full name">
  </div>

  <div class="form-group">
    <label for="your-email">Your email <span class="required">*</span></label>
    <input type="email" id="your-email" name="your_email" required placeholder="you@example.com">
  </div>

  <div class="form-row">
    <div class="form-group">
      <label for="nom-name">Nominee's name <span class="required">*</span></label>
      <input type="text" id="nom-name" name="nominee_name" required placeholder="Full name">
    </div>
    <div class="form-group">
      <label for="nom-email">Nominee's email</label>
      <input type="email" id="nom-email" name="nominee_email" placeholder="If you have it">
    </div>
  </div>

  <div class="form-group">
    <label for="nom-twitter">Nominee's Twitter / social handle</label>
    <input type="text" id="nom-twitter" name="nominee_handle" placeholder="@handle">
  </div>

  <div class="form-group">
    <label for="nom-affiliation">Nominee's affiliation / institution</label>
    <input type="text" id="nom-affiliation" name="nominee_affiliation" placeholder="University, company, etc.">
  </div>

  <div class="form-group">
    <label for="nom-reason">Why should they come to .Astronomy? <span class="required">*</span></label>
    <textarea id="nom-reason" name="reason" required rows="5" placeholder="Tell us about them. What would they contribute? What would they get out of it?"></textarea>
  </div>

  <div class="form-group">
    <label for="nom-link">Link to their work, website, or talks</label>
    <input type="url" id="nom-link" name="nominee_link" placeholder="https://...">
  </div>

  <div class="form-group">
    <label for="nom-event">Which future event are you nominating them for?</label>
    <input type="text" id="nom-event" name="event" placeholder="e.g. .Astronomy 14, or any future event">
  </div>

  <!-- hCaptcha — enabled automatically by Formspree on paid plans, or use free hCaptcha widget -->
  <div class="h-captcha" data-sitekey="HCAPTCHA_SITE_KEY" style="margin-bottom:1.25rem"></div>
  <script src="https://js.hcaptcha.com/1/api.js" async defer></script>

  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Submit nomination</button>
    <span class="form-note">Submissions go to the .Astronomy Brain Trust at braintrust@dotastronomy.com</span>
  </div>

  <div id="form-success" class="form-message form-success" style="display:none">
    Thanks for your nomination! We'll review it and reach out if we'd like to follow up.
  </div>

  <div id="form-error" class="form-message form-error" style="display:none">
    Something went wrong. Please try again or email us directly at <a href="mailto:braintrust@dotastronomy.com">braintrust@dotastronomy.com</a>.
  </div>

</form>
</div>

<script>
(function() {
  var form = document.getElementById('nominate-form');
  if (!form) return;

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Sending...';

    var data = new FormData(form);

    fetch(form.action, {
      method: 'POST',
      body: data,
      headers: { 'Accept': 'application/json' }
    }).then(function(response) {
      if (response.ok) {
        form.reset();
        document.getElementById('form-success').style.display = 'block';
        document.getElementById('form-error').style.display = 'none';
        btn.style.display = 'none';
      } else {
        throw new Error('Network response was not ok');
      }
    }).catch(function() {
      document.getElementById('form-error').style.display = 'block';
      btn.disabled = false;
      btn.textContent = 'Submit nomination';
    });
  });
})();
</script>
