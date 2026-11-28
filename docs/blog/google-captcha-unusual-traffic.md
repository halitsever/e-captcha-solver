---
title: "Google Unusual Traffic Captcha: Why It Shows Up"
titleTemplate: false
description: "Why Google says it detected unusual traffic from your computer network, what causes the reCAPTCHA page (VPNs, shared networks, malware) and what to do about it."
headline: "Why Google shows an \"unusual traffic\" captcha"
date: "2026-11-28"
keyword: "google captcha unusual traffic"
faq: [{"q": "Is my Google account blocked?", "a": "No. The page is about the network address the searches come from, not your account. Signing in does not change it."}, {"q": "Why does it happen on my phone too?", "a": "Phones on the same Wi-Fi share the network's public address. On mobile data, many customers can share one address as well."}, {"q": "Does the unusual traffic page mean I have a virus?", "a": "Not necessarily. Shared VPNs and networks are more common causes. If it keeps happening on your own home network without a VPN, scan for malware."}]
---

# Why Google shows an "unusual traffic" captcha

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">Sometimes a Google search stops at a page that says "Our systems have detected unusual traffic from your computer network" and asks you to solve a reCAPTCHA. It is not a penalty on your account. Google is asking whether a person is behind the searches coming from your network.</p>

## What the message means

Google's help page for this message says it appears when a network you use, including a VPN, seems to be sending automated traffic to Google Search. The decision is about the network address the searches come from, not about you personally. In most cases the page shows a reCAPTCHA, and once you solve it, searching works again.

## Common causes

Google's [help page on unusual traffic](https://support.google.com/websearch/answer/86640) lists these:

- **A shared VPN.** Many people use the same VPN exit address. If any of them run automated searches, everyone on that address can get the captcha. Google mentions IPv6 tunnel services in the same breath.
- **A shared network.** At a school, office, café or dormitory, all devices often share one public address.
- **A shared internet provider.** Some providers put many customers behind the same public address.
- **Malware.** A program on your computer, or on another device on your network, may be sending searches in the background.

Tools and browser extensions that fetch search results automatically send automated traffic too. Google does not publish the exact rules it uses.

## What to do

1. **Solve the reCAPTCHA.** That is what the page is for, and it usually clears the block.
2. **No captcha shown?** Google says to check that your browser supports reCAPTCHA and that JavaScript is turned on. Blocked third-party scripts or strict privacy extensions can hide the widget.
3. **Turn off the VPN or proxy** and search again. If that fixes it, the VPN exit address is the cause. Your VPN provider may offer other servers.
4. **Scan for malware** if the page keeps appearing on your own home network.
5. **On a work or school network,** tell the network administrator. Google notes that once the automated searches stop, people on the network can search normally again.
6. **Still happening at home without a VPN?** Your provider may share your public address with others. Google suggests contacting the provider.

## How long does it last?

Google does not give a fixed time. Solving the captcha clears it for your browser. If automated traffic keeps coming from the same address, the page can come back.

## What not to do

Do not install "captcha solver" extensions or services to get past this page. They send your traffic, and sometimes your browsing data, through a third party, and automated querying of Google Search is what triggers the page in the first place. If you need search results in a program, use an official API.

## The captcha behind the page

The page is a standard reCAPTCHA challenge: a checkbox that may open an image task. It works on the [challenge-response](/blog/what-is-a-captcha-challenge) principle like every other captcha. Google issues a challenge, your browser returns a token, and Google's server checks it before it sends you back to your search.

## FAQ

### Is my Google account blocked?

No. The page is about the network address the searches come from, not your account. Signing in does not change it.

### Why does it happen on my phone too?

Phones on the same Wi-Fi share the network's public address. On mobile data, many customers can share one address as well.

### Does the unusual traffic page mean I have a virus?

Not necessarily. Shared VPNs and networks are more common causes. If it keeps happening on your own home network without a VPN, scan for malware.

## Related posts

- [What is a CAPTCHA challenge-response test?](/blog/what-is-a-captcha-challenge)
- [Math CAPTCHAs: how they work and where they fall short](/blog/mathematical-captcha)
- [What is a captcha code?](/blog/what-is-a-captcha-code)
- [All posts](/blog/)
