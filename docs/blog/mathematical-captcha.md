---
title: "Math CAPTCHA: How It Works and Where It Falls Short"
titleTemplate: false
description: "How a mathematical captcha works, how to build one that is checked on the server, and why a sum like 3 + 4 stops simple bots but little else. Python example."
headline: "Math CAPTCHAs: how they work and where they fall short"
date: "2026-11-28"
keyword: "mathematical captcha"
faq: [{"q": "Is a math captcha secure?", "a": "It stops simple spam bots. It does not stop someone who targets your site, because the question is easy to read and there are very few possible answers."}, {"q": "Should the answer be checked in JavaScript?", "a": "No. The browser can be skipped entirely. Check the answer on the server and accept each challenge only once."}, {"q": "Are math captchas accessible?", "a": "A plain-text sum works with screen readers, but mental arithmetic is hard for some people, for example those with dyscalculia. Offer another way to complete the form."}]
---

# Math CAPTCHAs: how they work and where they fall short

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">A math captcha asks a simple sum, such as "What is 3 + 4?", before a form is accepted. It is common in WordPress and other form plugins because it is easy to add and easy for people. This page explains how one works, how to build it so it is checked properly, and what it does not protect against.</p>

## How a math captcha works

It is a [challenge-response test](/blog/what-is-a-captcha-challenge) like any other captcha:

1. The server picks two small numbers and an operator, usually addition, and works out the answer.
2. It shows the question, as text or drawn into an image, and keeps the answer where the browser cannot read it.
3. When the form comes back, the server compares the submitted number with the stored answer.

The question can be written in several ways: digits ("3 + 4"), words ("three plus four"), or an image of the sum with some noise. All three ask the same thing; they differ only in how hard the question is for a program to read.

## A server-checked math captcha in Python

The example below keeps no state per visitor. It signs the answer, an expiry time and a random nonce with HMAC, and sends the signature to the browser as a hidden form field. The browser cannot read the answer from the token, and the server can check it later without a session.

```python
import hashlib
import hmac
import secrets
import time

SECRET = secrets.token_bytes(32)  # load a fixed key from your config instead
USED = set()                      # use a shared store such as Redis with several workers


def sign(answer, expires, nonce):
    msg = f"{answer}:{expires}:{nonce}".encode()
    return hmac.new(SECRET, msg, hashlib.sha256).hexdigest()


def new_challenge():
    a, b = secrets.randbelow(9) + 1, secrets.randbelow(9) + 1
    expires, nonce = int(time.time()) + 300, secrets.token_hex(8)
    token = f"{expires}:{nonce}:{sign(a + b, expires, nonce)}"
    return f"What is {a} + {b}?", token


def check(answer, token):
    expires, nonce, sig = token.split(":")
    if int(expires) < time.time() or nonce in USED:
        return False
    USED.add(nonce)  # one attempt per challenge, right or wrong
    return hmac.compare_digest(sig, sign(answer.strip(), expires, nonce))
```

A few choices in it matter more than the maths:

- **The answer never reaches the browser.** A hidden field holding the answer itself, or a JavaScript check, is the most common mistake in home-made math captchas.
- **Each challenge works once.** The nonce goes into `USED` on the first attempt, right or wrong, so a correct answer cannot be replayed and a wrong one cannot be retried with the same token.
- **Challenges expire.** Five minutes is enough for a person filling in a form.
- **Constant-time comparison.** `hmac.compare_digest` avoids leaking the signature through timing.

## Where math captchas fall short

**The question is easy for a program to read.** If the sum is plain text in the HTML, a script reads "3 + 4" with one regular expression. Writing it in words only adds a lookup table. Drawing it as an image turns it into a text-recognition problem with a tiny alphabet: ten digits and a few operators. That is easier than the five-letter text this project's [CRNN model](/guide/crnn) was built for.

**The answer space is tiny.** With two numbers from 1 to 9 there are only 17 possible sums, from 2 to 18. A bot that guesses blindly is right about one time in seventeen. Without one-attempt challenges and rate limits, guessing alone gets through.

**It does not see behaviour.** Score-based captchas such as reCAPTCHA v3 and managed challenges such as Cloudflare Turnstile look at signals around the request. A math captcha only checks one number.

**It can be a barrier for some people.** Arithmetic under time pressure is hard for people with dyscalculia. A plain-text question at least works with screen readers; an image-only sum needs a text alternative.

## When a math captcha is enough

It suits low-value forms that mostly get drive-by spam: a contact form, a comment box, a newsletter signup. There it stops generic bots that fill in every form they find and never read the page. Pair it with a hidden honeypot field and a rate limit per IP address. For logins, signups and anything worth attacking on purpose, use a widget-based captcha whose token you verify on the server, as described in [what a captcha challenge is](/blog/what-is-a-captcha-challenge).

## FAQ

### Is a math captcha secure?

It stops simple spam bots. It does not stop someone who targets your site, because the question is easy to read and there are very few possible answers.

### Should the answer be checked in JavaScript?

No. The browser can be skipped entirely. Check the answer on the server and accept each challenge only once.

### Are math captchas accessible?

A plain-text sum works with screen readers, but mental arithmetic is hard for some people, for example those with dyscalculia. Offer another way to complete the form.

## Related posts

- [What is a CAPTCHA challenge-response test?](/blog/what-is-a-captcha-challenge)
- [What is a captcha code?](/blog/what-is-a-captcha-code)
- [How captcha OCR works, step by step](/blog/how-captcha-ocr-works)
- [All posts](/blog/)
