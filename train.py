import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("SMSSpamCollection", sep="\t", names=["label", "text"])
df["y"] = (df["label"] == "spam").astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["y"], test_size=0.2, random_state=42, stratify=df["y"])

vec = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2))
Xtr = vec.fit_transform(X_train)
Xte = vec.transform(X_test)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(Xtr, y_train)

print(classification_report(y_test, model.predict(Xte)))

joblib.dump(vec, "vec.pkl")
joblib.dump(model, "model.pkl")