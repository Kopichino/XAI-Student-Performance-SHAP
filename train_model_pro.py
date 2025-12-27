import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib
import os

print("🚀 Starting Model Training Pipeline...")

# --- STEP 1: LOAD DATA ROBUSTLY ---
file_name = "student-mat.csv"

if not os.path.exists(file_name):
    print(f"❌ ERROR: Could not find {file_name}. Please make sure it is in the same folder as this script.")
    exit()

# Try loading with semicolon first (Raw Kaggle format), then comma (Excel format)
try:
    df = pd.read_csv(file_name, sep=';')
    # Quick check: if we only have 1 column, the separator was wrong
    if df.shape[1] < 2:
        df = pd.read_csv(file_name, sep=',')
    print(f"✅ Data Loaded Successfully! Shape: {df.shape}")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit()

# --- STEP 2: CREATE TARGET & FEATURES ---
# Target: 1 if Final Grade (G3) < 10 (Fail), else 0 (Pass)
df['Risk_Label'] = df['G3'].apply(lambda x: 1 if x < 10 else 0)

# We KEEP 'G1' (First grade) as an early warning signal
# We DROP 'G2' and 'G3' to prevent data leakage (predicting future with future)
drop_cols = ['G3', 'Risk_Label', 'G2']
X = df.drop(drop_cols, axis=1)
y = df['Risk_Label']

# --- STEP 3: ENCODING ---
# Convert text (e.g., "GP", "MS", "yes", "no") into numbers
X = pd.get_dummies(X, drop_first=True)

# --- STEP 4: SPLIT DATA ---
# Stratify ensures we have a fair mix of passing/failing students in both sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- STEP 5: HANDLE IMBALANCE (SMOTE) ---
# This creates "synthetic" failing students so the model learns better
print("⚖️  Balancing data with SMOTE...")
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
print(f"   Original Fail Count: {sum(y_train == 1)}")
print(f"   New Fail Count: {sum(y_train_resampled == 1)}")

# --- STEP 6: TRAIN XGBOOST ---
print("🧠 Training XGBoost Model...")
model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42
)

model.fit(X_train_resampled, y_train_resampled)

# --- STEP 7: EVALUATE ---
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print("\n" + "="*30)
print(f"🏆 FINAL ACCURACY: {acc:.2f}")
print("="*30)

print("\nDetailed Report:")
print(classification_report(y_test, preds))

cm = confusion_matrix(y_test, preds)
print("\nConfusion Matrix (Read this carefully):")
print(f"✅ True Safe: {cm[0][0]} (Student safe, Model said safe)")
print(f"⚠️ False Alarm: {cm[0][1]} (Student safe, Model said Risk)")
print(f"❌ Missed Risk: {cm[1][0]} (Student FAILED, Model said safe) -> WE WANT THIS ZERO")
print(f"✅ Caught Risk: {cm[1][1]} (Student FAILED, Model predicted Risk)")

# --- STEP 8: SAVE ---
joblib.dump(model, 'risk_model.pkl')
joblib.dump(X_train.columns, 'model_columns.pkl')
# Save X_test for our future explanation dashboard
X_test.to_csv("X_test_processed.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("\n💾 Model saved as 'risk_model.pkl'. Ready for Phase 2!")