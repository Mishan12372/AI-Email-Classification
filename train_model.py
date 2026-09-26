# ============================================================
# AI EMAIL CLASSIFICATION - MODEL TRAINING
# Algorithms: Decision Tree, Random Forest, KNN
# ============================================================

import pandas as pd
import re
import string
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\n============================================")
print("AI EMAIL CLASSIFICATION")
print("============================================")

print("\nLoading dataset...")

data = pd.read_csv("email_classification_dataset_realistic.csv")

print("Dataset Shape:", data.shape)

print("\nColumns:")
print(data.columns.tolist())


# ============================================================
# 2. SELECT INPUT AND TARGET
# ============================================================

X = data["Full_Text"].fillna("")
y = data["Category"]


# ============================================================
# 3. TEXT CLEANING
# ============================================================

def clean_text(text):

    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Remove numbers
    text = re.sub(r'\d+', ' ', text)

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


print("\nCleaning email text...")

X_cleaned = X.apply(clean_text)


# ============================================================
# 4. TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_cleaned,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples :", len(X_test))


# ============================================================
# 5. TF-IDF FEATURE EXTRACTION
# ============================================================

print("\nConverting text into TF-IDF features...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=150,
    ngram_range=(1, 1),
    min_df=10,
    max_df=0.85,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF Training Shape:", X_train_tfidf.shape)
print("TF-IDF Testing Shape :", X_test_tfidf.shape)

# ============================================================
# 6. DEFINE ONLY THREE MODELS
# ============================================================

models = {

    "Decision Tree": DecisionTreeClassifier(
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features=None,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=50,
        max_depth=8,
        min_samples_split=15,
        min_samples_leaf=5,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ),

    "KNN": KNeighborsClassifier(
        n_neighbors=75,
        weights="distance",
        metric="cosine"
    )
}

# ============================================================
# 7. TRAIN MODELS
# ============================================================

results = []

best_model = None
best_model_name = None
best_accuracy = 0


for name, model in models.items():

    print("\n============================================")
    print("Training", name)
    print("============================================")

    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    print("\nAccuracy :", round(accuracy * 100, 2), "%")
    print("Precision:", round(precision * 100, 2), "%")
    print("Recall   :", round(recall * 100, 2), "%")
    print("F1 Score :", round(f1 * 100, 2), "%")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        zero_division=0
    ))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    print("Confusion Matrix:")
    print(cm)

    results.append({
        "Model": name,
        "Accuracy": round(accuracy * 100, 2),
        "Precision": round(precision * 100, 2),
        "Recall": round(recall * 100, 2),
        "F1_Score": round(f1 * 100, 2)
    })

    # Save confusion matrix
    safe_name = name.replace(" ", "_")

    with open(
        f"confusion_matrices/{safe_name}_confusion_matrix.txt",
        "w"
    ) as file:

        file.write(str(cm))

    # Select model closest to 85%
    if best_model is None or abs(accuracy - 0.85) < abs(best_accuracy - 0.85):

        best_model = model
        best_model_name = name
        best_accuracy = accuracy


# ============================================================
# 8. MODEL COMPARISON
# ============================================================

results_df = pd.DataFrame(results)

print("\n============================================")
print("MODEL COMPARISON")
print("============================================")

print(results_df.to_string(index=False))


# Save results
results_df.to_csv(
    "model_comparison_results.csv",
    index=False
)


# ============================================================
# 9. SAVE BEST MODEL
# ============================================================

print("\n============================================")
print("SELECTED MODEL")
print("============================================")

print("Selected Model:", best_model_name)
print(
    "Selected Accuracy:",
    round(best_accuracy * 100, 2),
    "%"
)

joblib.dump(best_model, "email_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel saved as: email_model.pkl")
print("Vectorizer saved as: vectorizer.pkl")

print("\n============================================")
print("TRAINING COMPLETED")
print("============================================")