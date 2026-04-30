---
layout: default
title: ".Astronomy, Live"
description: Live coverage of the current .Astronomy event.
---

<span class="section-label">// live</span>

<div class="live-header">
  <div class="live-badge"><span class="live-dot"></span> Live now</div>
  <h1 class="live-title">EVENT NAME, City, Country</h1>
  <div class="event-meta">
    <span>DATES</span>
    <span>VENUE</span>
  </div>
</div>

<div class="live-grid">

  <div class="live-main">

    <section class="live-section">
      <h2>Live blog</h2>
      <div class="liveblog">

        <!-- Add new entries at the TOP, newest first -->
        <!-- Copy and paste this block for each new entry:

        <div class="liveblog-entry">
          <div class="liveblog-time">HH:MM UTC</div>
          <div class="liveblog-body">
            <p>Your update here.</p>
          </div>
        </div>

        -->

        <div class="liveblog-empty">
          <p>Live blog entries will appear here during the event. Updates are posted in real time.</p>
        </div>

      </div>
    </section>

    <section class="live-section">
      <h2>Today's schedule</h2>
      <div class="live-schedule">
        <!-- Paste today's schedule here, e.g.:
        <div class="sched-item">
          <span class="sched-time">09:00</span>
          <span class="sched-title">Opening and welcome</span>
        </div>
        -->
        <p style="color:var(--text-muted)">Schedule to be added.</p>
      </div>
    </section>

  </div>

  <div class="live-sidebar">

    <div class="live-sidebar-card">
      <div class="live-sidebar-title">Join the conversation</div>
      <p>Follow along on social media using <strong>#dotastro</strong></p>
      <a href="https://dotastronomyteam.slack.com" target="_blank" rel="noopener" class="btn btn-outline btn-sm" style="margin-top:0.5rem">Open Slack</a>
    </div>

    <div class="live-sidebar-card">
      <div class="live-sidebar-title">This event</div>
      <ul class="live-links">
        <li><a href="../EVENTDIR/">Event page</a></li>
        <li><a href="../EVENTDIR/talks.html">Talks</a></li>
        <li><a href="../EVENTDIR/hacks.html">Hacks</a></li>
      </ul>
    </div>

    <div class="live-sidebar-card">
      <div class="live-sidebar-title">Hack proposals</div>
      <p style="font-size:0.85rem; color:var(--text-muted)">Add your hack idea during the event by filing a GitHub issue.</p>
      <a href="https://github.com/dotastro/dotastrosite/issues/new?template=new_hack.md" target="_blank" rel="noopener" class="btn btn-outline btn-sm" style="margin-top:0.5rem">Propose a hack</a>
    </div>

  </div>

</div>

---

<p class="archive-note">This is the live event page for BotAstro to manage during an active .Astronomy event. To activate: update the title, dates and venue above, add the correct event directory link in the sidebar, then add a link to this page from the nav in <code>_layouts/default.html</code>. Remove the nav link when the event ends and move content to the event archive page.</p>
