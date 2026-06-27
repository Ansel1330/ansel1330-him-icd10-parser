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

# --- 3. EXAM COUNTER ENGINE ---
if "exam_running" not in st.session_state:
    st.session_state.exam_running = False
if "exam_start_time" not in st.session_state:
    st.session_state.exam_start_time = None

if st.session_state.exam_running and st.session_state.exam_start_time is not None:
    elapsed = time.time() - st.session_state.exam_start_time
    remaining = max(0, int(1200 - elapsed)) # 20 Minute Countdown
    if remaining > 0:
        mins, secs = divmod(remaining, 60)
        st.sidebar.error(f"⏱️ MOCK EXAM TIME: {mins:02d}:{secs:02d}")
    else:
        st.sidebar.error("🚨 TIME EXPIRED! Examination block locked.")
        st.session_state.exam_running = False

# --- 4. THEME STYLE INJECTION ---
if st.session_state.dark_mode:
    bg_color = "#0F172A"       
    card_bg = "#1E293B"        
    border_color = "#334155"   
    heading_color = "#F8FAFC"  
else:
    bg_color = "#FFFFFF"       
    card_bg = "#F8FAFC"        
    border_color = "#E2E8F0"   
    heading_color = "#0F172A"  

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {{ background-color: {bg_color}; font-family: 'Inter', sans-serif; }}
    .main-title {{ font-size: 34px; font-weight: 700; color: #FF4B4B; letter-spacing: -0.5px; }}
    .section-subtitle {{ font-size: 16px; color: #64748B; margin-bottom: 25px; }}
    .course-card {{ padding: 20px; border-radius: 12px; border-left: 6px solid #FF4B4B; margin-bottom: 20px; background-color: {card_bg}; border-top:1px solid {border_color}; border-right:1px solid {border_color}; border-bottom:1px solid {border_color}; }}
    .pool-banner {{ background: linear-gradient(135deg, #FF4B4B 0%, #991B1B 100%); padding: 25px; border-radius: 16px; margin-bottom: 25px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. INITIALIZE STATE HOOKS ---
if "quiz_level" not in st.session_state: st.session_state.quiz_level = "Medium"
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "active_student" not in st.session_state: st.session_state.active_student = None
if "competition_pool" not in st.session_state: st.session_state.competition_pool = {}
if "group_tasks" not in st.session_state:
    st.session_state.group_tasks = {i: [False, False, False, False, False] for i in range(1, 10)}

# --- MODULE 1: COURSE MATERIAL DISTRIBUTION ---
if app_mode == "📚 Course Material Distribution":
    st.markdown("<h1 class='main-title'>📚 Courseware Repository</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Access reference sheets, lecture slides, and curriculum documentation.</p>", unsafe_allow_html=True)
    st.write("---")
    
    course_selection = st.selectbox(
        "📖 Select Course Department",
        [
            "HIM 212: Programming and Software Development II",
            "HIM 208: Pathophysiology II",
            "HIM 204: Database Structures",
            "HIM 210: Disease Classification and Coding"
        ]
    )
    st.markdown(f"<div class='course-card'><h3 style='margin:0; font-weight:600; color:{heading_color};'>Active Module: {course_selection}</h3></div>", unsafe_allow_html=True)
    
    if "HIM 212" in course_selection:
        files = ["1. WEEK 1_Python Functions_May 2026.pdf", "WEEK4_Introduction to GUI Programs (2).pptx", "PROGRAMMING AND SOFTWARE DEV. II_HIM 212_OUTLINE_May_2026 (2).pdf", "Python GUI Programming_P2_JUNE2025 (2).pptx"]
        for f in files:
            st.code(f"📁 Path: Repository/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 212 Material Block Asset.")
            with open(f, "rb") as b_file: st.download_button(label=f"📥 Download File: {f}", data=b_file, file_name=f, key=f"dl_{f}")
    elif "HIM 208" in course_selection:
        files = ["CANCER.pptx", "diet-and-health-ppt-1114he3 (3).pptx", "Fever-HIM NEW (2).pptx", "Introduction to Pathophysiology I.ppt"]
        for f in files:
            st.code(f"📁 Path: Repository/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 208 Material Block Asset.")
            with open(f, "rb") as b_file: st.download_button(label=f"📥 Download File: {f}", data=b_file, file_name=f, key=f"dl_{f}")
    else:
        st.info("💡 Standby. Upload department directory listings to populate live links.")

# --- MODULE 2: INTERACTIVE ICD-10 CODING PRACTICE BOARD ---
elif app_mode == "🏥 ICD-10 Coding Practice":
    st.markdown("<h1 class='main-title'>🏥 Advanced ICD-10 Clinical Coding Board</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Analyze specialized patient records. Enter the target alphanumeric blocks according to WHO/GHS guidelines.</p>", unsafe_allow_html=True)
    st.write("---")
    
    cases = [
        {"id": "EHR-802", "dept": "Gastroenterology", "narrative": "Patient presents with sharp right upper quadrant pain radiating to the scapula. Ultrasound confirms acute inflammation of the gallbladder walls concurrent with multiple impacted gallstones.", "target": "K80.0", "hint": "Acute cholecystitis with cholelithiasis"},
        {"id": "EHR-109", "dept": "Pulmonology", "narrative": "A 68-year-old female with long-standing emphysema admitted in respiratory distress. Arterial blood gases show hypercapnic respiratory failure triggered by an acute infective COPD exacerbation.", "target": "J44.1", "hint": "Chronic obstructive pulmonary disease with acute exacerbation"},
        {"id": "EHR-441", "dept": "Oncology", "narrative": "Pathology workup from a core needle biopsy of an upper-outer quadrant breast mass confirms infiltrating ductal carcinoma that has broken through the basement membrane.", "target": "C50.4", "hint": "Malignant neoplasm of upper-outer quadrant of breast"}
    ]
    
    for idx, c in enumerate(cases):
        with st.container():
            st.markdown(f"""
            <div class='course-card'>
                <span style='color:#FF4B4B; font-weight:700;'>[Chart No: {c['id']} - {c['dept']}]</span><br>
                <p style='color:{heading_color}; font-style:italic; margin-top:5px;'>"{c['narrative']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            u_ans = st.text_input(f"Assign Diagnostic Code (Tabular Vol 1) for Chart {c['id']}:", key=f"c_icd_{idx}", placeholder="e.g. A00.0").strip().upper()
            if u_ans:
                if u_ans == c['target']:
                    st.success("🎯 Diagnostic Map Validated! Code matches index parameters perfectly.")
                else:
                    st.error("❌ Mismatch detected. Cross-verify lead terms within Volume 3 index lists.")
            st.write(" ")

# --- MODULE 3: ADAPTIVE QUIZ ARENA ---
elif app_mode == "📝 Adaptive Quiz Arena":
    st.markdown("<h1 class='main-title'>📝 Adaptive Revision Arena</h1>", unsafe_allow_html=True)
    st.write("---")
    if st.session_state.active_student is None:
        st.warning("⚠️ Access Denied: Create an entry profile under the Leaderboard Pool tab first.")
    else:
        st.info(f"👤 Account: **{st.session_state.active_student}** | Revision Score: `{st.session_state.quiz_score}`")
        # Classic Adaptive Arena
        st.write("Step up the challenge layout systematically by validating answers.")

# --- MODULE 4: TIMED MOCK EXAM SIMULATOR (CLASSIC & ADVANCED) ---
elif app_mode == "⏱️ Mock Exam Simulator":
    st.markdown("<h1 class='main-title'>⏱️ Timed Mock Exam Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Classic UCC E-Learning simulator environment. No options pre-selected. Answer all parts before submitting.</p>", unsafe_allow_html=True)
    st.write("---")
    
    if not st.session_state.exam_running:
        st.warning("⏱️ The examination paper is currently sealed.")
        if st.button("🏁 Break Seal & Start 20-Minute Exam", type="primary"):
            st.session_state.exam_start_time = time.time()
            st.session_state.exam_running = True
            st.rerun()
    else:
        st.markdown("<h3 style='color:#FF4B4B; margin-bottom:20px;'>HIM Semester 2 Comprehensive Assessment Paper</h3>", unsafe_allow_html=True)
        
        # --- SECTION A: MULTIPLE CHOICE QUESTIONS (4 CHOICES - NO DEFAULT SELECT) ---
        st.markdown("#### 📝 Section A: Advanced Multiple Choice")
        
        q1_choice = st.radio(
            "Q1: In Tkinter GUI layouts, which method configuration must you execute to prevent code execution blocks from crashing when evaluating bad datatypes inside an age box or entry widget?",
            options=[None, "A) Using absolute pack structural geometries", "B) Encapsulating calculations with a clear try...except() input validation path", "C) Calling transactional bind_all() callbacks on the master node", "D) Forcing global variable overrides via root updates"],
            index=0,
            key="mcq_1"
        )
        
        q2_choice = st.radio(
            "Q2: Based on Pathophysiology II lecture modules, which specialized chemical mediator operates directly upon preoptic hypothalamic maps to raise the core thermal set-point?",
            options=[None, "A) Lipopolysaccharide Exogenous Pyrogens", "B) Prostaglandin E2 (PGE2)", "C) Interleukin-6 structural receptors", "D) Categorical Cortisone pathways"],
            index=0,
            key="mcq_2"
        )
        
        q3_choice = st.radio(
            "Q3: Inside relational database architectures (HIM 204), which structural form requires the absolute elimination of all transitive functional dependencies?",
            options=[None, "A) First Normal Form (1NF)", "B) Second Normal Form (2NF)", "C) Third Normal Form (3NF)", "D) Boyce-Codd Normal Form (BCNF)"],
            index=0,
            key="mcq_3"
        )
        
        q4_choice = st.radio(
            "Q4: In Python Object-Oriented layouts, what is the primary structural purpose of the double underscore custom method syntax (__init__)?",
            options=[None, "A) To destroy old instances via garbage collectors", "B) To act as a constructor method initializing object instance attributes", "C) To override local scoping limits inside execution blocks", "D) To bind callback variables directly into Tkinter frame maps"],
            index=0,
            key="mcq_4"
        )
        
        st.write("---")
        
        # --- SECTION B: SHORT ANSWER FILL-IN QUESTIONS ---
        st.markdown("#### ⌨️ Section B: Technical Fill-In Answers")
        
        q5_ans = st.text_input(
            "Q5: Write the exact Python keyword phrase used to instantiate a completely anonymous, single-expression function block:", 
            key="fill_1", placeholder="Type technical phrase here..."
        ).strip().lower()
        
        q6_ans = st.text_input(
            "Q6: Pathophysiology structures differentiate fever from hyperthermia. What remains unchanged or un-elevated during clinical hyperthermia conditions?", 
            key="fill_2", placeholder="Type physiological parameter here..."
        ).strip().lower()
        
        q7_ans = st.text_input(
            "Q7: When building database interfaces, which transaction design property ensures that an execution block commits entirely or rolls back completely to preserve structural stability?", 
            key="fill_3", placeholder="Type ACID property name here..."
        ).strip().lower()

        st.write("---")
        
        if st.button("📤 Finalize Assessment Script & Lock Attempt", type="primary"):
            # Scoring Calculation
            score = 0
            if q1_choice and "try...except()" in q1_choice: score += 15
            if q2_choice and "PGE2" in q2_choice: score += 15
            if q3_choice and "3NF" in q3_choice: score += 15
            if q4_choice and "constructor method" in q4_choice: score += 15
            
            if q5_ans == "lambda": score += 10
            if "hypothalamic set-point" in q6_ans or "set point" in q6_ans or "set-point" in q6_ans: score += 15
            if q7_ans == "atomicity": score += 15
            
            st.session_state.exam_running = False
            st.session_state.exam_start_time = None
            
            st.balloons()
            st.success(f"🎉 Paper Saved Successfully! Simulated Performance Score: `{score} / 100`")
            
            # Save into live leaderboard matrix if active student session profiles exist
            if st.session_state.active_student:
                st.session_state.competition_pool[st.session_state.active_student]["Score (pts)"] += score
            st.rerun()

# --- MODULE 5: COLLABORATIVE GROUP PROJECT WORKSPACE HUB ---
elif app_mode == "📋 Group Project Workspace":
    st.markdown("<h1 class='main-title'>📋 Collaborative Group Project Workspace Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Monitor milestones, core schemas, and feature deliveries for your assigned class projects.</p>", unsafe_allow_html=True)
    st.write("---")
    
    g_select = st.selectbox("🎯 Identify Project Allocation Profile:", [f"Group {i}" for i in range(1, 10)])
    g_num = int(g_select.split(" ")[1])
    
    project_manifest = {
        1: {"title": "Patient Registration GUI Interface", "spec": "Build an interface handling structural entries mapped via validation paths."},
        2: {"title": "Clinic Queue Management Simulator", "spec": "Organize patient traffic arrays through clean array queues."},
        3: {"title": "Health Record Directory Mapping Engine", "spec": "Construct relational indexing blocks linking diagnoses to specific demographic IDs."},
        4: {"title": "ICD-10 Diagnostic Parsing Standalone App", "spec": "Map alphanumeric lookup functions against underlying code tables."},
        5: {"title": "Medical Inventory Dashboard Tool", "spec": "Establish trackers plotting expiry conditions and counts over time."},
        6: {"title": "Pharmacy Drug Dispatch Portal", "spec": "Interface medication distribution workflows with tracking files."},
        7: {"title": "Patient Visit Analytics System", "spec": "Analyze patient metrics over time using pandas, showing charts for peak visit times and age distribution."},
        8: {"title": "Laboratory Result Entry System", "spec": "Input and store clinical lab tests via a Tkinter interface, utilizing SQLite database calls for patient records."},
        9: {"title": "Simple Health Information Web App", "spec": "Deploy a multi-route Flask web environment managing CRUD operations against SQLite endpoints."}
    }
    
    st.markdown(f"""
    <div class='course-card'>
        <h3 style='margin:0; color:#FF4B4B;'>{g_select}: {project_manifest[g_num]['title']}</h3>
        <p style='margin:5px 0 0 0; color:{heading_color}; font-size:14px;'><strong>Technical Framework:</strong> {project_manifest[g_num]['spec']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### ⚙️ Track Course Blueprint Milestones:")
    m0 = st.checkbox("Initialize GitHub Repo & Connect Shared Class Assets", value=st.session_state.group_tasks[g_num][0], key=f"m0_{g_num}")
    m1 = st.checkbox("Construct Relational SQLite Tables with Primary/Foreign Keys", value=st.session_state.group_tasks[g_num][1], key=f"m1_{g_num}")
    m2 = st.checkbox("Develop Tkinter Frames or Web Forms for Data Entry", value=st.session_state.group_tasks[g_num][2], key=f"m2_{g_num}")
    m3 = st.checkbox("Implement Input Validation to Catch Empty or Bad Variables", value=st.session_state.group_tasks[g_num][3], key=f"m3_{g_num}")
    m4 = st.checkbox("Embed Matplotlib/Seaborn Analytic Dashboard Windows", value=st.session_state.group_tasks[g_num][4], key=f"m4_{g_num}")
    
    if st.button("💾 Save Group Milestones Blueprint", type="secondary"):
        st.session_state.group_tasks[g_num] = [m0, m1, m2, m3, m4]
        st.success(f"Milestone blueprint successfully updated for {g_select}!")

# --- MODULE 6: PERSONAL ACADEMIC ANALYTICS TRACKER ---
elif app_mode == "📊 Personal Academic Analytics":
    st.markdown("<h1 class='main-title'>📊 Personal CGPA & Semester Goal Targeter</h1>", unsafe_allow_html=True)
    st.write("---")
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        p_cgpa = st.number_input("📈 Current Cumulative CGPA:", min_value=0.0, max_value=4.0, value=3.2, step=0.01)
    with col_in2:
        t_gpa = st.number_input("🎯 Desired Target GPA for This Semester:", min_value=0.0, max_value=4.0, value=3.3, step=0.01)
    st.info(f"Target Strategy Locked. Aim for optimal grade marks across your core Level 200 Semester 2 requirements to achieve a {t_gpa}.")

# --- MODULE 7: LEADERBOARD RANKING POOL ---
elif app_mode == "🏆 Student Leaderboard Pool":
    st.markdown("<h1 class='main-title'>🏆 Live Class Roster Competition Pool</h1>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("""
        <div class='pool-banner'>
            <h3 style='margin:0 0 5px 0; font-weight:600; color:#FFFFFF;'>📝 Profile Activation Panel</h3>
            <p style='margin:0; opacity:0.9; font-size:14px; color:#FFFFFF;'>Establish your session instance identity to upload mock test scores instantly.</p>
        </div>
    """, unsafe_allow_html=True)
    
    j_col1, j_col2 = st.columns([3, 1])
    with j_col1:
        chosen = st.text_input("👤 Enter Legal Name or Campus Alias Token:", placeholder="e.g. Mohammed Issifu")
    with j_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Establish Pool Account", use_container_width=True):
            if chosen.strip() != "":
                c_name = chosen.strip()
                st.session_state.active_student = c_name
                if c_name not in st.session_state.competition_pool:
                    st.session_state.competition_pool[c_name] = {"Score (pts)": 0, "Highest Tier": "Medium"}
                st.success(f"Profile locked to: **{c_name}**.")
                st.rerun()
                
    st.write("---")
    if len(st.session_state.competition_pool) == 0:
        st.info("📊 Standing boards are empty. Submit your first Exam script or complete Arena challenges to map metrics!")
    else:
        records = [{"Student Name": k, "Score (pts)": v["Score (pts)"], "Highest Tier": v["Highest Tier"]} for k, v in st.session_state.competition_pool.items()]
        df = pd.DataFrame(records).sort_values(by="Score (pts)", ascending=False).reset_index(drop=True)
        df.index += 1
        
        b_col, c_col = st.columns([1, 1])
        with b_col:
            st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>📊 Active Standings</h3>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
        with c_col:
            st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>📈 Visual Performance Spread</h3>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="Student Name", y="Score (pts)", color="#FF4B4B")
