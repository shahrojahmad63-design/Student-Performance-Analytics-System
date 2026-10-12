"""
app.py
======
Student Performance Analytics System - Streamlit Web Dashboard
Modern, responsive, beginner-friendly analytics interface.
Utilizes reusable business logic and calculations from functions.py.
"""

import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import reusable logic from functions.py
from functions import (
    load_dataset,
    validate_student_data,
    calculate_student_results,
    calculate_class_summary,
    calculate_subject_averages,
    get_top_students,
    get_lowest_students,
    analyze_attendance_impact,
    filter_students,
    REQUIRED_COLUMNS,
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom Styling for Modern Dashboard
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 22px;
        color: #f8fafc;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 4px;
    }
    .metric-subtitle {
        font-size: 0.8rem;
        color: #cbd5e1;
    }
    .status-pass {
        color: #22c55e;
        font-weight: 600;
    }
    .status-fail {
        color: #ef4444;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State & Dataset Loading
# ---------------------------------------------------------
DEFAULT_CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "students.csv"
)

# Sidebar: Dataset Selection & Upload
st.sidebar.title("🎓 Navigation")
st.sidebar.markdown("**Student Performance Analytics**")

dataset_source = st.sidebar.radio(
    "Choose Dataset Source:",
    ["Use Default Sample Data", "Upload Custom CSV"],
)

active_df = None
validation_errors = []
is_valid_data = False

if dataset_source == "Upload Custom CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Upload a Student CSV File", type=["csv"]
    )
    if uploaded_file is not None:
        try:
            raw_uploaded = load_dataset(uploaded_file)
            is_valid_data, validation_errors, validated_df = validate_student_data(
                raw_uploaded
            )
            if is_valid_data:
                active_df = calculate_student_results(validated_df)
                st.sidebar.success(f"Loaded {len(active_df)} student records!")
            else:
                st.sidebar.error("Dataset validation failed. See Upload page.")
                active_df = calculate_student_results(validated_df)
        except Exception as e:
            st.sidebar.error(f"Error reading uploaded file: {e}")
    else:
        st.sidebar.info("Upload a CSV file to begin analysis.")
else:
    # Load default dataset
    if os.path.exists(DEFAULT_CSV_PATH):
        raw_default = load_dataset(DEFAULT_CSV_PATH)
        is_valid_data, validation_errors, validated_df = validate_student_data(
            raw_default
        )
        active_df = calculate_student_results(validated_df)
    else:
        st.error(f"Default dataset not found at {DEFAULT_CSV_PATH}")

