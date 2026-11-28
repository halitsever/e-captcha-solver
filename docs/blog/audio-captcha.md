---
title: "Audio Captcha: How It Works and Who It Fails"
titleTemplate: false
description: "An audio captcha reads out letters or words to type instead of an image puzzle. How it works, why the W3C calls it a poor fit for many users, and options."
headline: "Audio captchas and accessibility"
date: "2026-11-28"
keyword: "audio captcha"
faq: [{"q": "What is an audio captcha?", "a": "A captcha that plays letters, digits or words over noise and asks you to type what you heard. It is the alternative to image and text captchas for people who cannot see them."}, {"q": "Are audio captchas accessible?", "a": "Only partly. The W3C notes they fail deaf-blind users, people without sound or in noisy places, non-English speakers and many users with cognitive disabilities."}, {"q": "Can bots solve audio captchas?", "a": "Yes. The W3C note cites a study with a 90% success rate against Google's audio reCAPTCHA."}]
---

# Audio captchas and accessibility

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">An audio captcha plays a short recording of letters, digits or words over background noise and asks you to type what you heard. It exists because image and text captchas lock out people who cannot see them. It solves that for some users and creates new problems for others.</p>

## How it works

The site generates a random answer, turns it into speech, adds noise or distortion so that speech recognition has a harder time, and plays it through a button next to the visual challenge. You type the answer, and the server compares it with the one it generated, the same [challenge-response](/blog/what-is-a-captcha-challenge) check that a [text captcha code](/blog/what-is-a-captcha-code) uses. reCAPTCHA's image challenge, for example, has a headphones button that switches to an audio task.

## Who it fails

The W3C's note [Inaccessibility of CAPTCHA](https://www.w3.org/TR/turingtest/) (a 2021 draft update by the Accessible Platform Architectures Working Group) lists the problems:

- **Deaf-blind users**, people without working sound, and anyone in a noisy place cannot use it.
- **Language.** Audio captchas are almost always in English, which the note says leaves non-English speakers behind.
- **Replay.** Few audio captchas have an easy, reliable way to play the clip again.
- **Cognitive load.** Remembering a string of distorted letters while typing them makes audio a poor choice for users with cognitive disabilities.

## It does not stop bots well either

The same note points out that robots can recognise spoken content too, and cites a University of Maryland study with a 90% success rate against Google's audio reCAPTCHA. The noise that is meant to stop speech recognition hurts human listeners just as much.

This mirrors what happened to text captchas. A small model can learn one style of distorted text, as the [CRNN in this repository](/guide/crnn) does for E-captcha images, and speech models do the same for distorted audio.

## What the W3C suggests instead

- **Offer several alternatives** whenever an interactive captcha is used, so nobody is left with only one way through.
- **Prefer non-interactive checks**, which the note says pose no accessibility challenges: risk scoring in the background, such as [reCAPTCHA v3](/blog/what-is-recaptcha), rate limits, and honeypot fields.
- **Use account-level checks** such as two-step or multi-device verification where a person really needs to be confirmed.

A [math captcha](/blog/mathematical-captcha) is sometimes suggested as an accessible option. It is readable by screen readers, but it adds a calculation, and it is just as easy for scripts.

## FAQ

### What is an audio captcha?

A captcha that plays letters, digits or words over noise and asks you to type what you heard. It is the alternative to image and text captchas for people who cannot see them.

### Are audio captchas accessible?

Only partly. The W3C notes they fail deaf-blind users, people without sound or in noisy places, non-English speakers and many users with cognitive disabilities.

### Can bots solve audio captchas?

Yes. The W3C note cites a study with a 90% success rate against Google's audio reCAPTCHA.

## Related posts

- [What is a CAPTCHA challenge-response test?](/blog/what-is-a-captcha-challenge)
- [Math CAPTCHAs: how they work and where they fall short](/blog/mathematical-captcha)
- [What reCAPTCHA is and how it decides](/blog/what-is-recaptcha)
- [All posts](/blog/)
