# Academic Project Documentation
## Student Performance Analytics System

---

### 1. Project Title & Objective

- **Project Title:** Student Performance Analytics System
- **Academic Domain:** Python Programming, Applied Data Analytics, and Educational Informatics
- **Target Audience:** Python with AI Course Assignment / Mini-Project Submission
- **GitHub Repository URL:** https://github.com/shahrojahmad63-design/Student-Performance-Analytics-System

#### Objective
The primary objective of this project is to develop an automated, reliable, and user-friendly software solution to analyze student marks and attendance data. Using core Python, NumPy, Pandas, and Streamlit, the system provides:
1. Automated ingestion, cleaning, and multi-factor validation of student academic records.
2. Vectorized calculation of aggregate marks, averages, subject-wise statistics, and letter grades.
3. Accurate evaluation of student Pass/Fail status governed by strict per-subject passing thresholds.
4. Identification of high-achieving students and learners requiring academic intervention.
5. Statistical exploration of the relationship between attendance rates and academic performance.
6. A dual-interface experience: an exhaustive command-line reporting tool and an interactive Streamlit web dashboard.

---

### 2. Technologies Used & Justification

| Technology | Role | Justification |
| :--- | :--- | :--- |
| **Python 3.9+** | Core Language | Robust standard library, readable syntax, and native mathematical capabilities ideal for foundational analytics. |
| **NumPy** | Numerical Computation | Offers high-performance $N$-dimensional arrays, element-wise arithmetic, and statistical routines (`np.mean`, `np.corrcoef`, `np.where`) that bypass slow Python loops. |
| **Pandas** | Tabular Data Processing | Provides high-level `DataFrame` structures for reading CSV files, indexing, grouped aggregations, and multi-condition filtering. |
| **Matplotlib** | Data Visualization | Generates publication-ready static charts (bar charts, boxplots, scatter plots, and pie charts). |
| **Streamlit** | Web Application Dashboard | Rapidly turns data scripts into interactive, reactive web applications without requiring complex frontend frameworks. |
| **unittest** | Quality Assurance | Built-in test automation library ensuring reliability across mathematical calculations, edge-case scores, and validation checks. |
| **Git / GitHub** | Version Control | Enables distributed version tracking, professional documentation hosting, and portfolio presentation. |

---

### 3. Dataset Description & Schema

The system operates on tabular CSV records representing student cohorts. A sample dataset consisting of 25 realistic student records is provided in `students.csv`.

#### Dataset Attributes:
1. **Student ID** (`int`): Unique identifier assigned to each student.
2. **Name** (`str`): Full name of the student.
3. **Department** (`str`): Academic discipline (Computer Science, Data Science, Artificial Intelligence, Information Technology).
4. **Python Marks** (`float`/`int`): Score achieved in Python course (Range: $0$ to $100$).
5. **Maths Marks** (`float`/`int`): Score achieved in Mathematics course (Range: $0$ to $100$).
6. **English Marks** (`float`/`int`): Score achieved in English course (Range: $0$ to $100$).
7. **Attendance Percentage** (`float`/`int`): Ratio of attended classes to total sessions held (Range: $0$ to $100$).

#### Data Integrity Constraints:
- No missing values (`NaN`/`null`) permitted in calculation columns.
- Student IDs must be strictly unique (duplicate IDs flagged).
- Numeric marks and attendance figures must reside strictly within $[0, 100]$.

---

### 4. System Architecture & Workflow

The architecture follows a decoupled **Model-View separation**:
- **Engine Layer (`functions.py`)**: Stateless, testable functions for loading, validating, calculating, ranking, and filtering.
- **Presentation Layer (CLI - `main.py`)**: Terminal workflow for batch reporting, formatted tables, and exports.
- **Presentation Layer (Web - `app.py`)**: Reactive Streamlit dashboard with tabs, filters, and charts.

```
       [ students.csv / Uploaded CSV ]
                      │
                      ▼
            [ load_dataset() ]
                      │
                      ▼
        [ validate_student_data() ]
         ├── Column Presence Check
         ├── Null / NaN Detection
         ├── Duplicate ID Detection
         └── Range Validation [0 - 100]
                      │
                      ▼
      [ calculate_student_results() ]
         ├── NumPy Total Marks Addition
         ├── NumPy Average Marks Division
         ├── Pass/Fail Thresholding (≥ 40 in all subjects)
         └── Letter Grade Assignment (A+ to F)
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
   [ main.py - CLI ]       [ app.py - Web UI ]
   • Class Summary         • Interactive Metric Cards
   • Subject Stats         • Dynamic Search & Filtering
   • Top 3 / Top 5         • Matplotlib Visualizations
   • Attendance Analysis   • Drag-and-drop CSV Upload
   • CSV Auto-Export       • 1-Click CSV Download
```

---

### 5. Grading Rules & Pass/Fail Criteria

To ensure academic fairness and consistency, the system applies unambiguous rules:

#### 1. Pass/Fail Decision Rule:
$$\text{Result} = \begin{cases} \text{"Pass"}, & \text{if } \min(\text{Python}, \text{Maths}, \text{English}) \ge 40 \\ \text{"Fail"}, & \text{otherwise} \end{cases}$$
*Key Note:* Even if a student achieves an overall average of $75\%$, if their score in any single subject is below $40$, their status is immediately marked as **Fail** and their assigned grade is **F**.

