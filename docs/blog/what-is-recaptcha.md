---
title: "What Is reCAPTCHA? Google's Bot Check Explained"
titleTemplate: false
description: "reCAPTCHA is Google's service that tells people from bots on websites. How the v2 checkbox, invisible v2 and score-based v3 work, and what the site sees."
headline: "What reCAPTCHA is and how it decides"
date: "2026-11-28"
keyword: "what is recaptcha"
faq: [{"q": "Is reCAPTCHA made by Google?", "a": "Yes. reCAPTCHA is a Google service that websites add to forms and pages to tell people from bots."}, {"q": "What does reCAPTCHA v3 do?", "a": "It checks requests without any puzzle and gives each one a score from 0.0 (very likely a bot) to 1.0 (very likely a person). The website decides what to do with the score."}, {"q": "Does reCAPTCHA use cookies?", "a": "Google's reCAPTCHA FAQ says it sets a necessary cookie, _GRECAPTCHA, for its risk analysis."}]
---

# What reCAPTCHA is and how it decides

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">reCAPTCHA is Google's captcha service. A website adds it to a form or a page, and reCAPTCHA decides whether the visitor is likely a person or a script, sometimes with a puzzle and often without one. It is the box that says I'm not a robot, and the small badge in the corner of many sites.</p>

## The versions you meet as a visitor

Google's developer docs describe these types:

| Type | What you see | How it decides |
| --- | --- | --- |
| v2 "I'm not a robot" checkbox | A checkbox | Passes you at once or opens a challenge, such as picking images |
| v2 invisible | Usually nothing, a badge at most | Only the most suspicious traffic is asked to solve a challenge, by default |
| v3 | Nothing | Returns a score for each request, with no user interaction |

For v3, Google says the score runs from 0.0 to 1.0, where 1.0 is very likely a good interaction and 0.0 is very likely a bot, and that a site can start with a threshold of 0.5. The site decides what to do with a low score: block the request, ask for a second check, or just log it. More types exist in Google Cloud under the reCAPTCHA name.

## What happens behind the checkbox

1. The page loads reCAPTCHA's script from Google, which runs its risk analysis in your browser. Google's [reCAPTCHA FAQ](https://developers.google.com/recaptcha/docs/faq) says it sets a necessary cookie, `_GRECAPTCHA`, for that purpose.
2. When you pass, the browser gets a token, a long string, and the form sends it along with your data.
3. The website's server sends the token and a secret key to Google's `siteverify` endpoint and gets back `success`, the time of the challenge and the host name.
4. Each token is valid for two minutes and can be verified only once, according to Google's [verification docs](https://developers.google.com/recaptcha/docs/verify).

That last step is where many failures come from. [reCAPTCHA verification failed](/blog/recaptcha-verification-failed) explains the usual causes.

## How it relates to other captchas

reCAPTCHA is one implementation of the [challenge-response idea](/blog/what-is-a-captcha-challenge) behind every captcha. Older captchas showed [distorted text codes](/blog/what-is-a-captcha-code); reCAPTCHA moved first to image tasks and then to scoring behaviour in the background. Text captchas are within reach of small OCR models, and the model in this repository is an example: a small CRNN that reads one text captcha style, E-captcha. It is not built for reCAPTCHA and does not solve image or score-based checks.

## When reCAPTCHA keeps asking

Repeated challenges usually mean the request looks unusual to Google's analysis: a shared network or VPN, blocked cookies, or traffic that resembles automation. [Why Google shows an unusual traffic captcha](/blog/google-captcha-unusual-traffic) covers the Google Search version of this.

## FAQ

### Is reCAPTCHA made by Google?

Yes. reCAPTCHA is a Google service that websites add to forms and pages to tell people from bots.

### What does reCAPTCHA v3 do?

It checks requests without any puzzle and gives each one a score from 0.0 (very likely a bot) to 1.0 (very likely a person). The website decides what to do with the score.

### Does reCAPTCHA use cookies?

Google's reCAPTCHA FAQ says it sets a necessary cookie, _GRECAPTCHA, for its risk analysis.

## Related posts

- [What is a CAPTCHA challenge-response test?](/blog/what-is-a-captcha-challenge)
- [recaptcha.net: why that domain shows up](/blog/what-is-recaptcha-net)
- [Why a captcha says verification failed](/blog/recaptcha-verification-failed)
- [All posts](/blog/)
