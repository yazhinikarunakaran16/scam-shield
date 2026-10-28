import joblib
from sklearn.metrics import classification_report
from rules import rule_features
from tanglish_test import DEV_SCAM, DEV_NORMAL, HOLDOUT_SCAM, HOLDOUT_NORMAL

vec = joblib.load("vec.pkl")
model = joblib.load("model.pkl")


def scores(msgs):
    ml = model.predict_proba(vec.transform(msgs))[:, 1]
    rule = [min(rule_features(m)[0] / 5, 1) for m in msgs]
    hybrid = [0.5 * a + 0.5 * b for a, b in zip(ml, rule)]
    return ml, rule, hybrid


def run(name, scam, normal, show_errors):
    msgs = scam + normal
    y = [1] * len(scam) + [0] * len(normal)
    ml, rule, hybrid = scores(msgs)
    print("#" * 8, name, "#" * 8)
    for label, probs, thr in [("ML only", ml, 0.5),
                              ("Rules only", rule, 0.4),
                              ("Hybrid", hybrid, 0.4)]:
        preds = [1 if p >= thr else 0 for p in probs]
        print("=====", label, "=====")
        print(classification_report(y, preds, zero_division=0))
    if show_errors:
        print("Hybrid missed scams:")
        for m, p, t in zip(msgs, hybrid, y):
            if t == 1 and p < 0.4:
                print(" -", m)
        print("Hybrid wrongly flagged normal:")
        for m, p, t in zip(msgs, hybrid, y):
            if t == 0 and p >= 0.4:
                print(" -", m)


run("DEV (Tanglish)", DEV_SCAM, DEV_NORMAL, True)
run("HOLDOUT (Tanglish)", HOLDOUT_SCAM, HOLDOUT_NORMAL, False)