# Scam Message Shield

A tool that checks whether an SMS or WhatsApp message looks like a scam and explains why, built for Indian-style scams (fake KYC, parcel fees, job offers, prize lotteries).

## How it works
1. **ML model:** TF-IDF + Logistic Regression, trained on the UCI SMS Spam Collection plus 60 hand-written Indian-style messages.
2. **Rules:** signals such as shortened links, urgency/threat words, OTP/PIN requests, fee requests and too-good-to-be-true job offers.
3. **Hybrid score:** average of the ML probability and the rule score, shown as HIGH RISK, SUSPICIOUS or LIKELY SAFE.
4. **Explanation:** the rule signals are shown to the user. An optional LLM step (Llama API) can turn them into a plain-language explanation.

## Results
The model trained on the English UCI dataset alone reached only 0.25 scam recall on 40 Indian-style messages. After adding Indian-style training messages:

| Test set | Method | Scam precision | Scam recall | Accuracy |
|---|---|---|---|---|
| Dev set (40 messages, used while building) | ML only | 0.83 | 0.95 | 0.88 |
| Dev set | Rules only | 0.85 | 0.85 | 0.85 |
| Dev set | Hybrid | 0.90 | 0.95 | 0.93 |
| Fresh set (30 messages, not used for tuning) | ML only | 0.71 | 1.00 | 0.80 |
| Fresh set | Rules only | 0.80 | 0.80 | 0.80 |
| Fresh set | Hybrid | 0.87 | 0.87 | 0.87 |

Original English-only baseline on the UCI hold-out set (1,115 messages): scam precision 0.90, recall 0.93.
### Tanglish (Tamil written in English letters) results
I added Tanglish rules (threat words, work-from-home offers, genuine-message warnings such as "do not share"). Hybrid accuracy:

| Test set | Messages | ML only | Rules only | Hybrid |
|---|---|---|---|---|
| Tanglish dev set (rules were tuned on its errors) | 30 | 0.90 | 0.93 | 0.97 |
| Tanglish holdout (not used to tune, same author) | 20 | 0.75 | 0.75 | 0.85 |
| English fresh set, re-run after rule changes (no longer a clean test) | 30 | 0.80 | 0.83 | 0.90 |

Before the Tanglish rules, hybrid accuracy was 0.87 (Tanglish dev), 0.75 (Tanglish holdout) and 0.87 (English fresh).

## Limitations
- Tanglish is supported only in Roman letters, not Tamil script.
- Both Tanglish test sets and the rules were written by the same person, so the holdout is not fully independent, and it has only 20 messages.
- Still missed or wrongly flagged: fake job offers asking for a fee, some earning-offer scams, and genuine Aadhaar update messages.
## Future work
- Collect real, anonymised scam messages and test on them.
- Better handling of legitimate OTP and bank alerts.
- Tamil and Hindi support.
- Learn the rule/ML weights instead of a fixed average.

## Run it