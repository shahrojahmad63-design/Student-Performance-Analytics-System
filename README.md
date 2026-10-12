# 🎓 Student Performance Analytics System

A complete, beginner-friendly data analytics project built with **Python 3**, **NumPy**, **Pandas**, **Matplotlib**, and **Streamlit**. Designed for academic mini-project submissions, viva presentations, and real-world student grading analysis.

---

## 📌 Project Overview

The **Student Performance Analytics System** automates the assessment of student academic records. It reads student marks in core subjects (Python, Mathematics, English) alongside attendance records, calculates individual performance metrics, assigns standard letter grades, evaluates pass/fail status, and detects the impact of class attendance on student marks.

It includes:
1. **Command-Line Interface (CLI)**: Fast, detailed terminal report with ASCII charts and formatted tables (`main.py`).
2. **Interactive Web Dashboard**: Modern, responsive, multi-page web application powered by **Streamlit** (`app.py`).
3. **Reusable Data Engine**: Pure modular calculation and validation logic in `functions.py`.
4. **Comprehensive Test Suite**: Automated unit tests using Python's built-in `unittest` framework (`tests/test_functions.py`).

---

## 🌟 Key Features

- **Automated Data Ingestion**: Reads records seamlessly from CSV using Pandas.
- **Robust Data Validation**: Detects missing columns, null values, duplicate Student IDs, and marks/attendance values outside the valid range `[0, 100]`.
- **Vectorized Performance Calculations**: Uses NumPy array operations to compute Total Marks and Average Marks.
- **Consistent Grading & Pass/Fail Rules**:
  - **Passing Condition**: A student must secure at least **40 marks in EACH individual subject** (Python, Maths, and English) to pass. Scoring below 40 in any subject results in an automatic **Fail** and grade **F**.
  - **Grading Scheme**:
    - **A+** : Average $\ge$ 90% (Pass)
    - **A** : 80% $\le$ Average $<$ 90% (Pass)
    - **B** : 70% $\le$ Average $<$ 80% (Pass)
    - **C** : 60% $\le$ Average $<$ 70% (Pass)
    - **D** : 50% $\le$ Average $<$ 60% (Pass)
    - **E** : 40% $\le$ Average $<$ 50% (Pass)
    - **F** : Average $<$ 40% OR Failed in any subject
- **Class Summary & Insights**:
  - Total students enrolled.
  - Overall class average score.
  - Total passed and failed student count and percentages.
  - Highest-performing and lowest-performing student identification.
- **Subject-Wise Analysis**: Computes mean, minimum, and maximum scores for each subject.
- **Rankings & Hall of Fame**: Instant retrieval of Top 3 and Top 5 performers.
- **Attendance vs Performance Analytics**:
  - Groups attendance into High ($\ge 85\%$), Moderate ($75\% - 84\%$), and Low ($< 75\%$) categories.
  - Calculates Pearson correlation between attendance percentage and average marks.
- **Dynamic Search & Filtering**: Filter records by Student Name, ID, Department, Grade, and Result status.
- **Custom Dataset Upload & CSV Export**: Upload any custom CSV dataset with automated validation, and export analyzed results in one click.

---

## 📂 Project Structure

```text
student-performance-analytics/
├── main.py                    # Command-line analytics application
├── app.py                     # Streamlit interactive web dashboard
├── functions.py               # Reusable calculations, validation, and analytics engine
├── students.csv               # 25 realistic sample student records
├── requirements.txt           # Python dependencies (pandas, numpy, matplotlib, streamlit)
├── README.md                  # Project overview, installation, and usage instructions
├── Project_Documentation.md   # Comprehensive assignment documentation
├── .gitignore                 # Excludes venv, pycache, temporary files
├── screenshots/               # Application UI and CLI screenshots
└── tests/
    └── test_functions.py      # Automated unit tests for calculation and validation logic
```

---

## 💻 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.9+** | Core programming language |
| **Pandas** | Tabular data manipulation, CSV ingestion, and filtering |
| **NumPy** | Vectorized mathematical operations, statistical calculations, correlations |
| **Matplotlib** | Static bar charts, boxplots, scatter plots, and pie charts |
| **Streamlit** | Responsive, modern web dashboard UI |
| **unittest** | Automated unit testing |
| **Git & GitHub** | Source code version control |

---

## 🚀 Quickstart Guide (macOS / Linux)

### 1. Clone or Open the Project Directory
```bash
cd "/Users/apple/Desktop/ai intrn project/student-performance-analytics"
```

### 2. Set Up a Virtual Environment
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the Applications

### A. Run Command-Line Program (CLI)
Executes the full analytics pipeline and prints a structured report to your terminal:
```bash
python3 main.py
```
*(Optional: Run with a custom CSV dataset: `python3 main.py path/to/my_students.csv`)*

### B. Start the Streamlit Web Dashboard
Launches the interactive dashboard in your default browser (accessible at `http://localhost:8501`):
```bash
streamlit run app.py
```

### C. Run the Unit Test Suite
Executes all automated unit tests:
```bash
python3 -m unittest discover tests
```

---

## 📊 Dataset Schema (`students.csv`)

The dataset contains the following attributes:

| Column Header | Data Type | Description | Valid Range |
| :--- | :--- | :--- | :--- |
| `Student ID` | Integer | Unique identifier for each student | Positive integer |
| `Name` | String | Full name of the student | Text |
| `Department` | String | Academic department (e.g. Computer Science, AI, DS) | Text |
| `Python Marks` | Numeric | Marks obtained in Python course | 0 – 100 |
| `Maths Marks` | Numeric | Marks obtained in Mathematics course | 0 – 100 |
| `English Marks` | Numeric | Marks obtained in English course | 0 – 100 |
| `Attendance Percentage` | Numeric | Student attendance rate | 0 – 100 |

---

## 🐙 Uploading to GitHub

To publish this project to GitHub under `student-performance-analytics`:

1. Initialize git and commit your files:
```bash
cd "/Users/apple/Desktop/ai intrn project/student-performance-analytics"
git init
git add .
git commit -m "Initial commit: Complete Student Performance Analytics System"
```

2. Create a new repository on [GitHub](https://github.com/new) named:
   `student-performance-analytics`

3. Link the remote repository and push:
```bash
git remote add origin https://github.com/shahrojahmad63-design/Student-Performance-Analytics-System.git
git branch -M main
git push -u origin main
```

---

## 🎓 College Viva Preparation (Q&A)

1. **Q: Why use NumPy when Pandas is already available?**
   - *A:* NumPy provides low-level array manipulation and vectorized arithmetic. In `functions.py`, we convert columns to NumPy arrays to rapidly compute total marks, apply conditional filters with `np.where`, compute correlation coefficients with `np.corrcoef`, and extract minimums/maximums without row-by-row Python loop overhead.

2. **Q: How is Pass/Fail status decided?**
   - *A:* A student must score at least 40 in Python, Maths, and English individually. If a student scores 95 in Maths and 95 in English but 35 in Python, they are marked as **Fail** with an automatic grade **F**, preventing a high average from masking a subject failure.

3. **Q: How does the attendance correlation work?**
   - *A:* We calculate the Pearson correlation coefficient between `Attendance Percentage` and `Average Marks`. A positive value close to +1 indicates that higher attendance strongly corresponds to higher academic marks.

---

## 📄 License
This project is open-source and intended for educational purposes.