# Sidebar Navigation Pages
page = st.sidebar.selectbox(
    "Go to Module:",
    [
        "📊 Overview & Summary",
        "📋 Student Records & Filter",
        "📈 Subject-wise Analysis",
        "🏆 Top & Bottom Performers",
        "⏱️ Attendance vs Performance",
        "📥 Upload & Export Dataset",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Python with AI Mini Project | Streamlit Dashboard")

# ---------------------------------------------------------
# Helper Component: Metric Card
# ---------------------------------------------------------
def render_metric_card(title: str, value: str, subtitle: str = ""):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtitle">{subtitle}</div>
    </div>
    """


# ---------------------------------------------------------
# Main Page Router
# ---------------------------------------------------------
if active_df is None:
    st.title("🎓 Student Performance Analytics System")
    st.warning("Please upload a valid CSV file from the sidebar to continue.")
    st.stop()

# =========================================================
# MODULE 1: Overview & Summary
# =========================================================
if page == "📊 Overview & Summary":
    st.title("🎓 Student Performance Analytics System")
    st.markdown(
        "Analyze student marks, evaluate subject proficiencies, calculate pass/fail status, "
        "and explore attendance impact using **NumPy** and **Pandas**."
    )

    summary = calculate_class_summary(active_df)

    # Metric Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            render_metric_card(
                "Total Students",
                f"{summary['total_students']}",
                "Registered students",
            ),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            render_metric_card(
                "Class Average",
                f"{summary['class_average']:.1f}%",
                "Average score out of 100",
            ),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            render_metric_card(
                "Passed Count",
                f"{summary['passed_count']} / {summary['total_students']}",
                f"{summary['pass_percentage']}% Pass Rate (Cutoff: ≥40)",
            ),
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            render_metric_card(
                "Failed Count",
                f"{summary['failed_count']} / {summary['total_students']}",
                f"{summary['fail_percentage']}% Failed in ≥1 subject",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Star Performers Highlight
    col_high, col_low = st.columns(2)
    with col_high:
        st.subheader("🌟 Highest Performing Student")
        h = summary["highest_student"]
        if h:
            st.info(
                f"**Name:** {h['Name']}  \n"
                f"**ID:** {h['Student ID']} | **Department:** {h['Department']}  \n"
                f"**Average Marks:** {h['Average Marks']}% | **Total:** {h['Total Marks']}/300  \n"
                f"**Grade:** `{h['Grade']}` | **Status:** `{h['Result']}`"
            )

    with col_low:
        st.subheader("⚠️ Lowest Performing Student")
        l = summary["lowest_student"]
        if l:
            st.warning(
                f"**Name:** {l['Name']}  \n"
                f"**ID:** {l['Student ID']} | **Department:** {l['Department']}  \n"
                f"**Average Marks:** {l['Average Marks']}% | **Total:** {l['Total Marks']}/300  \n"
                f"**Grade:** `{l['Grade']}` | **Attendance:** {l['Attendance Percentage']}%"
            )

    st.markdown("---")

    # Distribution Charts
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("📊 Grade Distribution")
        grade_order = ["A+", "A", "B", "C", "D", "E", "F"]
        grade_counts = (
            active_df["Grade"]
            .value_counts()
            .reindex(grade_order, fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(6, 3.8))
        colors = ["#22c55e", "#10b981", "#38bdf8", "#facc15", "#fb923c", "#f87171", "#ef4444"]
        bars = ax.bar(grade_counts.index, grade_counts.values, color=colors, edgecolor="#0f172a", width=0.6)
        ax.set_ylabel("Number of Students", fontsize=10)
        ax.set_xlabel("Assigned Grade", fontsize=10)
        ax.set_title("Student Count per Letter Grade", fontsize=11, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(
                    f"{int(height)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )
        st.pyplot(fig)

    with chart_col2:
        st.subheader("🎯 Pass vs Fail Distribution")
        res_counts = active_df["Result"].value_counts()
        fig_pie, ax_pie = plt.subplots(figsize=(6, 3.8))
        pie_colors = ["#22c55e" if k == "Pass" else "#ef4444" for k in res_counts.index]
        ax_pie.pie(
            res_counts.values,
            labels=res_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=pie_colors,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            textprops={"fontsize": 11, "fontweight": "bold"},
        )
        ax_pie.set_title("Pass vs Fail Proportion", fontsize=11, fontweight="bold")
        st.pyplot(fig_pie)

# =========================================================
# MODULE 2: Student Records & Filter
# =========================================================
elif page == "📋 Student Records & Filter":
    st.title("📋 Student Records & Search")
    st.markdown("Filter records by student name, ID, department, grade, or pass/fail result.")

    # Filter Controls
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.2, 1, 1])

    with f_col1:
        search_query = st.text_input("🔍 Search by Student Name or ID:", placeholder="e.g. Aarav or 101")
    with f_col2:
        dept_options = ["All"] + sorted(active_df["Department"].dropna().unique().tolist())
        selected_dept = st.selectbox("Department:", dept_options)
    with f_col3:
        grade_options = ["All"] + ["A+", "A", "B", "C", "D", "E", "F"]
        selected_grade = st.selectbox("Grade:", grade_options)
    with f_col4:
        result_options = ["All", "Pass", "Fail"]
        selected_result = st.selectbox("Result Status:", result_options)

    # Apply Filter
    filtered_df = filter_students(
        active_df,
        name_query=search_query,
        department=selected_dept,
        grade=selected_grade,
        result=selected_result,
    )

    st.write(f"Showing **{len(filtered_df)}** of **{len(active_df)}** students:")

    # Highlight table
    def highlight_status(val):
        if val == "Pass":
            return "background-color: #dcfce7; color: #166534; font-weight: bold;"
        elif val == "Fail":
            return "background-color: #fee2e2; color: #991b1b; font-weight: bold;"
        return ""

    display_cols = [
        "Student ID",
        "Name",
        "Department",
        "Python Marks",
        "Maths Marks",
        "English Marks",
        "Total Marks",
        "Average Marks",
        "Attendance Percentage",
        "Grade",
        "Result",
    ]

    styler = filtered_df[display_cols].style
    if hasattr(styler, "map"):
        styled_df = styler.map(highlight_status, subset=["Result"])
    else:
        styled_df = styler.applymap(highlight_status, subset=["Result"])
    st.dataframe(styled_df, use_container_width=True)

# =========================================================
# MODULE 3: Subject-wise Analysis
# =========================================================
elif page == "📈 Subject-wise Analysis":
    st.title("📈 Subject-Wise Performance Analysis")
    st.markdown("Evaluate subject-wise class averages, minimum scores, and maximum scores.")

    subject_df = calculate_subject_averages(active_df)

    col1, col2 = st.columns([1.2, 2])
    with col1:
        st.subheader("Summary Table")
        st.dataframe(subject_df, use_container_width=True)

        st.info(
            "**Key Findings:**\n"
            f"- Highest Scoring Subject: **{subject_df.loc[subject_df['Average Marks'].idxmax(), 'Subject']}**\n"
            f"- Lowest Scoring Subject: **{subject_df.loc[subject_df['Average Marks'].idxmin(), 'Subject']}**"
        )

    with col2:
        st.subheader("Average Marks by Subject")
        fig, ax = plt.subplots(figsize=(6, 3.6))
        bars = ax.bar(
            subject_df["Subject"],
            subject_df["Average Marks"],
            color=["#3b82f6", "#10b981", "#8b5cf6"],
            width=0.5,
        )
        ax.set_ylim(0, 100)
        ax.set_ylabel("Average Marks (out of 100)")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        for bar in bars:
            h = bar.get_height()
            ax.annotate(
                f"{h:.1f}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                fontweight="bold",
            )
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("Subject Marks Boxplot (Spread & Outliers)")
    fig_box, ax_box = plt.subplots(figsize=(8, 3.8))
    marks_data = [
        active_df["Python Marks"].dropna(),
        active_df["Maths Marks"].dropna(),
        active_df["English Marks"].dropna(),
    ]
    boxplot_kwargs = dict(
        patch_artist=True,
        boxprops=dict(facecolor="#e0f2fe", color="#0284c7"),
        medianprops=dict(color="#0369a1", linewidth=2),
    )
    try:
        ax_box.boxplot(marks_data, tick_labels=["Python", "Maths", "English"], **boxplot_kwargs)
    except TypeError:
        ax_box.boxplot(marks_data, labels=["Python", "Maths", "English"], **boxplot_kwargs)
    ax_box.set_ylabel("Marks (0-100)")
    ax_box.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig_box)

# =========================================================
# MODULE 4: Top & Bottom Performers
# =========================================================
elif page == "🏆 Top & Bottom Performers":
    st.title("🏆 Academic Performance Rankings")
    st.markdown("Recognize student excellence and identify candidates requiring extra tutoring.")

    tab_top3, tab_top5, tab_low = st.tabs(["Top 3 Performers", "Top 5 Performers", "Bottom 3 Performers"])

    with tab_top3:
        st.subheader("🥇 Top 3 Students (Academic Excellence)")
        top_3 = get_top_students(active_df, n=3)
        cols = st.columns(3)
        medals = ["🥇 1st Place", "🥈 2nd Place", "🥉 3rd Place"]
        for idx, col in enumerate(cols):
            if idx < len(top_3):
                row = top_3.iloc[idx]
                with col:
                    st.markdown(
                        render_metric_card(
                            medals[idx],
                            row["Name"],
                            f"Avg: {row['Average Marks']}% | Grade: {row['Grade']} | Dept: {row['Department']}",
                        ),
                        unsafe_allow_html=True,
                    )
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(top_3[["Student ID", "Name", "Department", "Total Marks", "Average Marks", "Grade", "Result"]])

    with tab_top5:
        st.subheader("Top 5 Students by Average Marks")
        top_5 = get_top_students(active_df, n=5)

        fig, ax = plt.subplots(figsize=(7, 3.5))
        y_pos = np.arange(len(top_5))
        ax.barh(y_pos, top_5["Average Marks"], color="#38bdf8", edgecolor="#0284c7")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_5["Name"])
        ax.invert_yaxis()  # Highest at the top
        ax.set_xlabel("Average Marks (%)")
        ax.set_xlim(0, 105)
        for i, v in enumerate(top_5["Average Marks"]):
            ax.text(v + 1, i, f"{v}% (Grade {top_5.iloc[i]['Grade']})", va="center", fontweight="bold")
        st.pyplot(fig)

        st.dataframe(top_5[["Student ID", "Name", "Department", "Python Marks", "Maths Marks", "English Marks", "Average Marks", "Grade"]])

    with tab_low:
        st.subheader("Students Requiring Academic Attention")
        low_3 = get_lowest_students(active_df, n=3)
        st.warning("These students scored lowest overall or failed one or more subjects:")
        st.dataframe(low_3[["Student ID", "Name", "Department", "Average Marks", "Result", "Grade", "Attendance Percentage"]])

# =========================================================
# MODULE 5: Attendance vs Performance
# =========================================================
elif page == "⏱️ Attendance vs Performance":
    st.title("⏱️ Attendance vs Academic Performance")
    st.markdown("Investigate how attendance percentage impacts student marks and pass rates.")

    att_results = analyze_attendance_impact(active_df)
    corr = att_results["correlation"]

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(
            render_metric_card(
                "Pearson Correlation",
                f"{corr:+0.3f}",
                "Attendance vs Marks Correlation",
            ),
            unsafe_allow_html=True,
        )
        if corr > 0.6:
            st.success("Strong positive link: higher attendance correlates with higher average marks.")
        elif corr > 0.3:
            st.info("Moderate positive correlation between regular attendance and student marks.")
        else:
            st.warning("Low or negative correlation in this dataset.")

        st.subheader("Attendance Categories")
        st.dataframe(att_results["brackets_df"], use_container_width=True)

    with c2:
        st.subheader("Scatter Plot: Attendance vs Average Marks")
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ["#22c55e" if r == "Pass" else "#ef4444" for r in active_df["Result"]]
        ax.scatter(
            active_df["Attendance Percentage"],
            active_df["Average Marks"],
            c=colors,
            s=70,
            edgecolors="#1e293b",
            alpha=0.85,
        )
        # Add regression trendline if enough points
        x = active_df["Attendance Percentage"].to_numpy()
        y = active_df["Average Marks"].to_numpy()
        if len(x) > 2 and np.std(x) > 0:
            m, b = np.polyfit(x, y, 1)
            ax.plot(x, m * x + b, color="#0284c7", linestyle="--", linewidth=2, label="Trendline")
            ax.legend()

        ax.set_xlabel("Attendance Percentage (%)")
        ax.set_ylabel("Average Marks (%)")
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig)

# =========================================================
# MODULE 6: Upload & Export Dataset
# =========================================================
elif page == "📥 Upload & Export Dataset":
    st.title("📥 Dataset Management: Upload & Export")

    # CSV Upload Section
    st.subheader("1. Upload Custom Dataset")
    st.markdown(
        "Upload your own CSV file. The system will automatically validate columns, "
        "check for duplicate IDs, missing values, and mark ranges."
    )

    user_file = st.file_uploader("Upload CSV", type=["csv"], key="page_uploader")
    if user_file is not None:
        try:
            uploaded_df = load_dataset(user_file)
            valid, errs, clean_df = validate_student_data(uploaded_df)
            if valid:
                st.success("Data validation passed! No critical errors found.")
                st.dataframe(clean_df.head(), use_container_width=True)
            else:
                st.error("Validation issues found:")
                for e in errs:
                    st.write(f"❌ {e}")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    st.markdown("---")

    # CSV Export Section
    st.subheader("2. Download Analyzed Dataset")
    st.markdown(
        "Download the current analyzed results (including Total Marks, Average Marks, "
        "Letter Grades, and Pass/Fail status) as a CSV file."
    )

    # Convert DataFrame to CSV buffer
    csv_buffer = io.StringIO()
    active_df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    st.download_button(
        label="📥 Download Analyzed Results (CSV)",
        data=csv_bytes,
        file_name="student_performance_analyzed.csv",
        mime="text/csv",
        help="Click to download the processed dataset.",
    )

    st.markdown("---")
    st.subheader("Preview of Data to be Exported")
    st.dataframe(active_df, use_container_width=True)
