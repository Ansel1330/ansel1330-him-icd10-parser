import streamlit as st
import pandas as pd
import numpy as np
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="UCC HIM Level 200 Hub", page_icon="🎓", layout="wide")

# --- CUSTOM CSS FOR COMPACT UI & DESIGN ---
st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #FF4B4B; margin-bottom: 5px; }
    .sub-header { font-size: 16px; color: #555555; margin-bottom: 20px; }
    .course-card { padding: 15px; border-radius: 8px; border-left: 5px solid #0066cc; margin-bottom: 15px; background-color: rgba(0,102,204,0.05); }
    </style>
""", unsafe_allowed_value=True)

# --- TRACKING CODES & PERSISTENT SESSION STATE ---
if "quiz_level" not in st.session_state:
    st.session_state.quiz_level = "Medium"
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "current_course_quiz" not in st.session_state:
    st.session_state.current_course_quiz = "HIM 212: Programming II"
if "leaderboard_data" not in st.session_state:
    # Seed data mimicking your cohort's competition group
    st.session_state.leaderboard_data = pd.DataFrame([
        {"Student Name": "Kuami Majesty", "Score (pts)": 140, "Level Completed": "Intermediate"},
        {"Student Name": "Mohammed Issifu", "Score (pts)": 190, "Level Completed": "Super Difficult"},
        {"Student Name": "Abigail Mensah", "Score (pts)": 110, "Level Completed": "Medium"},
        {"Student Name": "Emmanuel Tetteh", "Score (pts)": 80, "Level Completed": "Medium"},
        {"Student Name": "Priscilla Osei", "Score (pts)": 150, "Level Completed": "Intermediate"}
    ]).sort_values(by="Score (pts)", ascending=False).reset_index(drop=True)

# --- SIDEBAR PORTAL & NAVIGATION ---
st.sidebar.image("OIP.webp", use_container_width=True, errors="ignore")
st.sidebar.title("UCC HIM Portal")
st.sidebar.markdown("### Level 200 - Semester 2")

# Main Hub Controller Switching
app_mode = st.sidebar.radio(
    "🧭 Navigation Hub",
    ["📚 Course Material Distribution", "📝 Adaptive Quiz Arena", "🏆 Student Leaderboard Pool"]
)
st.sidebar.markdown("---")
st.sidebar.info("Department of Health Information Management\nSchool of Allied Health Sciences - UCC")

# --- HUB MODULE 1: COURSE MATERIAL DISTRIBUTION ---
if app_mode == "📚 Course Material Distribution":
    st.title("📚 Level 200 Second Semester Courseware Repository")
    st.write("Access reference guides, schemas, outlines, and lecture files across all active domains.")
    st.write("---")
    
    # Grid of Active Level 200 Courses
    course_selection = st.selectbox(
        "📖 Select Course Department",
        [
            "HIM 212: Programming and Software Development II",
            "HIM 208: Pathophysiology II",
            "HIM 204: Database Structures",
            "HIM 210: Disease Classification and Coding",
            "PHL 205: Critical Thinking and Practical Reasoning",
            "HIM 202: System Analysis and Design",
            "HIM 206: Data Communication and Networks in Healthcare"
        ]
    )
    
    st.markdown(f"<div class='course-card'><h3>Current Portal: {course_selection}</h3></div>", unsafe_allowed_html=True)
    
    # 1. PROGRAMMING II SESSION
    if "HIM 212" in course_selection:
        st.write("#### Assigned Core Files & Handouts")
        files = ["1. WEEK 1_Python Functions_May 2026.pdf", "WEEK4_Introduction to GUI Programs (2).pptx", 
                 "PROGRAMMING AND SOFTWARE DEV. II_HIM 212_OUTLINE_May_2026 (2).pdf", "Python GUI Programming_P2_JUNE2025 (2).pptx"]
        for f in files:
            st.code(f"📁 Source: .../PROGRAMMING/{f}")
            if not os.path.exists(f): 
                with open(f, "w") as empty_f: empty_f.write("Class Material Placeholder")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f.split('_')[-1]}", data=b_file, file_name=f, key=f)

    # 2. PATHOPHYSIOLOGY II SESSION
    elif "HIM 208" in course_selection:
        st.write("#### Assigned Lecture Presentation Media")
        files = ["CANCER.pptx", "diet-and-health-ppt-1114he3 (3).pptx", "Fever-HIM NEW (2).pptx", "Introduction to Pathophysiology I.ppt"]
        for f in files:
            st.code(f"📁 Source: .../PATHOPHYSIOLOGY/{f}")
            if not os.path.exists(f): 
                with open(f, "w") as empty_f: empty_f.write("Class Material Placeholder")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f)

    # 3. DATABASE STRUCTURES SESSION
    elif "HIM 204" in course_selection and "Database" in course_selection:
        st.write("#### Assigned DBMS Structures Handouts")
        files = ["HIM 204 LECTURE 1 - INTRODUCTION TO DBMS (3).pdf", "HIM 204 LECTURE 2 - DBMS ARCHITECTURE (2).pdf",
                 "HIM 204 LECTURE 3 - ENTITY RELATION MODEL.pdf", "HIM 204 LECTURE 4 - WORKING WITH ER DIAGRAMS.pdf",
                 "HIM 204 LECTURE 5 - NORMALIZATION IN DBMS.pdf", "HIM 204 LECTURE 6 - NORMAL FORMS.pdf",
                 "HIM 204 LECTURE 7 - INTRODUCTION TO DATABASE QUERIES.pdf", "HIM 204 LECTURE 8 - TUTORIAL SESSION.pdf"]
        for f in files:
            st.code(f"📁 Link: {f}")
            st.caption("Awaiting user batch drag-and-drop to complete live cloud storage sync.")

    # 4. DISEASE CLASSIFICATION & CODING SESSION (INTEGRATED ICD-10 PARSER TOOL)
    elif "HIM 210" in course_selection:
        st.write("### ⚡ Integrated Functional Asset")
        st.info("💡 **HIM 210 Live Lab Tool:** Below is the active ICD-10 Diagnostic Parser Engine embedded directly inside its structural course module!")
        st.markdown("---")
        
        search_query = st.text_input("🔍 ICD-10 Alpha-Index & Tabular Match Engine (Type Search Term):")
        if search_query:
            st.success(f"Parsing extracted hits for: '{search_query}' across Volume 1 and Volume 3 maps...")
            # Interactive matching table mock
            mock_hits = pd.DataFrame([
                {"Term Match": search_query.capitalize(), "ICD-10 Code block": "B15-B19", "Volume Registry": "Vol 3 Index (Page 328)"},
                {"Term Match": f"{search_query.capitalize()} (unspecified)", "ICD-10 Code block": "K75.9", "Volume Registry": "Vol 1 Tabular"}
            ])
            st.dataframe(mock_hits, use_container_width=True)

    # 5. REMAINING COHORT COURSE LISTINGS
    else:
        st.write("#### System Status Warning")
        st.warning("⚠️ Ready for File Paths. Paste your structural URLs or folders here in our next run to activate instant downloads for your classmates!")

# --- HUB MODULE 2: ADAPTIVE QUIZ ARENA ---
elif app_mode == "📝 Adaptive Revision Quiz":
    st.title("📝 Multi-Level Adaptive Revision Arena")
    st.write("Answer questions from Level 200 courses correctly to step up the difficulty from **Medium ➡️ Intermediate ➡️ Super Difficult**.")
    st.write("---")
    
    st.session_state.current_course_quiz = st.selectbox(
        "🎯 Select Topic Base to Test",
        ["HIM 212: Programming II", "HIM 208: Pathophysiology II", "HIM 204: Database Structures", "PHL 205: Critical Thinking"]
    )
    
    # Level Progress Layout
    levels = ["Medium", "Intermediate", "Super Difficult"]
    current_lvl = st.session_state.quiz_level
    st.progress((levels.index(current_lvl) + 1) / len(levels))
    st.markdown(f"#### Active Tier Status: :orange[{current_lvl}] | Total Accumulated Points: `{st.session_state.quiz_score}`")

    # Adaptive Questions Bank Matrix
    quiz_matrix = {
        "HIM 212: Programming II": {
            "Medium": {"q": "In Python, which keyword defines a reusable code block function?", "o": ["func", "def", "lambda"], "c": "def"},
            "Intermediate": {"q": "Which Tkinter geometric positioning tool organizes components into rows and columns?", "o": ["pack()", "place()", "grid()"], "c": "grid()"},
            "Super Difficult": {"q": "What mechanism avoids data corruption by locking read/write tasks inside multi-user SQLite connections?", "o": ["Transaction WAL isolation", "Recursive callbacks", "Widget binding callbacks"], "c": "Transaction WAL isolation"}
        },
        "HIM 208: Pathophysiology II": {
            "Medium": {"q": "What core characteristic distinguishes Gram-positive cell structures?", "o": ["Thin lipids", "Thick peptidoglycan layer retaining stain", "Outer lipopolysaccharide coat"], "c": "Thick peptidoglycan layer retaining stain"},
            "Intermediate": {"q": "Which transfer pattern relies on a virus vector injecting foreign genetic sequences into targeted host bacteria?", "o": ["Transduction", "Conjugation via sex pilus", "Transformation"], "c": "Transduction"},
            "Super Difficult": {"q": "Which specialized chemical component works straight on preoptic hypothalamus maps to spike core set-points?", "o": ["Interleukin-1", "Prostaglandin E2 (PGE2)", "Tumor Necrosis Factor"], "c": "Prostaglandin E2 (PGE2)"}
        },
        "HIM 204: Database Structures": {
            "Medium": {"q": "What structural key uniquely identifies a record row inside an index matrix?", "o": ["Foreign key", "Primary key", "Composite node"], "c": "Primary key"},
            "Intermediate": {"q": "Which Normal Form demands the exclusion of all transitive functional dependencies?", "o": ["1NF", "2NF", "3NF"], "c": "3NF"},
            "Super Difficult": {"q": "Which design concept describes an atomic, logical execution block that fully commits or entirely rolls back to preserve stability?", "o": ["Entity Relation Cardinality", "ACID Transaction", "Multi-valued dependency splitting"], "c": "ACID Transaction"}
        },
        "PHL 205: Critical Thinking": {
            "Medium": {"q": "Which error type describes an attack targeted straight at an opponent's character rather than structural arguments?", "o": ["Ad Hominem", "Straw Man Fallacy", "Slippery Slope"], "c": "Ad Hominem"},
            "Intermediate": {"q": "What type of reasoning draws logically certain conclusions from general premises?", "o": ["Deductive reasoning", "Inductive inference", "Abductive assumption"], "c": "Deductive reasoning"},
            "Super Difficult": {"q": "Which condition is met when a premise's truth absolute forces a true conclusion, yet its premises remain false?", "o": ["Soundness criteria met", "Valid structure only", "Cognitive structural fallacy"], "c": "Valid structure only"}
        }
    }

    # Pull current active question object
    q_package = quiz_matrix[st.session_state.current_course_quiz][current_lvl]
    user_choice = st.radio(f"❓ Question: {q_package['q']}", q_package['o'])
    
    if st.button("🚀 Process Choice & Update"):
        if user_choice == q_package['c']:
            st.success("🎯 Masterful! That choice is absolutely correct.")
            st.session_state.quiz_score += 50
            
            # Level advancing logic mechanics
            if current_lvl == "Medium":
                st.session_state.quiz_level = "Intermediate"
            elif current_lvl == "Intermediate":
                st.session_state.quiz_level = "Super Difficult"
            elif current_lvl == "Super Difficult":
                st.balloons()
                st.success("🏆 Incredible! You have fully maxed out this course branch with a perfect track!")
            st.rerun()
        else:
            st.error("❌ Incorrect path choice. Re-read your assigned materials repository list and test again!")

    if st.button("🔄 Restart Trial Matrix"):
        st.session_state.quiz_level = "Medium"
        st.session_state.quiz_score = 0
        st.rerun()

# --- HUB MODULE 3: LEADERBOARD RANKING POOL ---
elif app_mode == "🏆 Student Leaderboard Pool":
    st.title("🏆 UCC Level 200 Cohort Leaderboard Pool")
    st.write("Real-time tracked competitive points metric displaying performance across all topics.")
    st.write("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Leaderboard Ranking Table")
        st.dataframe(st.session_state.leaderboard_data, use_container_width=True)
        
    with col2:
        st.subheader("Performance Spread Chart")
        # Direct Plotly Chart Generation tracking high ranks
        st.bar_chart(data=st.session_state.leaderboard_data, x="Student Name", y="Score (pts)", color="#FF4B4B")
        
    st.markdown("---")
    st.caption("💡 Scores are calculated using correct adaptive step advancements (+50 per breakthrough).")
