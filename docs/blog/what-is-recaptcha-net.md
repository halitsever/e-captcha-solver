---
title: "What Is recaptcha.net? Google's reCAPTCHA Domain"
titleTemplate: false
description: "recaptcha.net is the domain Google offers for reCAPTCHA where google.com is blocked. Why it shows up in Screen Time, logs and blockers, and if it is safe."
headline: "recaptcha.net: why that domain shows up"
date: "2026-11-28"
keyword: "what is recaptcha.net"
faq: [{"q": "Is recaptcha.net a virus?", "a": "No. It is a domain Google provides for reCAPTCHA, listed in Google's reCAPTCHA FAQ for use where google.com is not reachable."}, {"q": "Why is recaptcha.net in my Screen Time?", "a": "A website you visited loaded reCAPTCHA from that domain in the background, for example on a login or checkout form."}, {"q": "Can I block recaptcha.net?", "a": "You can, but forms that use reCAPTCHA from that domain will then fail to load the check or refuse to submit."}]
---

# recaptcha.net: why that domain shows up

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">If you have spotted www.recaptcha.net in Screen Time, a router log, a firewall prompt or an ad blocker's list, it is the reCAPTCHA service loading from Google's second domain for it. A page you visited used reCAPTCHA and loaded it from there instead of from google.com.</p>

## What Google says

reCAPTCHA is normally loaded from `www.google.com/recaptcha/`. Google's [reCAPTCHA FAQ](https://developers.google.com/recaptcha/docs/faq) answers the question "Can I use reCAPTCHA globally?" with: use `www.recaptcha.net` in your code in circumstances when `www.google.com` is not accessible. The same scripts are served from both, so website owners who have visitors in places where google.com is blocked, or who simply prefer a separate domain, point their pages at recaptcha.net.

## Why you see it

- **Screen Time and parental controls.** Their website lists can include domains that pages load in the background. A shop or login page that uses reCAPTCHA makes the browser fetch recaptcha.net in the background, so it can appear in the list even though you never typed it.
- **Network and DNS logs.** Routers, Pi-hole and corporate firewalls record every domain requested, including scripts inside pages.
- **Ad and tracker blockers.** Some lists flag reCAPTCHA domains. Blocking them usually breaks the forms that rely on them: the checkbox does not load and the form refuses to submit.

## Is recaptcha.net safe?

The domain itself is Google's, as the reCAPTCHA documentation shows. What matters more is the page around it. Fake verification pages copy the reCAPTCHA look to trick people into running commands, and a real reCAPTCHA never asks you to open a Run dialog, a terminal, or to paste anything. [Fake captcha scams](/blog/fake-captcha-scam) shows what those look like.

## If a form will not load the check

1. Allow `www.recaptcha.net` and `www.google.com/recaptcha` in your blocker for that site, or pause the blocker.
2. Reload the page.
3. If it still fails after you tick the box, the site's own check may be at fault. See [reCAPTCHA verification failed](/blog/recaptcha-verification-failed).

What reCAPTCHA does once it loads is covered in [what is reCAPTCHA](/blog/what-is-recaptcha).

## FAQ

### Is recaptcha.net a virus?

No. It is a domain Google provides for reCAPTCHA, listed in Google's reCAPTCHA FAQ for use where google.com is not reachable.

### Why is recaptcha.net in my Screen Time?

A website you visited loaded reCAPTCHA from that domain in the background, for example on a login or checkout form.

### Can I block recaptcha.net?

You can, but forms that use reCAPTCHA from that domain will then fail to load the check or refuse to submit.

## Related posts

- [What reCAPTCHA is and how it decides](/blog/what-is-recaptcha)
- [Why a captcha says verification failed](/blog/recaptcha-verification-failed)
- [Fake captchas that ask you to run a command](/blog/fake-captcha-scam)
- [All posts](/blog/)
