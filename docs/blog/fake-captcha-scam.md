---
title: "Fake Captcha Scams: Spot a ClickFix Page"
titleTemplate: false
description: "A fake captcha scam tells you to press Windows+R or open Terminal and paste a command. How the ClickFix trick works and what to do if you ran it."
headline: "Fake captchas that ask you to run a command"
date: "2026-11-28"
keyword: "captcha scam"
faq: [{"q": "Is a captcha that asks me to press Windows+R real?", "a": "No. Real captchas never ask you to open the Run dialog, a terminal or PowerShell, or to paste a command. Close the page."}, {"q": "What does the fake captcha command do?", "a": "It downloads and runs malware, most often an information stealer that takes saved passwords, cookies and crypto wallets, according to Microsoft Threat Intelligence."}, {"q": "Can fake captchas infect a Mac?", "a": "Yes. Microsoft describes a campaign that gave Mac users a Terminal command which installed Atomic macOS Stealer."}]
---

# Fake captchas that ask you to run a command

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">A real captcha asks you to tick a box, pick images or type what you see. A fake one asks you to press a few keys, paste something and press Enter. That paste is a command the page copied to your clipboard, and running it installs malware. Microsoft calls the technique ClickFix.</p>

## How the trick works

Microsoft Threat Intelligence described it in [Think before you Click(Fix)](https://www.microsoft.com/en-us/security/blog/2025/08/21/think-before-you-clickfix-analyzing-the-clickfix-social-engineering-technique/) in August 2025:

1. A page shows what looks like a human verification step, often copying the look of Google reCAPTCHA or Cloudflare Turnstile.
2. When you click its button, the page silently copies a malicious command to your clipboard.
3. The instructions tell you to open the Windows **Run** dialog (<kbd>Windows</kbd> <kbd>R</kbd>), Windows Terminal or PowerShell, paste with <kbd>Ctrl</kbd> <kbd>V</kbd> and press <kbd>Enter</kbd>.
4. The command downloads and runs the real payload. Microsoft lists information stealers such as Lumma Stealer as the most common result, along with remote access tools and loaders.

Macs are targeted too. Microsoft describes a campaign that showed a fake captcha and, on macOS, gave a Terminal command that asked for the user's password and installed Atomic macOS Stealer, which takes browser cookies, passwords and crypto wallets.

## How to tell a fake captcha from a real one

| A real captcha | A fake captcha |
| --- | --- |
| A checkbox, an image grid, a slider or a text code inside the page | Steps that send you outside the browser |
| Never asks for key combinations | Tells you to press Windows+R or open Terminal or PowerShell |
| Never asks you to paste anything | Tells you to paste and press Enter |
| Finishes in the page | Says something like "verification step required" with numbered instructions |

The rule is simple: no website check needs you to run a command. If a page asks, close it.

## If you already ran it

1. **Disconnect from the internet** to cut the link to the attacker.
2. **Run a full scan** with your security software, such as Microsoft Defender on Windows.
3. **Change your passwords from another, clean device**, starting with email and banking, and sign out of other sessions. Stealers take saved passwords and browser cookies, so a new password matters more than a scan.
4. **Turn on two-step verification** where you have not already.
5. **Tell your IT team** if it was a work computer. Microsoft's guidance for organisations includes limiting the Run dialog and PowerShell for users who do not need them.

## Why it works

People are used to captchas, and they are used to following small steps to get past them. The scam borrows that habit. How a genuine check works is in [what is a captcha](/blog/what-is-a-captcha-challenge) and [what is reCAPTCHA](/blog/what-is-recaptcha).

## FAQ

### Is a captcha that asks me to press Windows+R real?

No. Real captchas never ask you to open the Run dialog, a terminal or PowerShell, or to paste a command. Close the page.

### What does the fake captcha command do?

It downloads and runs malware, most often an information stealer that takes saved passwords, cookies and crypto wallets, according to Microsoft Threat Intelligence.

### Can fake captchas infect a Mac?

Yes. Microsoft describes a campaign that gave Mac users a Terminal command which installed Atomic macOS Stealer.

## Related posts

- [What is a CAPTCHA challenge-response test?](/blog/what-is-a-captcha-challenge)
- [What reCAPTCHA is and how it decides](/blog/what-is-recaptcha)
- [recaptcha.net: why that domain shows up](/blog/what-is-recaptcha-net)
- [All posts](/blog/)
