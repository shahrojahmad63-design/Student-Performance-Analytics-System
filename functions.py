"""
functions.py
============
Student Performance Analytics System
Reusable data processing, validation, calculation, and analytics functions.
Built using Python 3, NumPy, and Pandas.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

# Expected columns in the student dataset
REQUIRED_COLUMNS = [
    "Student ID",
    "Name",
    "Department",
    "Python Marks",
    "Maths Marks",
    "English Marks",
    "Attendance Percentage",
]

# Subject columns
SUBJECT_COLUMNS = ["Python Marks", "Maths Marks", "English Marks"]

# Passing cutoff per subject
PASSING_MARKS = 40


def load_dataset(source: Union[str, any]) -> pd.DataFrame:
    """
    Load student dataset from a file path or file-like buffer (e.g. uploaded file in Streamlit).

    Parameters:
        source: Path to CSV file or file-like buffer object.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    df = pd.read_csv(source)
    # Strip any leading/trailing whitespace from column headers
    df.columns = [col.strip() for col in df.columns]
    return df


def validate_student_data(df: pd.DataFrame) -> Tuple[bool, List[str], pd.DataFrame]:
    """
    Validate dataset for missing columns, null values, duplicates,
    and out-of-range numeric values (marks 0-100, attendance 0-100).

    Parameters:
        df (pd.DataFrame): Raw DataFrame to validate.

    Returns:
        Tuple[bool, List[str], pd.DataFrame]:
            - is_valid: True if no fatal errors exist, False otherwise.
            - error_messages: List of human-friendly error or warning descriptions.
            - cleaned_df: Cleaned copy of DataFrame with proper data types.
    """
    errors: List[str] = []

    # 1. Check for required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(
            f"Missing required column(s): {', '.join(missing_cols)}. "
            f"Expected columns: {', '.join(REQUIRED_COLUMNS)}."
        )
        return False, errors, df

    cleaned_df = df.copy()

    # 2. Check for missing / null values
    null_counts = cleaned_df[REQUIRED_COLUMNS].isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if not cols_with_nulls.empty:
        null_details = ", ".join(
            [f"{col} ({count} missing)" for col, count in cols_with_nulls.items()]
        )
        errors.append(f"Missing (null) values detected in: {null_details}.")

    # 3. Check for duplicate Student IDs
    duplicates = cleaned_df[cleaned_df.duplicated(subset=["Student ID"], keep=False)]
    if not duplicates.empty:
        dup_ids = duplicates["Student ID"].unique().tolist()
        errors.append(f"Duplicate Student ID(s) detected: {dup_ids}.")

    # 4. Convert numeric fields and check range
    numeric_columns = SUBJECT_COLUMNS + ["Attendance Percentage"]
    for col in numeric_columns:
        # Try converting to numeric
        converted = pd.to_numeric(cleaned_df[col], errors="coerce")
        if converted.isnull().any() and not cleaned_df[col].isnull().any():
            errors.append(
                f"Column '{col}' contains non-numeric values that could not be parsed."
            )
        cleaned_df[col] = converted

        # Check range for marks and attendance (0 to 100)
        invalid_values = cleaned_df[
            (cleaned_df[col] < 0) | (cleaned_df[col] > 100)
        ]
        if not invalid_values.empty:
            errors.append(
                f"Column '{col}' has {len(invalid_values)} value(s) outside the valid range [0, 100]."
            )

    is_valid = len(errors) == 0
    return is_valid, errors, cleaned_df


def assign_grade(average_marks: float, result_status: str) -> str:
    """
    Assign letter grade based on Average Marks and Pass/Fail status.

    Grading Scheme:
        A+ : Average >= 90 (and Pass)
        A  : 80 <= Average < 90 (and Pass)
        B  : 70 <= Average < 80 (and Pass)
        C  : 60 <= Average < 70 (and Pass)
        D  : 50 <= Average < 60 (and Pass)
        E  : 40 <= Average < 50 (and Pass)
        F  : Average < 40 OR Result == 'Fail'

    Parameters:
        average_marks (float): Student's average marks out of 100.
        result_status (str): 'Pass' or 'Fail'.

    Returns:
        str: Assigned letter grade.
    """
    if result_status == "Fail":
        return "F"

    if average_marks >= 90:
        return "A+"
    elif average_marks >= 80:
        return "A"
    elif average_marks >= 70:
        return "B"
    elif average_marks >= 60:
        return "C"
    elif average_marks >= 50:
        return "D"
    elif average_marks >= 40:
        return "E"
    else:
        return "F"


