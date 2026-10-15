# 🤖 AI Usage & Impact Analysis: Students vs Professionals

An end-to-end data analysis project that explores how students and professionals use AI tools, and how it affects their productivity and satisfaction.

## 🔗 Live Dashboard
👉 *(Add your Streamlit link here after deployment)*

## 📌 Project Overview
- **Dataset:** 300 survey records, 19 columns (288 after cleaning)
- **Goal:** Compare AI tool adoption, productivity, satisfaction and time saved between students and professionals
- **Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit

## 🧹 Data Cleaning
- Removed 12 duplicate rows
- Converted text values like `"36 yrs"`, `"$25"`, `"6.4 hrs"` into numbers
- Standardised inconsistent labels (`chatgpt / Chat GPT` → `ChatGPT`, `M / male / MALE` → `Male`, etc.)
- Removed impossible values (age, hours > 24)
- Filled missing values (median for numbers, `Unknown` for text)

## 📊 Key Insights
- **ChatGPT** is the most used AI tool; **Coding** is the top use-case
- About **55%** of users use a free plan
- Paid users do **not** show higher productivity than free users
- Productivity is strongly linked with **Time Saved**, **Satisfaction** and **Usage Hours**
- Age, cost and accuracy rating show almost no effect on productivity

> Note: small survey dataset, so results show correlation, not causation.

## 🖥️ Dashboard Features
- Sidebar filters: User Type, Country, AI Tool, Purpose, Plan
- KPI cards (users, usage, productivity, satisfaction, time saved)
- 8 interactive Plotly charts
- Raw data view + CSV download

## 📁 Project Structure
```
ai-usage-impact-analysis/
├── AI_Usage_Impact_Analysis.ipynb
├── app.py
├── ai_usage_cleaned.csv
├── AI_Usage_and_Impact_on_Students_and_Professionals.csv
├── requirements.txt
└── README.md
```

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 👤 Author
**Prince Patel**  
[GitHub](https://github.com/patelprince1207) | [LinkedIn](https://linkedin.com/in/princepatel-ai-ml)
