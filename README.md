# 🎓 Student Academic Risk Dashboard (XAI Project)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)
![SHAP](https://img.shields.io/badge/Explainability-SHAP-red)

## 📌 Project Overview
This project is an **Explainable AI (XAI) System** designed to predict student dropout risk and, crucially, **explain why** a specific student is at risk.

Unlike "black box" models that simply output a prediction, this system provides actionable insights using **SHAP (Shapley Additive Explanations)** values. It features a full-stack architecture with a **FastAPI** backend (serving the ML model) and a modern **Next.js/React** frontend dashboard for university faculty.

### 🎯 Key Goals
1. **Predict:** Identify students at high risk of failing (Grade < 10) using historical data.
2. **Explain:** Visualize *why* the model made that decision (e.g., "High Absences increased risk by 20%").
3. **Intervene:** Provide an interactive "What-If" dashboard where teachers can adjust variables (like improving attendance) to see if it saves the student.

---

## 🛠️ Tech Stack

### **Backend (The "Brain")**
- **Language:** Python  
- **Machine Learning:** XGBoost Classifier (Optimized with SMOTE for class imbalance)  
- **Explainable AI:** SHAP (TreeExplainer)  
- **API Framework:** FastAPI  
- **Data Processing:** Pandas, NumPy, Scikit-learn  

### **Frontend (The "Face")**
- **Framework:** Next.js (React)  
- **Styling:** Tailwind CSS  
- **UI Components:** Shadcn/ui (Lucide Icons, Sliders, Cards)  
- **Visualization:** Matplotlib (Server-side rendering of SHAP plots)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+

---

## 1️⃣ Backend Setup (Python)

Navigate to the root directory `Student_Risk_XAI`.

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the Server
uvicorn backend:app --reload
```

The backend will start at:  
**http://127.0.0.1:8000**

---

## 2️⃣ Frontend Setup (Next.js)

Open a new terminal and navigate to the frontend folder.

```bash
cd frontend

# 1. Install Node modules
npm install

# 2. Run the Development Server
npm run dev
```

Dashboard will launch at:  
**http://localhost:3000**

---

## 🖥️ Usage Guide

1. Open the Dashboard: http://localhost:3000  
2. Adjust Parameters using sliders:
   - **G1 Grade:** First period grade (0–20)  
   - **Absences:** Number of school absences  
   - **Study Time:** Weekly study time rating (1–4)  
3. Click **Analyze Risk**  
4. View Results:
   - **Risk Score:** Failure probability  
   - **SHAP Force Plot:** Shows how features increased/decreased risk  

---

## 📊 Model Performance

The model was trained on the UCI Student Performance Dataset.

- **Accuracy:** ~85%  
- **Recall (Risk Detection):** 65%  
- **Technique:** SMOTE used to handle class imbalance  

---

## 📂 Project Structure

```bash
Student_Risk_XAI/
├── backend.py              # FastAPI Server & Logic
├── risk_model.pkl          # Trained XGBoost Model
├── model_columns.pkl       # Saved feature names
├── requirements.txt        # Python dependencies
├── explain_model.py        # Script for generating static SHAP analysis
│
├── frontend/               # Next.js Application
│   ├── app/
│   │   ├── page.tsx        # Main Dashboard UI
│   │   ├── layout.tsx      # App Layout
│   │   └── globals.css     # Global Styles
│   ├── components/         # UI Components (Buttons, Sliders)
│   └── package.json        # Node dependencies
│
└── README.md               # Documentation
```

---

## 🛡️ License
This project is for educational purposes as part of the XAI (Explainable AI) coursework.

