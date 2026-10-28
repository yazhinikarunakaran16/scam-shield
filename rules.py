import re

URGENT = ["urgent", "immediately", "blocked", "suspended", "expire",
          "expires", "expired", "final notice", "within 24 hours",
          "today", "tonight", "disconnected", "frozen", "deactivated"]
SENSITIVE = ["otp", "cvv", "pin", "password", "aadhaar", "aadhar"]
LURE = ["lottery", "prize", "won", "reward", "refund", "cashback", "free",
        "scholarship", "salary"]
BANK_KYC = ["kyc", "pan", "bank", "account", "atm", "upi", "netbanking"]
SHORT_LINKS = ["bit.ly", "tinyurl", "rb.gy", "cutt.ly", "goo.gl", "is.gd"]

# Tamil / Tanglish additions
TAMIL_THREAT = (r"(block|cut|close|freeze|suspend)\s+"
                r"(aaga|aagum|aagiduchu|aayiduchu|aagirukku)|udane|mani neram")
TAMIL_JOB = r"sambarikk|veetula irundhe"
SAFE_PHRASES = r"do not share|never share|don't share|share pann(aa|a)dheenga|yaaridamum|neenga illa-?na"
ASKS_TO_SEND = r"anuppunga|share pannunga"


def has_word(words, text):
    return [w for w in words if re.search(r"\b" + w + r"\b", text)]


def rule_features(msg):
    text = msg.lower()
    score = 0
    reasons = []

    has_link = False
    if any(s in text for s in SHORT_LINKS):
        score += 2
        has_link = True
        reasons.append("Shortened link")
    elif re.search(r"https?://|www\.", text):
        score += 1
        has_link = True
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

    if re.search(TAMIL_THREAT, text):
        score += 2
        reasons.append("Tamil/Tanglish urgency or threat words")

    if re.search(TAMIL_JOB, text):
        score += 2
        reasons.append("Tanglish work-from-home / earning offer")

    if (re.search(SAFE_PHRASES, text) and not has_link
            and not re.search(ASKS_TO_SEND, text)):
        score -= 2
        reasons.append("Has a genuine-message warning (e.g. do not share)")

    score = max(score, 0)
    return score, reasons