def calculate_student_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Total Marks, Average Marks, Pass/Fail Result, and Grade
    for each student using NumPy arrays and Pandas vectorization.

    Rules:
        - Total Marks: Sum of Python, Maths, and English marks.
        - Average Marks: Total Marks / 3.0 (rounded to 2 decimal places).
        - Pass/Fail Condition: Student must score >= 40 in EACH subject.
        - Grade: Assigned using the standard grading scheme.

    Parameters:
        df (pd.DataFrame): Validated student DataFrame.

    Returns:
        pd.DataFrame: Analyzed DataFrame containing new columns:
                      'Total Marks', 'Average Marks', 'Result', 'Grade'.
    """
    analyzed_df = df.copy()

    # Extract marks as NumPy array for calculations
    python_marks = analyzed_df["Python Marks"].to_numpy()
    maths_marks = analyzed_df["Maths Marks"].to_numpy()
    english_marks = analyzed_df["English Marks"].to_numpy()

    # 1. Total Marks (NumPy addition)
    total_marks = python_marks + maths_marks + english_marks
    analyzed_df["Total Marks"] = total_marks

    # 2. Average Marks (Rounded to 2 decimals)
    average_marks = np.round(total_marks / 3.0, 2)
    analyzed_df["Average Marks"] = average_marks

    # 3. Determine Pass/Fail Status
    # Condition: Must score >= 40 in Python AND Maths AND English
    passed_all_subjects = (
        (python_marks >= PASSING_MARKS)
        & (maths_marks >= PASSING_MARKS)
        & (english_marks >= PASSING_MARKS)
    )
    analyzed_df["Result"] = np.where(passed_all_subjects, "Pass", "Fail")

    # 4. Assign Grades using row-wise application
    analyzed_df["Grade"] = [
        assign_grade(avg, res)
        for avg, res in zip(analyzed_df["Average Marks"], analyzed_df["Result"])
    ]

    return analyzed_df


def calculate_class_summary(df: pd.DataFrame) -> Dict[str, Union[int, float, str, Dict]]:
    """
    Compute comprehensive class summary metrics including:
    - Total students
    - Class average marks
    - Passed and failed counts & percentages
    - Highest and lowest performing students

    Parameters:
        df (pd.DataFrame): Analyzed student DataFrame.

    Returns:
        Dict: Summary statistics dictionary.
    """
    total_students = len(df)
    if total_students == 0:
        return {
            "total_students": 0,
            "class_average": 0.0,
            "passed_count": 0,
            "pass_percentage": 0.0,
            "failed_count": 0,
            "fail_percentage": 0.0,
            "highest_student": None,
            "lowest_student": None,
        }

    # Use NumPy for aggregate calculations
    avg_marks_array = df["Average Marks"].to_numpy()
    class_average = float(np.round(np.mean(avg_marks_array), 2))

    passed_count = int(np.sum(df["Result"].to_numpy() == "Pass"))
    failed_count = int(np.sum(df["Result"].to_numpy() == "Fail"))

    pass_percentage = round((passed_count / total_students) * 100, 2)
    fail_percentage = round((failed_count / total_students) * 100, 2)

    # Highest and Lowest performer
    highest_idx = df["Average Marks"].idxmax()
    lowest_idx = df["Average Marks"].idxmin()

    highest_student = df.loc[highest_idx].to_dict()
    lowest_student = df.loc[lowest_idx].to_dict()

    return {
        "total_students": total_students,
        "class_average": class_average,
        "passed_count": passed_count,
        "pass_percentage": pass_percentage,
        "failed_count": failed_count,
        "fail_percentage": fail_percentage,
        "highest_student": highest_student,
        "lowest_student": lowest_student,
    }


def calculate_subject_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate subject-wise average, minimum, and maximum marks using NumPy.

    Parameters:
        df (pd.DataFrame): Student DataFrame.

    Returns:
        pd.DataFrame: Table with Subject, Average, Min, and Max marks.
    """
    subject_stats = []

    for subject in SUBJECT_COLUMNS:
        marks = df[subject].dropna().to_numpy()
        avg_val = float(np.round(np.mean(marks), 2))
        min_val = float(np.min(marks))
        max_val = float(np.max(marks))
        subject_stats.append(
            {
                "Subject": subject.replace(" Marks", ""),
                "Average Marks": avg_val,
                "Minimum Marks": min_val,
                "Maximum Marks": max_val,
            }
        )

    return pd.DataFrame(subject_stats)


