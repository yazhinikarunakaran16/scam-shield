import joblib
from sklearn.metrics import classification_report
from rules import rule_features
from test_messages import SCAM, NORMAL

vec = joblib.load("vec.pkl")
model = joblib.load("model.pkl")

messages = SCAM + NORMAL
y_true = [1] * len(SCAM) + [0] * len(NORMAL)

ml = model.predict_proba(vec.transform(messages))[:, 1]
rule = [min(rule_features(m)[0] / 5, 1) for m in messages]
hybrid = [0.5 * a + 0.5 * b for a, b in zip(ml, rule)]


def report(name, probs, thr):
    preds = [1 if p >= thr else 0 for p in probs]
    print("=====", name, "=====")
    print(classification_report(y_true, preds, zero_division=0))


report("ML only", ml, 0.5)
report("Rules only", rule, 0.4)
report("Hybrid (ML + rules)", hybrid, 0.4)

print("Missed scams (hybrid):")
for m, p, t in zip(messages, hybrid, y_true):
    if t == 1 and p < 0.4:
        print(" -", m)

print("Wrongly flagged normal messages (hybrid):")
for m, p, t in zip(messages, hybrid, y_true):
    if t == 0 and p >= 0.4:
        print(" -", m)