import re

URGENT = ["urgent", "immediately", "blocked", "suspended", "expire",
          "expires", "expired", "final notice", "within 24 hours",
          "today", "tonight", "disconnected", "frozen", "deactivated"]
SENSITIVE = ["otp", "cvv", "pin", "password", "aadhaar", "aadhar"]
LURE = ["lottery", "prize", "won", "reward", "refund", "cashback", "free",
        "scholarship", "salary"]
BANK_KYC = ["kyc", "pan", "bank", "account", "atm", "upi", "netbanking"]
SHORT_LINKS = ["bit.ly", "tinyurl", "rb.gy", "cutt.ly", "goo.gl", "is.gd"]


def has_word(words, text):
    return [w for w in words if re.search(r"\b" + w + r"\b", text)]


def rule_features(msg):
    text = msg.lower()
    score = 0
    reasons = []

    if any(s in text for s in SHORT_LINKS):
        score += 2
        reasons.append("Shortened link")
    elif re.search(r"https?://|www\.", text):
        score += 1
        reasons.append("Contains a link")

    if re.search(r"\.(xyz|top|click|icu)\b", text):
        score += 1
        reasons.append("Suspicious website ending")

    if has_word(URGENT, text):
        score += 2
        reasons.append("Urgency / threat words")

    if has_word(SENSITIVE, text):
        score += 2
        reasons.append("Mentions OTP / PIN / Aadhaar")

    if has_word(LURE, text):
        score += 1
        reasons.append("Prize / refund / reward lure")

    if has_word(BANK_KYC, text):
        score += 1
        reasons.append("Bank / KYC words")

    return score, reasons