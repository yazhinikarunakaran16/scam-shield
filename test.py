import joblib

vec = joblib.load("vec.pkl")
model = joblib.load("model.pkl")

messages = [
    "URGENT! Your bank account is blocked. Click bit.ly/xyz to verify now",
    "Congratulations! You won a free prize. Call 09061701461 to claim",
    "Hey, are we meeting at 5 pm today?",
    "Please send me the notes from class",
]

for msg in messages:
    p = model.predict_proba(vec.transform([msg]))[0][1]
    print(f"{p:.2f}  |  {msg}")