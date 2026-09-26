from flask import Flask, render_template, request
import joblib
from datetime import datetime

app = Flask(__name__)

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("email_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Temporary history
prediction_history = []

print("==========================================")
print("AI EMAIL CLASSIFICATION SYSTEM")
print("==========================================")
print("Model loaded successfully")
print("Vectorizer loaded successfully")
print("==========================================")


# ==========================================
# REPLY SUGGESTION
# ==========================================

def generate_reply(category):

    category = str(category).lower()

    if "spam" in category:
        return "Thank you for your message. We have reviewed your email and will take the necessary action."

    elif "finance" in category:
        return "Thank you for contacting us regarding the financial matter. We have received your request and will review it shortly."

    elif "work" in category:
        return "Thank you for your email. I have received the information and will get back to you after reviewing it."

    elif "support" in category:
        return "Thank you for contacting support. We have received your request and will look into the issue as soon as possible."

    elif "promotion" in category:
        return "Thank you for sharing the information. I will review the offer and get back to you if required."

    elif "social" in category:
        return "Thank you for your message. It is nice to hear from you. I will get back to you soon."

    elif "newsletter" in category:
        return "Thank you for sharing the update. I have received the information successfully."

    elif "personal" in category:
        return "Thank you for your message. I appreciate you reaching out. I will get back to you soon."

    else:
        return "Thank you for your email. I have received your message and will get back to you shortly."


# ==========================================
# PRIORITY PREDICTION
# ==========================================

def predict_priority(subject, body):

    text = (subject + " " + body).lower()

    high_words = [
        "urgent",
        "emergency",
        "immediately",
        "asap",
        "critical",
        "important",
        "deadline",
        "action required",
        "account blocked",
        "payment failed"
    ]

    medium_words = [
        "please",
        "request",
        "meeting",
        "update",
        "reminder",
        "follow up",
        "information"
    ]

    for word in high_words:
        if word in text:
            return "High"

    for word in medium_words:
        if word in text:
            return "Medium"

    return "Low"


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# CLASSIFY EMAIL
# ==========================================

@app.route("/classify")
def classify():
    return render_template("classify.html")


# ==========================================
# PREDICT
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    subject = request.form.get("subject", "").strip()
    body = request.form.get("body", "").strip()

    # Empty email
    if subject == "" and body == "":
        return render_template(
            "result.html",
            prediction="No email entered",
            priority="Unknown",
            reply="Please enter an email before classification.",
            subject="",
            body=""
        )

    # Combine subject and body
    full_text = subject + " " + body

    try:

        # TF-IDF transformation
        text_vector = vectorizer.transform([full_text])

        # ML prediction
        prediction = model.predict(text_vector)[0]

    except Exception as e:

        print("Prediction error:", e)

        return render_template(
            "result.html",
            prediction="Prediction Error",
            priority="Unknown",
            reply="Unable to classify this email.",
            subject=subject,
            body=body
        )

    # Priority
    priority = predict_priority(subject, body)

    # Reply
    reply = generate_reply(prediction)

    # Date and time
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Save history
    prediction_history.append({
        "subject": subject,
        "category": prediction,
        "priority": priority,
        "time": current_time
    })

    print("==========================================")
    print("EMAIL PREDICTION")
    print("Subject :", subject)
    print("Category:", prediction)
    print("Priority:", priority)
    print("==========================================")

    return render_template(
        "result.html",
        prediction=prediction,
        priority=priority,
        reply=reply,
        subject=subject,
        body=body
    )


# ==========================================
# HISTORY
# ==========================================

@app.route("/history")
def history():
    return render_template(
        "history.html",
        history=prediction_history
    )


# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
