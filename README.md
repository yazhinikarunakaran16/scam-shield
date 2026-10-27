# Scam Message Shield

Detects scam SMS/WhatsApp messages and explains why they are risky.

## Current status
- TF-IDF + Logistic Regression model trained on UCI SMS Spam Collection
- Test results (1,115 messages): scam precision 0.90, recall 0.93, F1 0.91

## Coming next
- Rule-based features (suspicious links, urgency, OTP/bank requests)
- Indian-style scam message test set
- LLM explanations
- Streamlit app