#### 2. Grade Assignment Scale (for Passing Students):
- **A+** : Average Marks $\ge 90\%$
- **A** : $80\% \le \text{Average Marks} < 90\%$
- **B** : $70\% \le \text{Average Marks} < 80\%$
- **C** : $60\% \le \text{Average Marks} < 70\%$
- **D** : $50\% \le \text{Average Marks} < 60\%$
- **E** : $40\% \le \text{Average Marks} < 50\%$
- **F** : $\text{Average Marks} < 40\%$ OR $\text{Result} == \text{"Fail"}$

---

### 6. Key Features & Implementation Details

1. **Vectorized Computations (`functions.py`)**:
   Uses NumPy vectors (`df["Python Marks"].to_numpy()`) to calculate aggregates in a single vectorized pass.
2. **Attendance Impact Analysis**:
   Discretizes continuous attendance into three operational brackets:
   - *High Attendance:* $\ge 85\%$
   - *Moderate Attendance:* $75\% \text{ to } 84\%$
   - *Low Attendance:* $< 75\%$
   Computes Pearson correlation coefficient using `np.corrcoef()`.
3. **Multi-Faceted Search and Filter**:
   Allows simultaneous query by student name/ID, department, letter grade, and pass/fail result.
4. **Data Export**:
   Exports complete records with newly computed columns (`Total Marks`, `Average Marks`, `Grade`, `Result`) into `analyzed_students_output.csv`.

---

### 7. Sample Output

#### Sample CLI Output (`main.py`):
```text
=================================================================
       STUDENT PERFORMANCE ANALYTICS SYSTEM
     Powered by Python 3, NumPy, and Pandas
=================================================================

[INFO] Loading dataset from: students.csv
[SUCCESS] Loaded 25 student records.

[INFO] Validating dataset integrity...
[SUCCESS] All data validation checks passed perfectly!

=================================================================
  1. CLASS SUMMARY & OVERVIEW
=================================================================
Total Students Enrolled : 25
Overall Class Average   : 72.84 / 100
Passed Students Count   : 22 (88.0%)
Failed Students Count   : 3 (12.0%)
Highest Performer       : Shreya Ghosh (ID: 122, Dept: Data Science) - Avg: 96.0%, Grade: A+
Lowest Performer        : Manish Pandey (ID: 119, Dept: Information Technology) - Avg: 40.0%, Grade: F

=================================================================
  2. SUBJECT-WISE PERFORMANCE (NUMPY ANALYSIS)
=================================================================
Subject  Average Marks  Minimum Marks  Maximum Marks
 Python          71.64           35.0           96.0
  Maths          72.56           38.0           98.0
English          74.32           42.0           94.0

=================================================================
  3. TOP 3 STUDENTS (HALL OF FAME)
=================================================================
 Student ID          Name              Department  Average Marks  Total Marks Grade
        122  Shreya Ghosh            Data Science          96.00          288    A+
        104   Ananya Iyer Artificial Intelligence          94.33          283    A+
        114 Neha Kulkarni            Data Science          91.00          273    A+

=================================================================
  6. ATTENDANCE VS PERFORMANCE CORRELATION
=================================================================
Pearson Correlation (Attendance vs Avg Marks): +0.984
Insight: Strong positive correlation - High attendance strongly correlates with high marks.
```

---

### 8. Testing & Validation

The test suite in `tests/test_functions.py` contains 8 comprehensive unit tests:
- `test_assign_grade`: Verifies all grading boundaries and failing constraints.
- `test_calculate_student_results`: Confirms accuracy of total marks, averages, pass/fail status, and grade assignment.
- `test_calculate_class_summary`: Confirms class aggregate calculations and top/bottom performer identification.
- `test_calculate_subject_averages`: Validates subject-level averages, minimums, and maximums.
- `test_get_top_and_lowest_students`: Asserts correct sorting and slicing of ranking lists.
- `test_analyze_attendance_impact`: Checks attendance bracket categorization and correlation output.
- `test_filter_students`: Tests dynamic query resolution by name, department, and pass/fail condition.
- `test_validate_student_data_errors`: Confirms detection of missing columns, duplicate IDs, and out-of-range marks.

#### Test Execution Result:
```bash
python3 -m unittest discover tests
........
----------------------------------------------------------------------
Ran 8 tests in 0.071s

OK
```

---

### 9. Challenges Faced & Solutions

1. **Challenge: Preventing Unfair Passes via Averages**
   - *Problem:* A student with marks $[95, 95, 20]$ would have an average of $70\%$, falsely qualifying for grade B.
   - *Solution:* Implemented an explicit condition requiring $\ge 40$ in every subject before assigning any passing letter grade. Failing students are forced to Grade **F**.
2. **Challenge: Cross-Platform File Paths**
   - *Problem:* Running scripts from different working directories could cause `FileNotFoundError` when accessing `students.csv`.
   - *Solution:* Used relative directory resolution with `os.path.dirname(os.path.abspath(__file__))` to guarantee seamless path discovery.
3. **Challenge: Handling Bad Uploads in Web UI**
   - *Problem:* Users uploading unformatted CSVs could crash the Streamlit interface.
   - *Solution:* Integrated robust pre-flight validation returning user-friendly warning messages without raising uncaught exceptions.

---

### 10. Learning Outcomes

1. Mastery of **NumPy** array operations, broadcasting, and boolean masks.
2. Proficiency in **Pandas** for real-world CSV parsing, DataFrame wrangling, and grouping.
3. Rapid development of reactive, polished dashboards using **Streamlit**.
4. Writing modular, production-ready code with decoupled business logic and unit test coverage.
5. Understanding version control workflows with Git and GitHub.
