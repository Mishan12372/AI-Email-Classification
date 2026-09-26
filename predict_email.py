
# ============================================
# AI EMAIL CLASSIFICATION
# EMAIL PREDICTION
# ============================================

import joblib
import re


# ============================================
# 1. LOAD TRAINED MODEL
# ============================================

model = joblib.load("email_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


print("\n============================================")
print("       AI EMAIL CLASSIFICATION")
print("============================================")


# ============================================
# 2. TEXT CLEANING
# ============================================

def clean_text(text):

    text = text.lower()

    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Remove numbers
    text = re.sub(r'\d+', ' ', text)

    # Remove punctuation
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# ============================================
# 3. SUGGESTED REPLIES
# ============================================

reply_map = {

    "Work": [
        "Thank you for your email. I will review it and get back to you shortly.",
        "Thank you for sharing the information. I will check it and respond soon.",
        "I have received your email. I will review the details and get back to you."
    ],

    "Finance": [
        "Thank you. Your financial request has been received.",
        "Thank you for the information. I will review the financial details and get back to you.",
        "Your financial request has been received. We will review it shortly."
    ],

    "Spam": [
        "This email appears to be spam. No reply is recommended.",
        "This message has been identified as spam. Please avoid responding.",
        "No reply is recommended for this email."
    ],

    "Promotion": [
        "Thank you for sharing the promotional information.",
        "Thank you for the offer. I will review the details.",
        "I have received the promotional information. Thank you."
    ],

    "Newsletter": [
        "Thank you for the newsletter.",
        "Thank you for sharing the latest updates.",
        "I have received the newsletter. Thank you for the information."
    ],

    "Social": [
        "Thank you for reaching out on social media.",
        "Thanks for connecting with me.",
        "Thank you for your message. It was nice hearing from you."
    ],

    "Personal": [
        "Thank you! I'll get back to you soon.",
        "Thanks for your message. I will reply shortly.",
        "Thank you for reaching out. I'll get back to you soon."
    ],

    "Support": [
        "Your support request has been received. We will respond shortly.",
        "Thank you for contacting support. We are looking into your request.",
        "We have received your support request and will get back to you soon."
    ]
}


# ============================================
# 4. PRIORITY KEYWORDS
# ============================================

priority_keywords = {

    "High": [
        "urgent",
        "asap",
        "immediately",
        "important",
        "critical"
    ],

    "Medium": [
        "meeting",
        "project",
        "invoice",
        "payment",
        "report"
    ],

    "Low": []
}


# ============================================
# 5. GET EMAIL INPUT
# ============================================

print("\nEnter the email details below.")

subject = input("\nEnter Subject: ")
body = input("Enter Body: ")


# ============================================
# 6. COMBINE SUBJECT AND BODY
# ============================================

text = subject + " " + body


# ============================================
# 7. CLEAN INPUT TEXT
# ============================================

cleaned_text = clean_text(text)


# ============================================
# 8. CHECK EMPTY INPUT
# ============================================

if cleaned_text == "":
    print("\nError: Please enter a subject or email body.")
    exit()


# ============================================
# 9. CONVERT TEXT INTO TF-IDF
# ============================================

vec = vectorizer.transform([cleaned_text])


# ============================================
# 10. PREDICT EMAIL CATEGORY
# ============================================

category = model.predict(vec)[0]


# ============================================
# 11. PREDICT CONFIDENCE
# ============================================

confidence = None

if hasattr(model, "predict_proba"):

    probabilities = model.predict_proba(vec)

    confidence = max(probabilities[0]) * 100


# ============================================
# 12. PREDICT PRIORITY
# ============================================

lower = cleaned_text.lower()

priority = "Low"

if any(
    keyword in lower
    for keyword in priority_keywords["High"]
):
    priority = "High"

elif any(
    keyword in lower
    for keyword in priority_keywords["Medium"]
):
    priority = "Medium"


# ============================================
# 13. GET SUGGESTED REPLY
# ============================================

suggested_reply = reply_map.get(
    category,
    "Thank you for your email."
)


# ============================================
# 14. DISPLAY RESULT
# ============================================

print("\n============================================")
print("              PREDICTION RESULT")
print("============================================")

print("\nPredicted Category :", category)
print("Predicted Priority :", priority)

if confidence is not None:
    print("Prediction Confidence :", round(confidence, 2), "%")

print("\nSuggested Reply:")
print(suggested_reply)

print("\n============================================")
print("        PREDICTION COMPLETED")
print("============================================")
