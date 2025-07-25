# 🧾 Price Volume Analyzer Web App

A **Streamlit-based web application** that allows users to upload Excel or CSV files, automatically formats and cleans the data (removing dangerous characters, fixing column types, etc.), and exports a sanitized version for download.

---
## 🚀 Demo

Check out the live app here: [https://your-streamlit-app-url.streamlit.app](https://aiengineer-dataprocessingtool-fejphjszzjqwpg3knedvcm.streamlit.app/))

## ✅ Technologies Used

- **Python** – Backend logic  
- **Streamlit** – Web app interface  
- **Pandas** – Data manipulation  
- **XlsxWriter** – Export to Excel  
- **Docker** – Containerization  
- **Git/GitHub** – Version control & deployment  
- **Streamlit Community Cloud** – Hosting

---

## 🔐 Vulnerabilities Identified & Fixes

| # | Vulnerability | Fix |
|---|---------------|-----|
| 1 | **CSV/Excel Injection** (e.g. `=2+3`) | Escaped values by prefixing dangerous entries with `'` |
| 2 | **Missing Required Columns** | Added validation function with Streamlit error messaging |
| 3 | **Bad Encoding in CSVs** | Implemented `utf-8` with fallback to `ISO-8859-1` |
| 4 | **Uncaught Exceptions** | Added `try-except` blocks and `logging` support |
| 5 | **Excel Output Corruption** | Sanitized DataFrame before writing using `XlsxWriter` |
| 6 | **Deprecated Pandas Calls** | Replaced `applymap` with safer column-wise `.apply()` |
| 7 | **Invalid Dates** | Used `errors='coerce'` for date parsing |

---

## 🌟 Suggestions for Improvement

- Add support for **multiple file uploads**
- Implement **unit tests** for core functions
- Add **authentication** layer (if required)

---

## 🛠️ Setup Instructions

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/Revanth-r3/AI_Engineer-Data_processing_tool.git
cd AI_Engineer-Data_processing_tool

```
### 🔹 2. Local Setup
`
```
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### 🔹 3. Docker Setup

```
# Build Docker image
docker build -t my-streamlit-app .

# Run container
docker run -p 8501:8501 my-streamlit-app
```

### Open the localhost link

```
http://localhost:8501

Then upload the input data and enter the other manual inputs and generate output
```

### 📂 Sample Data
```
A sample input file (`sample_data.csv`) is included in the `/data` folder. You can use this to test the app.

You can also upload your own CSV file with similar structure to see how the app processes real data.
```
