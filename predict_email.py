import joblib

model=joblib.load("email_model.pkl")
vectorizer=joblib.load("vectorizer.pkl")

reply_map={
"Work":"Thank you for your email. I will review it and get back to you shortly.",
"Finance":"Thank you. Your financial request has been received.",
"Spam":"This email appears to be spam. No reply is recommended.",
"Promotion":"Thank you for the promotional information.",
"Newsletter":"Thank you for the newsletter.",
"Social":"Thank you for reaching out on social media.",
"Personal":"Thank you! I'll get back to you soon.",
"Support":"Your support request has been received. We will respond shortly."
}

priority_keywords={
"High":["urgent","asap","immediately","important","critical"],
"Medium":["meeting","project","invoice","payment","report"],
"Low":[]
}

subject=input("Enter Subject: ")
body=input("Enter Body: ")

text=subject+" "+body
vec=vectorizer.transform([text])

category=model.predict(vec)[0]

lower=text.lower()
priority="Low"
if any(k in lower for k in priority_keywords["High"]):
    priority="High"
elif any(k in lower for k in priority_keywords["Medium"]):
    priority="Medium"

print("\nPredicted Category :",category)
print("Predicted Priority :",priority)
print("Suggested Reply    :",reply_map.get(category,"Thank you for your email."))
