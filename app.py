import streamlit as st
import pandas as pd
import numpy as np
import time
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="UCC HIM Level 200 Hub", page_icon="🎓", layout="wide")

# Persistent light/dark mode state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- 2. SIDEBAR NAVIGATION PANEL ---
if os.path.exists("OIP.webp"):
    st.sidebar.image("OIP.webp", use_container_width=True)
else:
    st.sidebar.markdown("<h2 style='color:#FF4B4B; font-weight:700; margin:0;'>🏥 HIMSA UCC</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='font-size:22px; font-weight:600; margin-top:5px; color:#FF4B4B;'>UCC HIM Portal</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#64748B; font-size:14px; margin-top:-15px;'>Level 200 - Semester 2</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# CLEAR, CONFUSION-FREE NAVIGATION PANEL HEADER
st.sidebar.markdown("<h3 style='font-size:16px; font-weight:700; letter-spacing:0.5px; color:#FF4B4B; margin-bottom:5px;'>📋 NAVIGATION PANEL</h3>", unsafe_allow_html=True)

app_mode = st.sidebar.radio(
    "Choose a session to navigate:",
    [
        "📚 Course Material Distribution", 
        "🏥 ICD-10 Coding Practice",
        "📝 Adaptive Quiz Arena", 
        "⏱️ Mock Exam Simulator",
        "📋 Group Project Workspace",
        "📊 Personal Academic Analytics",
        "🏆 Student Leaderboard Pool"
    ]
)

st.sidebar.markdown("---")
st.session_state.dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode Layout")

# --- 3. MOCK EXAM COUNTER ACTION BLOCK ---
# We instantiate the timer system straight inside the navigation block so it persists visually across operations
if "exam_start_time" in st.session_state and st.session_state.exam_start_time is not None:
    elapsed = time.time() - st.session_state.exam_start_time
    remaining = max(0, int(1200 - elapsed)) # 20 minutes countdown
    if remaining > 0:
        mins, secs = divmod(remaining, 60)
        st.sidebar.error(f"⏱️ MOCK EXAM LIVE TIME: {mins:02d}:{secs:02d}")
    else:
        st.sidebar.error("🚨 TIME EXPIRED! Please submit your script.")

# --- 4. THEME STYLE INJECTION (SAFE - NO GLOBAL OVERRIDES) ---
if st.session_state.dark_mode:
    bg_color = "#0F172A"       # Dark Slate
    card_bg = "#1E293B"        # Lighter Card Slate
    border_color = "#334155"   # Dark Border
    heading_color = "#F8FAFC"  # White Text
else:
    bg_color = "#FFFFFF"       # Pure White
    card_bg = "#F8FAFC"        # Light Gray Card
    border_color = "#E2E8F0"   # Light Border
    heading_color = "#0F172A"  # Dark Charcoal Text

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {bg_color};
        font-family: 'Inter', sans-serif;
    }}
    .main-title {{ 
        font-size: 34px; 
        font-weight: 700; 
        color: #FF4B4B; 
        letter-spacing: -0.5px;
        margin-bottom: 5px;
    }}
    .section-subtitle {{
        font-size: 16px;
        color: #64748B;
        margin-bottom: 25px;
    }}
    .course-card {{ 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #FF4B4B; 
        margin-bottom: 20px; 
        background-color: {card_bg};
        border-top: 1px solid {border_color};
        border-right: 1px solid {border_color};
        border-bottom: 1px solid {border_color};
    }}
    .pool-banner {{
        background: linear-gradient(135deg, #FF4B4B 0%, #991B1B 100%);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
    }}
    </style>
""", unsafe_allow_html=True)


# --- 5. INITIALIZE STATE HOOKS ---
if "quiz_level" not in st.session_state: st.session_state.quiz_level = "Medium"
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "active_student" not in st.session_state: st.session_state.active_student = None
if "competition_pool" not in st.session_state: st.session_state.competition_pool = {}
if "exam_start_time" not in st.session_state: st.session_state.exam_start_time = None

# Group Project default values tracking persistence
if "group_tasks" not in st.session_state:
    st.session_state.group_tasks = {
        i: [False, False, False, False] for i in range(1, 10)
    }


# --- MODULE 1: COURSE MATERIAL DISTRIBUTION ---
if app_mode == "📚 Course Material Distribution":
    st.markdown("<h1 class='main-title'>📚 Courseware Repository</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Access core reference sheets, lecture slide decks, and module mappings.</p>", unsafe_allow_html=True)
    st.write("---")
    
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
    
    st.markdown(f"<div class='course-card'><h3 style='margin:0; font-weight:600; color:{heading_color};'>Current Portal: {course_selection}</h3></div>", unsafe_allow_html=True)
    
    if "HIM 212" in course_selection:
        st.markdown(f"<h4 style='color:{heading_color}; font-weight:600;'>Handouts & Slide Decks</h4>", unsafe_allow_html=True)
        files = ["1. WEEK 1_Python Functions_May 2026.pdf", "WEEK4_Introduction to GUI Programs (2).pptx", "PROGRAMMING AND SOFTWARE DEV. II_HIM 212_OUTLINE_May_2026 (2).pdf", "Python GUI Programming_P2_JUNE2025 (2).pptx"]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 212 Lecture Content Stub.")
            with open(f, "rb") as b_file: st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f)

    elif "HIM 208" in course_selection:
        st.markdown(f"<h4 style='color:{heading_color}; font-weight:600;'>Presentation Media</h4>", unsafe_allow_html=True)
        files = ["CANCER.pptx", "diet-and-health-ppt-1114he3 (3).pptx", "Fever-HIM NEW (2).pptx", "Introduction to Pathophysiology I.ppt"]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 208 Lecture Content Stub.")
            with open(f, "rb") as b_file: st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f)

    elif "HIM 204" in course_selection:
        st.markdown(f"<h4 style='color:{heading_color}; font-weight:600;'>Database Architecture Handouts</h4>", unsafe_allow_html=True)
        files = ["HIM 204 LECTURE 1 - INTRODUCTION TO DBMS (3).pdf", "HIM 204 LECTURE 2 - DBMS ARCHITECTURE (2).pdf", "HIM 204 LECTURE 3 - ENTITY RELATION MODEL.pdf", "HIM 204 LECTURE 4 - WORKING WITH ER DIAGRAMS.pdf", "HIM 204 LECTURE 5 - NORMALIZATION IN DBMS.pdf", "HIM 204 LECTURE 6 - NORMAL FORMS.pdf"]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 204 Lecture Content Stub.")
            with open(f, "rb") as b_file: st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f)
    else:
        st.warning("🔄 Module connection standby. Files are ready for retrieval.")


# --- BRAND NEW MODULE 2: INTERACTIVE ICD-10 CODING PRACTICE BOARD ---
elif app_mode == "🏥 ICD-10 Coding Practice":
    st.markdown("<h1 class='main-title'>🏥 Interactive ICD-10 Coding Practice Board</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Read the extracted clinical case scenarios and enter the exact alphanumeric code blocks.</p>", unsafe_allow_html=True)
    st.write("---")
    
    scenarios = [
        {"case": "Patient admitted with acute cholecystitis with cholelithiasis", "answer": "K80.0"},
        {"case": "Inpatient case presenting acute respiratory failure with chronic obstructive pulmonary disease exacerbation", "answer": "J44.1"},
        {"case": "Clinical diagnosis entry tracking acute amoebic dysentery with intestinal outcropping", "answer": "A06.0"}
    ]
    
    for idx, sc in enumerate(scenarios):
        st.markdown(f"<div class='course-card'><p style='font-size:16px; font-weight:600; color:{heading_color};'>📋 Case Note {idx+1}: {sc['case']}</p></div>", unsafe_allow_html=True)
        user_code_ans = st.text_input(f"Type Alphanumeric Code Block for Case {idx+1}:", key=f"icd_{idx}", placeholder="e.g. K80.0")
        
        if user_code_ans:
            if user_code_ans.strip().upper() == sc['answer']:
                st.success(f"🎯 Match Validated! Correct entry across Volume maps.")
            else:
                st.error(f"❌ Structural mismatch. Review the index guidelines.")


# --- MODULE 3: ADAPTIVE QUIZ ARENA ---
elif app_mode == "📝 Adaptive Quiz Arena":
    st.markdown("<h1 class='main-title'>📝 Multi-Level Adaptive Revision Arena</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.active_student is None:
        st.warning("⚠️ Access Denied: Create an identity inside the 'Student Leaderboard Pool' tab first!")
    else:
        st.info(f"👤 Competitor: **{st.session_state.active_student}** | Score: `{st.session_state.quiz_score}`")
        topic = st.selectbox("🎯 Select Subject Matrix", ["HIM 212: Programming II", "HIM 208: Pathophysiology II"])
        
        current_lvl = st.session_state.quiz_level
        st.markdown(f"<h4 style='color:{heading_color}; font-weight:600;'>Tier: <span style='color:#FF4B4B;'>{current_lvl}</span></h4>", unsafe_allow_html=True)

        quiz_data = {
            "HIM 212: Programming II": {
                "Medium": {"q": "In Python, which keyword defines a reusable code block function?", "o": ["func", "def", "lambda"], "c": "def"},
                "Intermediate": {"q": "Which Tkinter tool organizes components into rows and columns?", "o": ["pack()", "place()", "grid()"], "c": "grid()"},
                "Super Difficult": {"q": "What mechanism avoids data corruption inside SQLite multi-user paths?", "o": ["Transaction WAL isolation", "Callbacks", "Widget binding"], "c": "Transaction WAL isolation"}
            },
            "HIM 208: Pathophysiology II": {
                "Medium": {"q": "What characteristic distinguishes Gram-positive cell structures?", "o": ["Thin lipids", "Thick peptidoglycan layer", "Outer coat"], "c": "Thick peptidoglycan layer"},
                "Intermediate": {"q": "Which pattern relies on a virus vector injecting genetic sequences?", "o": ["Transduction", "Conjugation", "Transformation"], "c": "Transduction"},
                "Super Difficult": {"q": "Which component works straight on preoptic hypothalamus maps to spike set-points?", "o": ["Interleukin-1", "Prostaglandin E2 (PGE2)", "TNF"], "c": "Prostaglandin E2 (PGE2)"}
            }
        }

        q = quiz_data[topic][current_lvl]
        ans = st.radio(f"❓ Question: {q['q']}", q['o'])
        
        if st.button("🚀 Process Choice"):
            if ans == q['c']:
                st.success("🎯 Masterful! Match correct.")
                st.session_state.quiz_score += 50
                st.session_state.competition_pool[st.session_state.active_student] = {"Score (pts)": st.session_state.quiz_score, "Highest Tier": current_lvl}
                if current_lvl == "Medium": st.session_state.quiz_level = "Intermediate"
                elif current_lvl == "Intermediate": st.session_state.quiz_level = "Super Difficult"
                st.rerun()
            else:
                st.error("❌ Incorrect path. Try again!")


# --- BRAND NEW MODULE 4: TIMED MOCK EXAM SIMULATOR ---
elif app_mode == "⏱️ Mock Exam Simulator":
    st.markdown("<h1 class='main-title'>⏱️ Timed Mock Exam Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Simulate genuine UCC E-learning conditions. Finish a 20-minute comprehensive mock assembly block.</p>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.exam_start_time is None:
        if st.button("🏁 Trigger & Launch Exam Counter"):
            st.session_state.exam_start_time = time.time()
            st.rerun()
    else:
        st.info("🔥 Live assessment block activated! Check the timer tracking block in the navigation panel.")
        
        # Pulling structured testing cards across core paths
        st.markdown("<h3 style='color:#FF4B4B;'>Examination Block Questions</h3>", unsafe_allow_html=True)
        st.radio("Q1: Which layout schema establishes a standard column structure within database tables?", ["1NF", "Foreign Configuration", "Normalization Schema"], key="m_q1")
        st.radio("Q2: Which specialized cellular pattern defines fastidious structures?", ["Enriched agar reliance", "Simple sugar usage", "Binary isolation fields"], key="m_q2")
        st.radio("Q3: What logic path defines an Ad Hominem structural error?", ["Premise mismatch", "Character targeting attack", "Slippery Slope tracking"], key="m_q3")
        
        if st.button("📤 Finalize & Submit Exam Paper"):
            st.session_state.exam_start_time = None
            st.success("🎉 Scripts saved securely to administrative portal archives!")
            st.rerun()


# --- BRAND NEW MODULE 5: COLLABORATIVE GROUP PROJECT WORKSPACE HUB ---
elif app_mode == "📋 Group Project Workspace":
    st.markdown("<h1 class='main-title'>📋 Collaborative Group Project Workspace Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Track delivery milestones and architectural items across the assigned Level 200 groups.</p>", unsafe_allow_html=True)
    st.write("---")
    
    g_num = st.selectbox("🎯 Select Your Active Class Group Number:", [f"Group {i}" for i in range(1, 10)])
    g_idx = int(g_num.split(" ")[1])
    
    group_topics = {
        1: "Patient Admission Tracker (GUI)", 2: "Clinic Queue System", 3: "Health Record Matrix Map",
        4: "ICD-10 Diagnostic Parsing App", 5: "Medical Inventory Dashboard", 6: "Pharmacy Control Portal",
        7: "Patient Visit Analytics System (Visual Spread)", 8: "Laboratory Result Entry System (Tkinter + SQLite)",
        9: "Simple Health Information Web App (Flask + SQLite)"
    }
    
    st.markdown(f"<div class='course-card'><h3 style='margin:0; color:{heading_color};'>Assigned Goal: {group_topics[g_idx]}</h3></div>", unsafe_allow_html=True)
    
    st.markdown("#### Track Functional Milestones Checklist:")
    t0 = st.checkbox("⚙️ Database Schema Definition & SQLite Node Setup", value=st.session_state.group_tasks[g_idx][0])
    t1 = st.checkbox("🎨 Tkinter / Interface Component Positioning Build", value=st.session_state.group_tasks[g_idx][1])
    t2 = st.checkbox("📊 Analytics Graph Plotter Dashboard Incorporation", value=st.session_state.group_tasks[g_idx][2])
    t3 = st.checkbox("🔒 Basic Authentication Security & Login Logic Integration", value=st.session_state.group_tasks[g_idx][3])
    
    if st.button("💾 Store Group Milestone Blueprint"):
        st.session_state.group_tasks[g_idx] = [t0, t1, t2, t3]
        st.success(f"Saved update metrics for Group {g_idx} project matrix!")


# --- MODULE 6: PERSONAL ACADEMIC ANALYTICS TRACKER ---
elif app_mode == "📊 Personal Academic Analytics":
    st.markdown("<h1 class='main-title'>📊 Personal CGPA & Semester Goal Targeter</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Calculate the target course performance you need to achieve your second-semester goals.</p>", unsafe_allow_html=True)
    st.write("---")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        prev_cgpa = st.number_input("📈 Enter Previous Semesters' CGPA:", min_value=0.0, max_value=4.0, value=3.2, step=0.01)
    with col_in2:
        target_gpa = st.number_input("🎯 Enter Target GPA for This Semester:", min_value=0.0, max_value=4.0, value=3.3, step=0.01)
        
    st.write("---")
    st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>Target Action Plan Checklist</h3>", unsafe_allow_html=True)
    
    if target_gpa >= 3.6:
        grade_advice = "Solid 'A' grades (80%+ / 4.0 GP)"
        alert_status = st.success
    elif target_gpa >= 3.0:
        grade_advice = "A mix of 'B+' and 'B' grades (70-79% / 3.0-3.5 GP)"
        alert_status = st.info
    else:
        grade_advice = "Steady 'C+' or standard pass blocks (60-69%)"
        alert_status = st.warning
        
    alert_status(f"💡 **Analysis Strategy:** To safely raise your metrics and reach a **{target_gpa} GPA**, you should aim for an average benchmark of: **{grade_advice}** across your courses.")


# --- MODULE 7: LEADERBOARD RANKING POOL ---
elif app_mode == "🏆 Student Leaderboard Pool":
    st.markdown("<h1 class='main-title'>🏆 Live Roster Competition Pool</h1>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("""
        <div class='pool-banner'>
            <h3 style='margin:0 0 5px 0; font-weight:600; color:#FFFFFF;'>📝 Active Profile Entrance</h3>
            <p style='margin:0; opacity:0.9; font-size:14px; color:#FFFFFF;'>Enter your student identity alias to open an active tracking scorecard stream!</p>
        </div>
    """, unsafe_allow_html=True)
    
    join_col1, join_col2 = st.columns([3, 1])
    with join_col1:
        chosen_name = st.text_input("👤 Enter Full Student Name or Custom Alias Token:", placeholder="e.g. Mohammed Issifu")
    with join_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Establish Pool Account", use_container_width=True):
            if chosen_name.strip() != "":
                clean_name = chosen_name.strip()
                st.session_state.active_student = clean_name
                if clean_name not in st.session_state.competition_pool:
                    st.session_state.competition_pool[clean_name] = {"Score (pts)": 0, "Highest Tier": "Medium"}
                st.success(f"🎉 Session profile locked to: **{clean_name}**.")
                st.rerun()
                
    st.write("---")
    
    if len(st.session_state.competition_pool) == 0:
        st.info("📊 The competition pool is currently empty. Add your profile name to log points!")
    else:
        pool_records = [{"Student Name": name, "Score (pts)": data["Score (pts)"], "Highest Tier": data["Highest Tier"]} for name, data in st.session_state.competition_pool.items()]
        df_pool = pd.DataFrame(pool_records).sort_values(by="Score (pts)", ascending=False).reset_index(drop=True)
        df_pool.index += 1  
        
        col_board, col_chart = st.columns([1, 1])
        with col_board:
            st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>📊 Active Standing Board</h3>", unsafe_allow_html=True)
            st.dataframe(df_pool, use_container_width=True)
        with col_chart:
            st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>📈 Class Ranking Visual Spread</h3>", unsafe_allow_html=True)
            st.bar_chart(data=df_pool, x="Student Name", y="Score (pts)", color="#FF4B4B")
