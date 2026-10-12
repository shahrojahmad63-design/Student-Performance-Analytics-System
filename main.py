"""
main.py
=======
Student Performance Analytics System (CLI Application)
Analyzes student performance using Python, NumPy, and Pandas.
Designed for college viva demonstration and easy command-line execution.
"""

import os
import sys
import pandas as pd
import numpy as np

# Import functions from functions.py
from functions import (
    load_dataset,
    validate_student_data,
    calculate_student_results,
    calculate_class_summary,
    calculate_subject_averages,
    get_top_students,
    get_lowest_students,
    analyze_attendance_impact,
    export_results_to_csv,
    filter_students,
)


def print_header(title: str) -> None:
    """Print an attractive, clean section header."""
    separator = "=" * 65
    print(f"\n{separator}")
    print(f"  {title.upper()}")
    print(separator)


def display_table(df: pd.DataFrame) -> None:
    """Display a Pandas DataFrame in clean tabular format."""
    print(df.to_string(index=False))


def run_analytics_cli(csv_path: str = "students.csv") -> None:
    """
    Main function to execute complete student performance analytics
    from the command line.
    """
    print("=" * 65)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("     Powered by Python 3, NumPy, and Pandas")
    print("=" * 65)

    # 1. Check if dataset exists
    if not os.path.exists(csv_path):
        # Also check relative to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_path = os.path.join(script_dir, csv_path)
        if os.path.exists(alt_path):
            csv_path = alt_path
        else:
            print(f"\n[ERROR] File not found: '{csv_path}'")
            print("Please ensure students.csv exists in the project folder.")
            return

    print(f"\n[INFO] Loading dataset from: {csv_path}")

    # 2. Load dataset
    try:
        raw_df = load_dataset(csv_path)
        print(f"[SUCCESS] Loaded {len(raw_df)} student records.")
    except Exception as e:
        print(f"[ERROR] Failed to read CSV file: {e}")
        return

    # 3. Data Validation
    print("\n[INFO] Validating dataset integrity...")
    is_valid, errors, validated_df = validate_student_data(raw_df)

    if not is_valid:
        print("\n[VALIDATION WARNINGS / ERRORS FOUND]:")
        for err in errors:
            print(f"  - {err}")
        print("\nProceeding with available clean data where possible...")
    else:
        print("[SUCCESS] All data validation checks passed perfectly!")

    # 4. Performance Calculations (NumPy & Pandas)
    analyzed_df = calculate_student_results(validated_df)

    # 5. Class Summary Metrics
    print_header("1. Class Summary & Overview")
    summary = calculate_class_summary(analyzed_df)

    print(f"Total Students Enrolled : {summary['total_students']}")
    print(f"Overall Class Average   : {summary['class_average']:.2f} / 100")
    print(f"Passed Students Count   : {summary['passed_count']} ({summary['pass_percentage']}%)")
    print(f"Failed Students Count   : {summary['failed_count']} ({summary['fail_percentage']}%)")

    high_stud = summary["highest_student"]
    low_stud = summary["lowest_student"]
    if high_stud:
        print(f"Highest Performer       : {high_stud['Name']} (ID: {high_stud['Student ID']}, Dept: {high_stud['Department']}) - Avg: {high_stud['Average Marks']}%, Grade: {high_stud['Grade']}")
    if low_stud:
        print(f"Lowest Performer        : {low_stud['Name']} (ID: {low_stud['Student ID']}, Dept: {low_stud['Department']}) - Avg: {low_stud['Average Marks']}%, Grade: {low_stud['Grade']}")

    # 6. Subject-Wise Statistics
    print_header("2. Subject-Wise Performance (NumPy Analysis)")
    subj_df = calculate_subject_averages(analyzed_df)
    display_table(subj_df)

    # 7. Top 3 and Top 5 Performers
    print_header("3. Top 3 Students (Hall of Fame)")
    top_3_df = get_top_students(analyzed_df, n=3)[
        ["Student ID", "Name", "Department", "Average Marks", "Total Marks", "Grade"]
    ]
    display_table(top_3_df)

    print_header("4. Top 5 Students")
    top_5_df = get_top_students(analyzed_df, n=5)[
        ["Student ID", "Name", "Department", "Average Marks", "Total Marks", "Grade"]
    ]
    display_table(top_5_df)

    # 8. Lowest Performers
    print_header("5. Students Needing Academic Support (Lowest 3)")
    low_3_df = get_lowest_students(analyzed_df, n=3)[
        ["Student ID", "Name", "Department", "Average Marks", "Result", "Grade", "Attendance Percentage"]
    ]
    display_table(low_3_df)

    # 9. Attendance vs Performance Analysis
    print_header("6. Attendance vs Performance Correlation")
    att_results = analyze_attendance_impact(analyzed_df)
    corr = att_results["correlation"]
    print(f"Pearson Correlation (Attendance vs Avg Marks): {corr:+0.3f}")
    if corr > 0.5:
        print("Insight: Strong positive correlation - High attendance strongly correlates with high marks.")
    elif corr > 0:
        print("Insight: Moderate positive correlation - Regular attendance aids academic performance.")
    else:
        print("Insight: Low correlation between attendance and marks.")

    print("\nAttendance Category Breakdown:")
    display_table(att_results["brackets_df"])

    # 10. Grade Distribution
    print_header("7. Grade Distribution Summary")
    grade_counts = analyzed_df["Grade"].value_counts().sort_index()
    for grade, count in grade_counts.items():
        pct = (count / len(analyzed_df)) * 100
        bar = "█" * int(pct // 5)
        print(f"Grade {grade:2s} : {count:2d} students ({pct:5.1f}%) | {bar}")

    # 11. Department-Wise Summary
    print_header("8. Department-Wise Performance Summary")
    dept_summary = (
        analyzed_df.groupby("Department")
        .agg(
            Student_Count=("Student ID", "count"),
            Avg_Marks=("Average Marks", "mean"),
            Pass_Count=("Result", lambda r: (r == "Pass").sum()),
        )
        .reset_index()
    )
    dept_summary["Pass_Rate_%"] = (
        (dept_summary["Pass_Count"] / dept_summary["Student_Count"]) * 100
    ).round(2)
    dept_summary["Avg_Marks"] = dept_summary["Avg_Marks"].round(2)
    display_table(dept_summary)

    # 12. Full Records Preview
    print_header("9. Complete Analyzed Student Records (First 10)")
    preview_cols = [
        "Student ID",
        "Name",
        "Department",
        "Python Marks",
        "Maths Marks",
        "English Marks",
        "Total Marks",
        "Average Marks",
        "Grade",
        "Result",
    ]
    display_table(analyzed_df[preview_cols].head(10))

    # 13. Export Analyzed Data
    output_filename = "analyzed_students_output.csv"
    output_path = os.path.join(os.path.dirname(os.path.abspath(csv_path)), output_filename)
    export_results_to_csv(analyzed_df, output_path)
    print_header("10. Export Status")
    print(f"[SUCCESS] Complete analyzed dataset saved to: {output_filename}")
    print("=" * 65)
    print(" Analytics execution complete! Thank you for using the system.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    # Allow custom dataset file via command line argument: python main.py custom.csv
    input_file = sys.argv[1] if len(sys.argv) > 1 else "students.csv"
    run_analytics_cli(input_file)
