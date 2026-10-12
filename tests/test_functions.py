"""
test_functions.py
=================
Unit tests for functions.py in the Student Performance Analytics System.
Using Python's built-in unittest framework.
"""

import unittest
import pandas as pd
import numpy as np

from functions import (
    assign_grade,
    calculate_student_results,
    calculate_class_summary,
    calculate_subject_averages,
    get_top_students,
    get_lowest_students,
    analyze_attendance_impact,
    filter_students,
    validate_student_data,
)


class TestStudentAnalytics(unittest.TestCase):
    def setUp(self):
        """Create sample data fixture for testing."""
        self.sample_data = pd.DataFrame(
            [
                {
                    "Student ID": 1,
                    "Name": "Student A",
                    "Department": "Computer Science",
                    "Python Marks": 95,
                    "Maths Marks": 92,
                    "English Marks": 90,
                    "Attendance Percentage": 95,
                },
                {
                    "Student ID": 2,
                    "Name": "Student B",
                    "Department": "Data Science",
                    "Python Marks": 85,
                    "Maths Marks": 80,
                    "English Marks": 82,
                    "Attendance Percentage": 90,
                },
                {
                    "Student ID": 3,
                    "Name": "Student C",
                    "Department": "Computer Science",
                    "Python Marks": 75,
                    "Maths Marks": 70,
                    "English Marks": 72,
                    "Attendance Percentage": 82,
                },
                {
                    "Student ID": 4,
                    "Name": "Student D",
                    "Department": "Information Technology",
                    "Python Marks": 35,  # Fails in Python (<40)
                    "Maths Marks": 85,
                    "English Marks": 90,
                    "Attendance Percentage": 65,
                },
                {
                    "Student ID": 5,
                    "Name": "Student E",
                    "Department": "Data Science",
                    "Python Marks": 45,
                    "Maths Marks": 42,
                    "English Marks": 48,
                    "Attendance Percentage": 70,
                },
            ]
        )

    def test_assign_grade(self):
        """Test grade assignments across all score boundaries and fail status."""
        self.assertEqual(assign_grade(95.0, "Pass"), "A+")
        self.assertEqual(assign_grade(90.0, "Pass"), "A+")
        self.assertEqual(assign_grade(85.5, "Pass"), "A")
        self.assertEqual(assign_grade(80.0, "Pass"), "A")
        self.assertEqual(assign_grade(75.0, "Pass"), "B")
        self.assertEqual(assign_grade(65.0, "Pass"), "C")
        self.assertEqual(assign_grade(55.0, "Pass"), "D")
        self.assertEqual(assign_grade(45.0, "Pass"), "E")
        self.assertEqual(assign_grade(35.0, "Pass"), "F")
        # Failing any subject forces Grade F even if average is high
        self.assertEqual(assign_grade(85.0, "Fail"), "F")

    def test_calculate_student_results(self):
        """Test calculation of total marks, average, pass/fail result, and grades."""
        analyzed = calculate_student_results(self.sample_data)

        # Student A: 95 + 92 + 90 = 277, avg = 92.33, Pass, A+
        student_a = analyzed.loc[analyzed["Student ID"] == 1].iloc[0]
        self.assertEqual(student_a["Total Marks"], 277)
        self.assertAlmostEqual(student_a["Average Marks"], 92.33, places=2)
        self.assertEqual(student_a["Result"], "Pass")
        self.assertEqual(student_a["Grade"], "A+")

        # Student D: scored 35 in Python -> Must Fail and receive grade F despite avg 70.0
        student_d = analyzed.loc[analyzed["Student ID"] == 4].iloc[0]
        self.assertEqual(student_d["Total Marks"], 210)
        self.assertAlmostEqual(student_d["Average Marks"], 70.0, places=2)
        self.assertEqual(student_d["Result"], "Fail")
        self.assertEqual(student_d["Grade"], "F")

        # Student E: scored 45, 42, 48 -> Passed with Grade E
        student_e = analyzed.loc[analyzed["Student ID"] == 5].iloc[0]
        self.assertEqual(student_e["Result"], "Pass")
        self.assertEqual(student_e["Grade"], "E")

    def test_calculate_class_summary(self):
        """Test summary statistics calculation."""
        analyzed = calculate_student_results(self.sample_data)
        summary = calculate_class_summary(analyzed)

        self.assertEqual(summary["total_students"], 5)
        self.assertEqual(summary["passed_count"], 4)
        self.assertEqual(summary["failed_count"], 1)
        self.assertEqual(summary["pass_percentage"], 80.0)
        self.assertEqual(summary["fail_percentage"], 20.0)
        self.assertEqual(summary["highest_student"]["Name"], "Student A")
        self.assertEqual(summary["lowest_student"]["Name"], "Student E")

    def test_calculate_subject_averages(self):
        """Test subject averages calculation."""
        stats = calculate_subject_averages(self.sample_data)
        self.assertEqual(len(stats), 3)
        subjects = stats["Subject"].tolist()
        self.assertIn("Python", subjects)
        self.assertIn("Maths", subjects)
        self.assertIn("English", subjects)

        # Python: [95, 85, 75, 35, 45] -> sum=335, avg=67.0
        python_stat = stats.loc[stats["Subject"] == "Python"].iloc[0]
        self.assertEqual(python_stat["Average Marks"], 67.0)
        self.assertEqual(python_stat["Minimum Marks"], 35.0)
        self.assertEqual(python_stat["Maximum Marks"], 95.0)

    def test_get_top_and_lowest_students(self):
        """Test ranking functions."""
        analyzed = calculate_student_results(self.sample_data)
        top_2 = get_top_students(analyzed, n=2)
        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2.iloc[0]["Student ID"], 1)
        self.assertEqual(top_2.iloc[1]["Student ID"], 2)

        lowest_1 = get_lowest_students(analyzed, n=1)
        self.assertEqual(len(lowest_1), 1)
        self.assertEqual(lowest_1.iloc[0]["Student ID"], 5)

    def test_analyze_attendance_impact(self):
        """Test attendance categorization and correlation."""
        analyzed = calculate_student_results(self.sample_data)
        att_results = analyze_attendance_impact(analyzed)

        self.assertIn("correlation", att_results)
        self.assertIn("brackets_df", att_results)
        brackets = att_results["brackets_df"]
        self.assertEqual(len(brackets), 3)

    def test_filter_students(self):
        """Test search and filter criteria."""
        analyzed = calculate_student_results(self.sample_data)

        # Search by name
        res_search = filter_students(analyzed, name_query="Student A")
        self.assertEqual(len(res_search), 1)
        self.assertEqual(res_search.iloc[0]["Name"], "Student A")

        # Filter by department
        res_dept = filter_students(analyzed, department="Data Science")
        self.assertEqual(len(res_dept), 2)

        # Filter by Result
        res_fail = filter_students(analyzed, result="Fail")
        self.assertEqual(len(res_fail), 1)
        self.assertEqual(res_fail.iloc[0]["Name"], "Student D")

    def test_validate_student_data_errors(self):
        """Test validation catches missing columns, duplicates, and out-of-range marks."""
        # 1. Missing column
        bad_df = pd.DataFrame([{"Student ID": 1, "Name": "Alice"}])
        is_valid, errors, _ = validate_student_data(bad_df)
        self.assertFalse(is_valid)
        self.assertTrue(any("Missing required column" in err for err in errors))

        # 2. Duplicate Student ID
        dup_df = self.sample_data.copy()
        dup_df.loc[1, "Student ID"] = 1  # Make ID 1 duplicate
        is_valid, errors, _ = validate_student_data(dup_df)
        self.assertFalse(is_valid)
        self.assertTrue(any("Duplicate Student ID" in err for err in errors))

        # 3. Invalid mark (> 100)
        invalid_mark_df = self.sample_data.copy()
        invalid_mark_df.loc[0, "Python Marks"] = 105
        is_valid, errors, _ = validate_student_data(invalid_mark_df)
        self.assertFalse(is_valid)
        self.assertTrue(any("outside the valid range" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
