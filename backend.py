from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import shap
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

# Force Matplotlib to use a non-interactive backend (prevents crashes on servers)
matplotlib.use('Agg')

app = FastAPI()

# --- 1. ENABLE CORS (Allow Frontend to Talk to Backend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (React, browser, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, etc.
    allow_headers=["*"],
)

# --- 2. LOAD TRAINED MODEL & ASSETS ---
try:
    print("⏳ Loading Model and Assets...")
    model = joblib.load('risk_model.pkl')
    # We load the column names we saved during training to ensure inputs match perfectly
    model_columns = joblib.load('model_columns.pkl')
    
    # Initialize SHAP Explainer (The "Why" Engine)
    explainer = shap.TreeExplainer(model)
    print("✅ Model Loaded Successfully!")
except Exception as e:
    print(f"❌ CRITICAL ERROR: Could not load model files. {e}")
    print("Make sure 'risk_model.pkl' and 'model_columns.pkl' are in the same folder.")

# --- 3. DEFINE INPUT FORMAT (Must match Frontend JSON) ---
class StudentRequest(BaseModel):
    G1: int       # Grade (0-20)
    absences: int # Number of absences
    studytime: int # 1 to 4

# --- 4. HELPER FUNCTION: GENERATE SHAP IMAGE ---
def create_shap_plot_base64(input_df):
    try:
        # Calculate SHAP values for this specific student
        shap_values = explainer.shap_values(input_df)
        
        # Create the plot
        plt.figure(figsize=(10, 4))
        shap.force_plot(
            explainer.expected_value, 
            shap_values[0, :], 
            input_df.iloc[0, :], 
            matplotlib=True,
            show=False,
            text_rotation=15
        )
        
        # Save to a memory buffer (not a file)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', dpi=120)
        plt.close()
        buf.seek(0)
        
        # Encode as Base64 string for the frontend
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        return img_str
    except Exception as e:
        print(f"⚠️ Error generating SHAP plot: {e}")
        return ""

# --- 5. THE API ENDPOINT ---
@app.post("/predict")
async def predict_risk(data: StudentRequest):
    print(f"📥 Received Data: G1={data.G1}, Absences={data.absences}, StudyTime={data.studytime}")
    
    try:
        # A. PREPARE THE DATA ROW
        # Create a DataFrame with all 0s, using the columns from training
        input_df = pd.DataFrame(columns=model_columns)
        input_df.loc[0] = 0  # Initialize one row of zeros
        
        # B. FILL IN USER INPUTS
        # We only update the 3 fields the user changed. 
        # The rest stay 0 (default/neutral) or you can set better defaults here.
        if 'G1' in input_df.columns:
            input_df.at[0, 'G1'] = data.G1
        if 'absences' in input_df.columns:
            input_df.at[0, 'absences'] = data.absences
        if 'studytime' in input_df.columns:
            input_df.at[0, 'studytime'] = data.studytime
            
        # IMPORTANT: If your model used other important features (like 'failures'), 
        # setting them to 0 is fine for a demo, but ideally, you'd ask for them too.

        # C. PREDICT
        # predict_proba returns [[prob_class_0, prob_class_1]]
        prob_fail = float(model.predict_proba(input_df)[0][1])
        
        # Logic: If probability > 50%, they are High Risk
        risk_label = "High Risk" if prob_fail > 0.5 else "Safe"
        
        print(f"🤖 Prediction: {risk_label} ({prob_fail:.2f})")

        # D. EXPLAIN (SHAP)
        shap_image = create_shap_plot_base64(input_df)

        # E. RETURN RESPONSE
        return {
            "risk_score": prob_fail,
            "label": risk_label,
            "shap_image_base64": shap_image
        }

    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# To run this: uvicorn backend:app --reload