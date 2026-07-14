import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from student import Student

# Page Config
st.set_page_config(
    page_title="Helix Academics | Grade Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphic Theme accents)
st.markdown("""
    <style>
    .main {
        background-color: #0f111a;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 28px !important;
        font-weight: 700;
        color: #00ffcc !important;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
    }
    .metric-title {
        color: #8a90a6;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-val {
        color: #00ffcc;
        font-size: 26px;
        font-weight: bold;
    }
    .report-card {
        background: rgba(255, 255, 255, 0.02);
        border: 2px solid rgba(0, 255, 204, 0.2);
        border-radius: 16px;
        padding: 30px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Backend Instance
if 'db' not in st.session_state:
    st.session_state.db = Student()

db = st.session_state.db

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>🎓 HELIX ACADEMICS</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    menu = st.radio(
        "Navigation",
        ["Dashboard & Directory", "Student Management", "Academics & Grades", "Analytics Hub"],
        index=0
    )
    st.markdown("<br><br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.caption("Helix Student Grade Management System v2.1")

# ==================== MENU 1: DASHBOARD & DIRECTORY ====================
if menu == "Dashboard & Directory":
    st.markdown("<h1 style='color: white;'>System Overview</h1>", unsafe_allow_html=True)
    
    # Calculate Metrics
    stats = db.stats()
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>TOTAL ENROLLMENTS</div><div class='metric-val'>{stats['Total Students']}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>CLASS AVERAGE SCORE</div><div class='metric-val'>{stats['Average']}%</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>OVERALL PASS RATE</div><div class='metric-val'>{stats['Pass Rate']}%</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>TOP PERFORMING %</div><div class='metric-val'>{stats['Highest']}%</div></div>", unsafe_allow_html=True)
    else:
        st.info("No statistics available. Please add students first.")

    st.markdown("<h3 style='margin-top: 30px; color: white;'>Student Search & Directory</h3>", unsafe_allow_html=True)
    
    if db.data:
        # Clean, full-width search input bar
        search_query = st.text_input(
            "🔍 Search Student Profile", 
            placeholder="Type Name or Roll Number (e.g., Islam Khan or 382CO)...",
            key="directory_search"
        ).strip()
        
        df = pd.DataFrame(db.data)
        
        # Determine if we should show results
        if search_query:
            # Filter matches
            df_filtered = df[df['name'].str.contains(search_query, case=False) | df['roll_no'].str.contains(search_query, case=False)]
            
            if not df_filtered.empty:
                st.markdown(f"🚦 Showing **{len(df_filtered)}** matching profile(s):")
                # Flatten marks to a clean text representation for tabular preview
                df_filtered['subjects_enrolled'] = df_filtered['marks'].apply(lambda x: ", ".join(x.keys()) if x else "None")
                df_display = df_filtered[['roll_no', 'name', 'age', 'course', 'percentage', 'grade', 'subjects_enrolled']].copy()
                df_display.columns = ['Roll Number', 'Full Name', 'Age', 'Course Track', 'Overall %', 'Grade', 'Enrolled Subjects']
                
                st.dataframe(
                    df_display, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "Overall %": st.column_config.ProgressColumn("Overall %", format="%.2f%%", min_value=0, max_value=100)
                    }
                )
            else:
                st.error(f"No records found matching query: '{search_query}'")
        else:
            # Welcome banner/state when no active search is inputted
            st.info("💡 Enter a student's **Name** or **Roll Number** above to retrieve their academic profile and details.")
    else:
        st.info("No registered students found in the database. Head over to the 'Student Management' tab to add records.")
# ==================== MENU 2: STUDENT MANAGEMENT ====================
elif menu == "Student Management":
    st.markdown("<h1 style='color: white;'>Student Management Portal</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🆕 Register Student", "✏️ Update Student Bio", "❌ Remove Record"])

    # TAB 1: REGISTER STUDENT
    with tab1:
        st.subheader("Register a New Student Profile")
        with st.form("add_student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Student's Full Name", placeholder="e.g., Jane Doe")
                course = st.text_input("Academic Course Track", placeholder="e.g., B. Tech. Data Science")
            with col2:
                age = st.number_input("Student's Age", min_value=15, max_value=100, value=19, step=1)
            
            submit_btn = st.form_submit_button("Generate & Register Profile")
            
            if submit_btn:
                if name.strip() == "" or course.strip() == "":
                    st.error("Submission blocked: Student name and course fields cannot be empty.")
                else:
                    new_student = db.add_student(name.strip(), age, course.strip())
                    st.success(f"Successfully Registered! assigned Roll Number: **{new_student['roll_no']}**")

    # TAB 2: UPDATE BIOGRAPHICAL DETAILS (With verification step)
    with tab2:
        st.subheader("Modify Student Demographics")
        v_roll = st.text_input("Enter Roll Number to Modify", placeholder="e.g., 382CO", key="update_verify_roll").upper()
        
        if v_roll:
            student = db.get(v_roll)
            if student:
                st.markdown(f"🧬 **Verified Student Found:** `{student['name']}` | `{student['course']}`")
                
                with st.form("update_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Updated Name", value=student['name'])
                        new_course = st.text_input("Updated Course", value=student['course'])
                    with col2:
                        new_age = st.number_input("Updated Age", min_value=15, max_value=100, value=int(student['age']))
                    
                    update_btn = st.form_submit_button("Apply Demographic Changes")
                    if update_btn:
                        success = db.update(v_roll, name=new_name.strip(), age=new_age, course=new_course.strip())
                        if success:
                            st.success(f"Profile records updated for Roll No: {v_roll}")
            else:
                st.error("No verified profile matches this Roll Number.")

    # TAB 3: REMOVE RECORD (With verification step)
    with tab3:
        st.subheader("De-register Student Record")
        del_roll = st.text_input("Enter Roll Number to Remove", placeholder="e.g., 570DD", key="del_verify_roll").upper()
        
        if del_roll:
            student = db.get(del_roll)
            if student:
                st.warning(f"⚠️ **Action Required:** You are about to permanently delete **{student['name']}** (Course: {student['course']}). All associated academic grade history will be purged.")
                
                col_btn1, col_btn2 = st.columns([1, 4])
                with col_btn1:
                    confirm_del = st.button("Delete Permanently", type="primary")
                
                if confirm_del:
                    if db.delete(del_roll):
                        st.success(f"Student record for Roll No: **{del_roll}** was deleted.")
                        st.rerun()
            else:
                st.error("No verified profile matches this Roll Number.")

# ==================== MENU 3: ACADEMICS & GRADES ====================
elif menu == "Academics & Grades":
    st.markdown("<h1 style='color: white;'>Academics & Grading</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📝 Grade Input Console", "🗑️ Remove Subject Mark", "📄 Report Card Generator"])

    # TAB 1: ADD MARKS
    with tab1:
        st.subheader("Record Subject Grade Points")
        grade_roll = st.text_input("Verify Roll Number", placeholder="e.g., 382CO", key="grade_verify_roll").upper()
        
        if grade_roll:
            student = db.get(grade_roll)
            if student:
                st.markdown(f"✅ **Identity Confirmed:** `{student['name']}` ({student['course']})")
                
                with st.form("grades_entry_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        subject = st.text_input("Subject Area Name", placeholder="e.g., Advanced Mathematics")
                    with col2:
                        marks = st.number_input("Numerical Score achieved (0 - 100)", min_value=0, max_value=100, value=75, step=1)
                    
                    submit_grades = st.form_submit_button("Record Subject Mark")
                    if submit_grades:
                        if not subject.strip():
                            st.error("Input Invalid: Please supply a non-empty Subject Area Name.")
                        else:
                            db.add_marks(grade_roll, subject.strip(), marks)
                            st.success(f"Recorded score of **{marks}** in **{subject}** for **{student['name']}**.")
            else:
                st.error("No verified profile matches this Roll Number.")

    # TAB 2: REMOVE SUBJECT MARK
    with tab2:
        st.subheader("Remove Subject Grade Points")
        rem_roll = st.text_input("Verify Roll Number for Correction", placeholder="e.g., 382CO", key="rem_verify_roll").upper()
        
        if rem_roll:
            student = db.get(rem_roll)
            if student:
                st.markdown(f"✅ **Identity Confirmed:** `{student['name']}` ({student['course']})")
                if student["marks"]:
                    subjects_list = list(student["marks"].keys())
                    sub_to_delete = st.selectbox("Select Subject to Remove", subjects_list)
                    
                    if st.button("Delete Mark Record", type="primary"):
                        if db.delete_mark(rem_roll, sub_to_delete):
                            st.success(f"Removed **{sub_to_delete}** mark record for **{student['name']}**.")
                            st.rerun()
                else:
                    st.info("No marked subjects exist for this student.")
            else:
                st.error("No verified profile matches this Roll Number.")

    # TAB 3: REPORT CARD GENERATOR
    with tab3:
        st.subheader("Generate Student Transcript")
        report_roll = st.text_input("Verify Student Roll Number", placeholder="e.g., 382CO", key="report_verify_roll").upper()
        
        if report_roll:
            student = db.get(report_roll)
            if student:
                st.success("Verified. Outputting Official Student Academic Performance Report:")
                
                # Dynamic calculation for Status (Pass/Fail) and corresponding color
                is_pass = student['percentage'] > 34
                status_text = "PASS" if is_pass else "FAIL"
                status_color = "#00ffcc" if is_pass else "#ff4b4b"  # Emerald green for pass, coral red for fail
                
                # Report Card Design Container
                st.markdown(f"""
                <div class="report-card">
                    <h2 style='text-align: center; color: #00ffcc; margin-bottom: 0px;'>HELIX INSTITUTIONAL TRANSCRIPT</h2>
                    <p style='text-align: center; color: #8a90a6; font-size:12px;'>ACADEMIC RECORDS DEPARTMENT</p>
                    <hr style='border-color: rgba(0, 255, 204, 0.3);'>
                    <div style='display: flex; justify-content: space-between; font-family: monospace; font-size: 14px;'>
                        <div>
                            <p><b>STUDENT:</b> {student['name'].upper()}</p>
                            <p><b>ROLL NO:</b> {student['roll_no']}</p>
                        </div>
                        <div style='text-align: right;'>
                            <p><b>ACADEMIC TRACK:</b> {student['course'].upper()}</p>
                            <p><b>AGE RECORDED:</b> {student['age']}</p>
                        </div>
                    </div>
                    <hr style='border-color: rgba(255, 255, 255, 0.05);'>
                </div>
                """, unsafe_allow_html=True)
                
                # Table breakdown inside UI 
                if student['marks']:
                    sub_df = pd.DataFrame(list(student['marks'].items()), columns=["Subject Module", "Obtained Grade Score"])
                    st.table(sub_df)
                    
                    # Flex container displaying Score, Grade, and the dynamic Status
                    st.markdown(f"""
                    <div class="report-card" style="margin-top: -10px;">
                        <div style='display: flex; justify-content: space-around; text-align: center;'>
                            <div>
                                <h4 style='color: #8a90a6; margin-bottom: 5px;'>AGGREGATE SCORE</h4>
                                <h1 style='color: #00ffcc; margin-top: 0px;'>{student['percentage']}%</h1>
                            </div>
                            <div>
                                <h4 style='color: #8a90a6; margin-bottom: 5px;'>FINAL GRADE ASSIGNED</h4>
                                <h1 style='color: #00ffcc; margin-top: 0px;'>{student['grade']}</h1>
                            </div>
                            <div>
                                <h4 style='color: #8a90a6; margin-bottom: 5px;'>STATUS</h4>
                                <h1 style='color: {status_color}; margin-top: 0px;'>{status_text}</h1>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Academic transcript is empty. Please enter module grade points for this student first.")
            else:
                st.error("No verified profile matches this Roll Number.")

# ==================== MENU 4: ANALYTICS HUB ====================
elif menu == "Analytics Hub":
    st.markdown("<h1 style='color: white;'>Analytics Hub & Insights</h1>", unsafe_allow_html=True)
    
    if db.data:
        df = pd.DataFrame(db.data)
        stats = db.stats()
        
        # ---------------- KPI CARDS SECTION ----------------
        st.markdown("<h3 style='color: white; margin-bottom: 15px;'>Academic Health Metrics</h3>", unsafe_allow_html=True)
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        
        with col_kpi1:
            st.markdown(
                f"""<div class='metric-card' style='border-top: 4px solid #00ffcc;'>
                    <div class='metric-title'>STUDENTS PASSED (>34%)</div>
                    <div class='metric-val' style='color: #00ffcc;'>{stats.get('Passed', 0)}</div>
                </div>""", 
                unsafe_allow_html=True
            )
        with col_kpi2:
            st.markdown(
                f"""<div class='metric-card' style='border-top: 4px solid #ff4b4b;'>
                    <div class='metric-title'>STUDENTS FAILED (≤34%)</div>
                    <div class='metric-val' style='color: #ff4b4b;'>{stats.get('Failed', 0)}</div>
                </div>""", 
                unsafe_allow_html=True
            )
        with col_kpi3:
            # Color-coded pass rate indicator
            pr_color = "#00ffcc" if stats.get('Pass Rate', 0) >= 60 else "#ff4b4b"
            st.markdown(
                f"""<div class='metric-card' style='border-top: 4px solid {pr_color};'>
                    <div class='metric-title'>OVERALL PASS RATE</div>
                    <div class='metric-val' style='color: {pr_color};'>{stats.get('Pass Rate', 0.0)}%</div>
                </div>""", 
                unsafe_allow_html=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- MAIN CHARTS SECTION ----------------
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Students per Grade Category")
            # Get clean counts of assigned letter grades
            grade_order = ['A', 'B', 'C', 'D', 'F']
            grade_counts = df['grade'].value_counts().reindex(grade_order, fill_value=0).reset_index()
            grade_counts.columns = ['Grade', 'Count']
            
            # Simplified bar chart
            fig_grades = px.bar(
                grade_counts, 
                x='Grade', 
                y='Count', 
                text='Count',
                labels={'Count': 'Number of Students', 'Grade': 'Letter Grade Assigned'},
                template="plotly_dark"
            )
            fig_grades.update_traces(
                marker_color='#00ffcc', 
                textposition='outside',
                cliponaxis=False
            )
            fig_grades.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title_font=dict(size=12))
            )
            st.plotly_chart(fig_grades, use_container_width=True)

        with col2:
            st.subheader("Class Success Ratio")
            # Donut chart representing Pass vs Fail proportion
            status_labels = ['Passed (Score >34)', 'Failed (Score ≤34)']
            status_values = [stats.get('Passed', 0), stats.get('Failed', 0)]
            
            # Fallback if there are zeros to avoid blank charts
            if sum(status_values) == 0:
                st.info("Add grade records to populate the Success Ratio.")
            else:
                fig_donut = go.Figure(data=[go.Pie(
                    labels=status_labels, 
                    values=status_values, 
                    hole=.5,
                    marker=dict(colors=['#00ffcc', '#ff4b4b']),
                    textinfo='percent+value'
                )])
                fig_donut.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_donut, use_container_width=True)

        # ---------------- SUBJECT ANALYTICS ----------------
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Average Score by Subject Field")
        
        # Re-structure marks data for clean plotting
        all_subjects_data = []
        for s in db.data:
            for sub, val in s["marks"].items():
                all_subjects_data.append({"Subject": sub, "Marks": val})
                
        if all_subjects_data:
            sub_df = pd.DataFrame(all_subjects_data)
            # Group and sort so the highest scoring subjects appear at the top
            avg_sub_df = sub_df.groupby("Subject")["Marks"].mean().reset_index().sort_values(by="Marks", ascending=True)
            
            # Clean horizontal bar chart
            fig_sub = px.bar(
                avg_sub_df, 
                x="Marks", 
                y="Subject", 
                orientation='h',
                text=avg_sub_df['Marks'].round(1),
                labels={'Marks': 'Average Percentage Score (%)', 'Subject': 'Course Subject'},
                template="plotly_dark"
            )
            fig_sub.update_traces(
                marker_color='#00ffcc',
                texttemplate='%{text}%',
                textposition='outside',
                cliponaxis=False
            )
            fig_sub.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 110]),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_sub, use_container_width=True)
        else:
            st.info("📊 Additional performance charts will display here once subject marks have been recorded.")
    else:
        st.info("Register active student profiles to configure institutional analytics pipelines.")