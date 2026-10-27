import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from train_extra import SCAM_EXTRA, NORMAL_EXTRA

df = pd.read_csv("SMSSpamCollection", sep="\t", names=["label", "text"])
df["y"] = (df["label"] == "spam").astype(int)

extra_texts = SCAM_EXTRA + NORMAL_EXTRA
extra_y = [1] * len(SCAM_EXTRA) + [0] * len(NORMAL_EXTRA)

REPEAT = 10  # Indian messages-ku adhigam weight kudukka
texts = list(df["text"]) + extra_texts * REPEAT
y = list(df["y"]) + extra_y * REPEAT

vec = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2))
X = vec.fit_transform(texts)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X, y)

joblib.dump(vec, "vec.pkl")
joblib.dump(model, "model.pkl")
print("Model retrained with", len(extra_texts), "Indian-style messages")