def get_top_students(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Retrieve top 'n' students ranked by Average Marks in descending order.

    Parameters:
        df (pd.DataFrame): Analyzed student DataFrame.
        n (int): Number of top performers to return.

    Returns:
        pd.DataFrame: Top n students.
    """
    sorted_df = df.sort_values(by=["Average Marks", "Total Marks"], ascending=False)
    return sorted_df.head(n).reset_index(drop=True)


def get_lowest_students(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """
    Retrieve lowest 'n' students ranked by Average Marks in ascending order.

    Parameters:
        df (pd.DataFrame): Analyzed student DataFrame.
        n (int): Number of lowest performers to return.

    Returns:
        pd.DataFrame: Lowest n students.
    """
    sorted_df = df.sort_values(by=["Average Marks", "Total Marks"], ascending=True)
    return sorted_df.head(n).reset_index(drop=True)


def analyze_attendance_impact(df: pd.DataFrame) -> Dict[str, any]:
    """
    Analyze student attendance and its relationship with performance.
    Categorizes attendance into:
      - High Attendance: >= 85%
      - Moderate Attendance: 75% to 84%
      - Low Attendance: < 75%

    Computes average performance for each band and Pearson correlation.

    Parameters:
        df (pd.DataFrame): Analyzed student DataFrame.

    Returns:
        Dict: Attendance brackets summary and correlation coefficient.
    """
    attendance = df["Attendance Percentage"].to_numpy()
    averages = df["Average Marks"].to_numpy()

    # Calculate Pearson Correlation Coefficient using NumPy
    if len(attendance) > 1 and np.std(attendance) > 0 and np.std(averages) > 0:
        correlation = float(np.round(np.corrcoef(attendance, averages)[0, 1], 3))
    else:
        correlation = 0.0

    # Categorize into attendance brackets
    brackets = []
    bands = [
        ("High (>= 85%)", attendance >= 85),
        ("Moderate (75% - 84%)", (attendance >= 75) & (attendance < 85)),
        ("Low (< 75%)", attendance < 75),
    ]

    for band_name, condition in bands:
        matching_students = df[condition]
        count = len(matching_students)
        avg_score = (
            float(np.round(np.mean(matching_students["Average Marks"].to_numpy()), 2))
            if count > 0
            else 0.0
        )
        pass_rate = (
            float(
                np.round(
                    (
                        np.sum(matching_students["Result"].to_numpy() == "Pass")
                        / count
                    )
                    * 100,
                    2,
                )
            )
            if count > 0
            else 0.0
        )
        brackets.append(
            {
                "Attendance Category": band_name,
                "Student Count": count,
                "Average Marks": avg_score,
                "Pass Rate (%)": pass_rate,
            }
        )

    return {
        "correlation": correlation,
        "brackets_df": pd.DataFrame(brackets),
    }


def filter_students(
    df: pd.DataFrame,
    name_query: Optional[str] = None,
    department: Optional[str] = None,
    grade: Optional[str] = None,
    result: Optional[str] = None,
) -> pd.DataFrame:
    """
    Filter student records based on search query, department, grade, and result.

    Parameters:
        df (pd.DataFrame): Analyzed student DataFrame.
        name_query (str, optional): Substring to search in student Name or ID.
        department (str, optional): Specific department or 'All'.
        grade (str, optional): Specific grade or 'All'.
        result (str, optional): 'Pass', 'Fail', or 'All'.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    filtered = df.copy()

    # Filter by Name or ID search
    if name_query and name_query.strip():
        q = name_query.strip().lower()
        filtered = filtered[
            filtered["Name"].astype(str).str.lower().str.contains(q)
            | filtered["Student ID"].astype(str).str.lower().str.contains(q)
        ]

    # Filter by Department
    if department and department != "All":
        filtered = filtered[filtered["Department"] == department]

    # Filter by Grade
    if grade and grade != "All":
        filtered = filtered[filtered["Grade"] == grade]

    # Filter by Result
    if result and result != "All":
        filtered = filtered[filtered["Result"] == result]

    return filtered.reset_index(drop=True)


def export_results_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Save analyzed student DataFrame to a CSV file.

    Parameters:
        df (pd.DataFrame): Analyzed DataFrame.
        output_path (str): Destination file path.
    """
    df.to_csv(output_path, index=False)
