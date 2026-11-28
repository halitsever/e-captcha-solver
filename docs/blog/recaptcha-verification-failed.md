---
title: "reCAPTCHA Verification Failed: Causes and Fixes"
titleTemplate: false
description: "reCAPTCHA verification failed or captcha not working? The usual causes for visitors and for site owners, from expired tokens to blocked scripts, with fixes."
headline: "Why a captcha says verification failed"
date: "2026-11-28"
keyword: "recaptcha verification failed"
faq: [{"q": "Why does reCAPTCHA say verification failed?", "a": "Usually because the token expired (it lasts two minutes), was checked twice, or the site's keys are set up wrong. Blocked scripts or cookies in the browser can cause it too."}, {"q": "How long is a reCAPTCHA token valid?", "a": "Two minutes, and it can be verified only once, according to Google's reCAPTCHA documentation."}, {"q": "Why is the captcha not working in my browser?", "a": "An extension may be blocking it, cookies may be off, or a VPN may make the traffic look unusual. Try a private window without extensions."}]
---

# Why a captcha says verification failed

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">A captcha can fail in two places: in your browser, where the check runs, and on the website's server, where the result is checked with the captcha provider. The message verification failed usually comes from the second step. Here is what goes wrong in each, and what to try.</p>

## If you are the visitor

Work down the list and try the form again after each step:

1. **Submit faster.** A reCAPTCHA token is valid for two minutes and can be checked only once, according to Google's [verification docs](https://developers.google.com/recaptcha/docs/verify). If you ticked the box, then filled in a long form, the token may have expired. Tick it again just before you submit.
2. **Reload the page.** A page that has been open for hours, or one you came back to with the back button, may hold a stale token.
3. **Turn off extensions for the site.** Ad blockers, privacy tools and script blockers can stop the captcha from loading or from reporting back. Allow `google.com/recaptcha` and `recaptcha.net` for that site.
4. **Allow cookies.** Google's reCAPTCHA FAQ says it sets a necessary cookie for its risk analysis. Strict cookie settings can make the check fail or keep asking.
5. **Leave the VPN or proxy.** Shared addresses that many people or scripts use look unusual and lead to more challenges, as with Google's [unusual traffic page](/blog/google-captcha-unusual-traffic).
6. **Check the clock.** A computer clock that is far off can break secure connections to the captcha provider. Set the date and time to update automatically.
7. **Try another browser or a private window**, which starts without your extensions and cookies.

If none of this helps, the problem is probably on the site's side, and its support team is the right contact.

## If you run the site

The server sends the token to `https://www.google.com/recaptcha/api/siteverify` and reads `success` and `error-codes`. Google lists these error codes:

| Code | Meaning |
| --- | --- |
| `missing-input-secret` | The secret parameter is missing |
| `invalid-input-secret` | The secret parameter is invalid or malformed |
| `missing-input-response` | The response parameter is missing |
| `invalid-input-response` | The response parameter is invalid or malformed |
| `bad-request` | The request is invalid or malformed |
| `timeout-or-duplicate` | The response is no longer valid: too old, or used before |

The common real-world causes behind them:

- **The token is sent twice.** A retry, a double-click or a second check in another service makes the second call return `timeout-or-duplicate`.
- **The form is slow.** Long forms let the token expire. Run the check, or reset the widget with `grecaptcha.reset()`, close to submit.
- **Keys do not match.** The site key on the page and the secret on the server belong to different keys, or the domain is not on the key's list. Google's FAQ also covers "Localhost is not in the list of supported domains" and "Invalid site key".
- **Logging the wrong thing.** Log the error codes from Google's answer, not only "verification failed", so you can tell an expired token from a wrong secret.

Moving to another provider, such as Cloudflare Turnstile, changes the details but not the shape of the check; the [nest-cloudflare-turnstile site](https://projects.halit.org/nest-cloudflare-turnstile/blog/verify-captcha-server-side.html) explains server-side verification for NestJS.

## FAQ

### Why does reCAPTCHA say verification failed?

Usually because the token expired (it lasts two minutes), was checked twice, or the site's keys are set up wrong. Blocked scripts or cookies in the browser can cause it too.

### How long is a reCAPTCHA token valid?

Two minutes, and it can be verified only once, according to Google's reCAPTCHA documentation.

### Why is the captcha not working in my browser?

An extension may be blocking it, cookies may be off, or a VPN may make the traffic look unusual. Try a private window without extensions.

## Related posts

- [Why Google shows an "unusual traffic" captcha](/blog/google-captcha-unusual-traffic)
- [What reCAPTCHA is and how it decides](/blog/what-is-recaptcha)
- [recaptcha.net: why that domain shows up](/blog/what-is-recaptcha-net)
- [All posts](/blog/)
