import pandas as pd
import re
import joblib


import pandas as pd

data = pd.read_csv("email_classification_dataset_realistic.csv")   # Change the path if needed

print(data.columns)
print(list(data.columns))

# ============================================
# MODEL COMPARISON
# ============================================

# ============================================
# FEATURE EXTRACTION (TF-IDF)
# ============================================
# 1. Separate features and target
X = data["Full_Text"]
y = data["Category"]

# 2. Split the dataset
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# 3. Create TF-IDF vectors
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=1000,
    ngram_range=(1,2)
)

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

# 4. Now train the models

from sklearn.linear_model import LogisticRegression, SGDClassifier, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, ComplementNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Store all models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Multinomial Naive Bayes": MultinomialNB(),
    "Bernoulli Naive Bayes": BernoulliNB(),
    "Complement Naive Bayes": ComplementNB(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Extra Trees": ExtraTreesClassifier(n_estimators=100, random_state=42),
    "Linear SVM": LinearSVC(random_state=42),
    "SGD Classifier": SGDClassifier(random_state=42),
    "Passive Aggressive": PassiveAggressiveClassifier(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

print("\n" + "="*70)
print("MODEL COMPARISON")
print("="*70)

results = []

best_accuracy = 0
best_model = None
best_name = ""

for name, model in models.items():

    # Train model
    model.fit(X_train_vector, y_train)

    # Predict
    prediction = model.predict(X_test_vector)

    # Accuracy
    accuracy = accuracy_score(y_test, prediction)

    # Store result
    results.append((name, accuracy))

    # Display
    print(f"{name:<30} : {accuracy*100:.2f}%")

    # Find best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_name = name

# ============================================
# BEST MODEL
# ============================================

print("\n" + "="*70)
print("BEST MODEL")
print("="*70)

print(f"Model    : {best_name}")
print(f"Accuracy : {best_accuracy*100:.2f}%")

# Save best model
import joblib

joblib.dump(best_model, "email_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nBest model saved successfully.")
print("email_model.pkl created")
print("vectorizer.pkl created")




import pandas as pd

data = pd.read_csv("email_classification_dataset_realistic.csv")

print("Total rows:", len(data))
print("Unique Full_Text:", data["Full_Text"].nunique())

print("\nUnique texts per category:")
print(data.groupby("Category")["Full_Text"].nunique())


print(data["Category"].value_counts())

print(data["Full_Text"].duplicated().sum())


from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(max_features=20)
x = vectorizer.fit_transform(data["Full_Text"])

print(vectorizer.get_feature_names_out())