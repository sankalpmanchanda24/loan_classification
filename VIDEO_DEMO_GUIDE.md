# 🎬 CreditWise AI — Demo Video Guide

A step-by-step script for recording a project demo video similar to the reference style.

---

## 🛠️ Setup Before Recording

1. **Resolution:** Record at 1920×1080 (1080p) or 2560×1440 for crisp output
2. **Browser:** Use Chrome/Edge in full screen, zoom to 90%
3. **Zoom tool:** Enable macOS screen zoom or use browser DevTools device simulation
4. **Screen recorder:** OBS Studio (free), Loom, or QuickTime (Mac built-in)
5. **Mic:** Use a decent microphone or record narration in post
6. **Start the app:** `python3 app.py` → open `http://127.0.0.1:5001`

---

## 🎥 Video Structure (~3–5 minutes)

### PART 1 — Hook / Intro (0:00–0:20)
> **Show:** A quick zoom-in on the hero section of the running website  
> **Say:** _"In this video I'll show you my Loan Eligibility Predictor — an AI-powered web app built with Python, Flask, and XGBoost that predicts loan approval in under a second."_

- Slowly scroll the hero section showing the animated particles background
- Highlight the "92% Accuracy" and "30+ Parameters" stats

---

### PART 2 — Project Overview (0:20–0:50)
> **Show:** VS Code / Finder with the project folder structure  
> **Say:** _"The project uses an XGBoost classifier trained on 50,000 loan records, a Flask backend, and a fully custom frontend with smooth animations."_

- Briefly show: `Loan_Classification.py`, `app.py`, `models/`, `templates/`, `static/`
- Optionally show: `data/loan_detection.csv` with a quick scroll

---

### PART 3 — Live Demo (0:50–2:30)
> **Show:** Browser running the app

**Step 1 — Scroll through form sections**  
Slowly scroll the page showing all 4 form cards fade in:
- Personal Information
- Employment & Education  
- Financial Profile (highlight the live credit score meter!)
- Loan Request Details

**Step 2 — Fill an APPROVED application**  
Fill in strong values:
- Age: 32, Married, Salaried, 8 years employed
- Income: $85,000, Credit Score: 760 → watch the "Excellent" badge appear live
- DTI: 0.22 → "Good" badge
- Loan: $40,000 at 6.5%, 48 months, Home

Click **"Analyze My Application"** and show:
- Button loading state
- Modal opens with the spinning AI rings
- 3-step loading animation
- Result card slides in → **APPROVED ✅** with green 99% confidence bar

**Step 3 — Fill a DECLINED application**  
Change values:
- Credit Score: 480 → watch "Very Poor" badge turn red
- DTI: 0.65 → "High" badge turns red
- Unemployed status
- Loan: $150,000

Click submit → Show **DECLINED ❌** result with red confidence bar

---

### PART 4 — Code Walkthrough (2:30–3:30)
> **Show:** VS Code

1. Open `app.py` → scroll to the `/predict` route
   - _"The Flask endpoint receives JSON, maps it to 30 feature columns, scales numerical values, and runs the XGBoost model in ~10ms."_

2. Open `Loan_Classification.py` → show training section
   - _"The model was trained with class balancing, 5-fold cross-validation, and achieved 92% accuracy."_

3. Open `templates/index.html` → briefly show the 4 form sections

4. Open `static/js/script.js` → show particle system init and `renderResult()`
   - _"The frontend uses a canvas-based particle system, IntersectionObserver for scroll animations, and live credit score / DTI meters."_

---

### PART 5 — Results / Closing (3:30–4:00)
> **Show:** Back to browser, scroll hero section

> **Say:** _"This project demonstrates an end-to-end ML pipeline — from data preprocessing and feature engineering to model training, deployment, and a polished production-ready UI. All code is on GitHub."_

- Show GitHub link if applicable
- End with the hero section and fade out

---

## 🎨 Editing Tips

| Element | Recommendation |
|---------|---------------|
| **Intro title card** | "CreditWise AI — Loan Predictor" with dark bg + gradient text |
| **Background music** | Lo-fi / ambient tech music (YouTube Audio Library) |
| **Zoom effects** | Punch-in zoom on key UI moments (credit badge change, modal) |
| **Captions** | Add captions with the `Auto-generated` then edit in editor |
| **Thumbnail** | Screenshot of the APPROVED modal over the dark UI background |
| **Chapters** (YouTube) | Add timestamps for each part in the description |

---

## 📝 YouTube Description Template

```
🏦 CreditWise AI — Real-time Loan Eligibility Predictor

Built with:
• Python + Flask backend
• XGBoost classifier (92% accuracy, 50K training samples)  
• Custom animated UI (particles, live credit meter, smooth transitions)
• 30+ financial features analyzed

⏱️ Timestamps:
0:00 – Intro
0:20 – Project structure
0:50 – Live demo (Approved)
1:40 – Live demo (Declined)
2:30 – Code walkthrough
3:30 – Results & closing

📦 GitHub: [your link here]

Tags: machine learning, python, flask, xgboost, loan prediction, web app, data science project
```

---

## 🖥️ Recommended Recording Software

- **macOS:** QuickTime (free) or OBS Studio
- **Windows:** OBS Studio or Xbox Game Bar (Win+G)
- **Zoom/annotation:** Screenflow (Mac), Camtasia, or free: Loom
- **Video editor:** DaVinci Resolve (free) or iMovie

---

> 💡 **Tip:** Record at 60fps if possible — the smooth CSS animations and particle effects look much better at higher frame rates.
