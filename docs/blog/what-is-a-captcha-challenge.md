---
title: "What Is a CAPTCHA? The Challenge-Response Test Explained"
titleTemplate: false
description: "What a CAPTCHA challenge-response test is, how the server checks the answer, the main kinds of captcha in use today and why text captchas are easy for OCR."
headline: "What is a CAPTCHA challenge-response test?"
date: "2026-11-28"
keyword: "what is a captcha challenge response"
hreflang: {"en": "blog/what-is-a-captcha-challenge", "tr": "blog/captcha-ne-demek", "x-default": "blog/what-is-a-captcha-challenge"}
faq: [{"q": "Is a CAPTCHA the same as reCAPTCHA?", "a": "No. CAPTCHA is the general idea. reCAPTCHA is Google's captcha service, one product among several, alongside hCaptcha and Cloudflare Turnstile."}, {"q": "Why do I get a captcha when I have done nothing wrong?", "a": "The site or its provider decided your request looked unusual, for example because many requests came from the same network or VPN. Solving it once usually clears it."}, {"q": "Can a captcha be checked only in the browser?", "a": "It can be written that way, but then a script can submit the form without it. The answer or token must be verified on the server."}]
---

# What is a CAPTCHA challenge-response test?

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">A CAPTCHA is a small test a website gives you to check that a person, not a script, is sending the request. It works as a challenge and a response: the site sets a task, you answer it, and the site checks the answer before it lets the request through.</p>

## What the letters stand for

CAPTCHA is short for "Completely Automated Public Turing test to tell Computers and Humans Apart". The name comes from a 2003 paper by Luis von Ahn, Manuel Blum, Nicholas Hopper and John Langford at Carnegie Mellon University. "Turing test" points at the idea behind it: a test that people pass easily and programs do not. "Completely automated" means a computer, not a person, makes the test and grades it.

## How the challenge and the response work

Every captcha, from a distorted word to an invisible score, follows the same three steps:

1. **Challenge.** The server creates a task and keeps the expected answer to itself, either in the session or signed inside a token. The browser only gets the task: an image, a question, a widget.
2. **Response.** You solve the task. The browser sends your answer, or a token the captcha widget issued, along with the form.
3. **Verification.** The server compares the response with what it expected. If they match, and the challenge has not expired or been used already, the request goes through.

The checking has to happen on the server. A captcha that only checks the answer in the browser can be skipped by sending the form without it. Single-use challenges and short expiry times stop the same correct answer from being replayed.

## The kinds of captcha you see today

| Kind | What you do | Example |
| --- | --- | --- |
| Text captcha | Type the distorted letters or digits in an image | Older login and signup forms, government sites |
| Math captcha | Answer a sum such as "3 + 4" | WordPress and form plugins |
| Image selection | Click every tile that shows a bus or a crosswalk | reCAPTCHA v2 image challenges |
| Checkbox | Tick "I'm not a robot" and only get a puzzle if the widget is unsure | reCAPTCHA v2, hCaptcha |
| Invisible or score based | Nothing; the site gets a risk score from your behaviour | reCAPTCHA v3, which returns a score from 0.0 to 1.0 |
| Managed challenge | Usually nothing; the browser runs checks in the background | Cloudflare Turnstile |
| Audio | Type the words or digits you hear | The accessible fallback of most image captchas |

The newer kinds moved the test away from the image. reCAPTCHA v3 and Turnstile look at signals from the browser and the request rather than asking you to read anything. Their responses are tokens the site must verify with the provider's API on its own server. For a worked example of that server-side check, see [Cloudflare Turnstile in NestJS](https://www.halit.org/posts/cloudflare-turnstile-nestjs).

## Why plain text captchas are weak

A text captcha bets that reading warped letters is hard for a computer. That bet stopped holding once neural networks became the normal tool for reading text. A text captcha from one site usually has a fixed style: the same fonts, the same length, the same alphabet and the same kind of noise. A model trained on a few thousand labelled examples of that one style learns it.

This project is a small, concrete case. The model in this repository reads [E-captcha](/) images: five letters from a 19-letter alphabet on a 200 x 50 grayscale image. It is a [CRNN](/guide/crnn) with five convolutional blocks and a two-layer bidirectional LSTM, trained with [CTC loss](/guide/ctc-loss). The README reports about 95% accuracy on E-captcha. That number holds for that one captcha style only, and the model reads nothing else, but it shows how little it takes. The [synthetic data generator](/blog/what-is-a-captcha-code) in the repo produces unlimited training images in the same style.

So a text captcha slows down casual scripts and does little against anyone willing to label a few thousand images. Sites that need more use the widget-based kinds above, rate limits and server-side checks together.

## What "challenge response" means on a captcha page

Some sites write "Please complete the challenge" or "Verify you are human" above the widget. That wording is the challenge step. If the page keeps coming back after you answer, the response is probably being rejected on the server: the token expired, cookies are blocked, or the network you are on looks automated to the provider. Google's version of that last case is explained in [why Google shows "unusual traffic" captchas](/blog/google-captcha-unusual-traffic).

## FAQ

### Is a CAPTCHA the same as reCAPTCHA?

No. CAPTCHA is the general idea. reCAPTCHA is Google's captcha service, one product among several, alongside hCaptcha and Cloudflare Turnstile.

### Why do I get a captcha when I have done nothing wrong?

The site or its provider decided your request looked unusual, for example because many requests came from the same network or VPN. Solving it once usually clears it.

### Can a captcha be checked only in the browser?

It can be written that way, but then a script can submit the form without it. The answer or token must be verified on the server.

## Related posts

- [Math CAPTCHAs: how they work and where they fall short](/blog/mathematical-captcha)
- [Why Google shows an "unusual traffic" captcha](/blog/google-captcha-unusual-traffic)
- [What is a captcha code?](/blog/what-is-a-captcha-code)
- [All posts](/blog/)
