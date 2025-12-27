import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the Model and Data
print("⏳ Loading model and data...")
model = joblib.load('risk_model.pkl')
X_test = pd.read_csv("X_test_processed.csv")

# 2. Initialize SHAP Explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

print("✅ SHAP values calculated!")

# --- VISUALIZATION 1: GLOBAL IMPORTANCE ---
plt.figure(figsize=(10, 8)) # Make figure larger
shap.summary_plot(shap_values, X_test, show=False)
plt.title("Top Factors Driving Student Risk (Global View)", fontsize=16)
plt.tight_layout()
plt.savefig("shap_summary_plot.png")
plt.clf() # Clear the plot so it doesn't overlap with the next one
print("📸 Saved 'shap_summary_plot.png'")

# --- VISUALIZATION 2: LOCAL EXPLANATION (Student #98) ---
# We know Student #98 is high risk from your previous run
student_index = 98 

print(f"\n🔍 Analyzing Student #{student_index}...")

# Force Plot (Matplotlib version)
# We do NOT use initjs() here. We force matplotlib=True.
plt.figure(figsize=(20, 3)) # Wide figure for the force plot
shap.force_plot(
    explainer.expected_value, 
    shap_values[student_index, :], 
    X_test.iloc[student_index, :],
    matplotlib=True,
    show=False,
    text_rotation=45 # Rotates labels so they don't overlap
)
plt.savefig("shap_student_explanation.png", bbox_inches='tight', dpi=150)
print("📸 Saved 'shap_student_explanation.png'")

print("\n🚀 Phase 2 Complete!")