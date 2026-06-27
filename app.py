import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="UCC HIM Level 200 Hub", page_icon="🎓", layout="wide")

# Persistent theme helper state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- 2. SIDEBAR HEADER ---
if os.path.exists("OIP.webp"):
    st.sidebar.image("OIP.webp", use_container_width=True)
else:
    st.sidebar.markdown("<h2 style='color:#FF4B4B; font-weight:700; margin:0;'>🏥 HIMSA UCC</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='font-size:22px; font-weight:600; margin-top:5px; color:#FF4B4B;'>UCC HIM Portal</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#64748B; font-size:14px; margin-top:-15px;'>Level 200 - Semester 2</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Replaced custom symbols with the explicit Navigation Panel label
st.sidebar.markdown("<h3 style='font-size:15px; font-weight:700; letter-spacing:0.5px; color:#FF4B4B; margin-bottom:5px;'>📋 NAVIGATION PANEL</h3>", unsafe_allow_html=True)

app_mode = st.sidebar.radio(
    "Choose a section to browse:",
    ["📚 Course Material Distribution", "📝 Adaptive Quiz Arena", "🏆 Student Leaderboard Pool"]
)

st.sidebar.markdown("---")

# --- 3. CUSTOM ELEMENT EMBEDDING STYLES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    .main-title { 
        font-size: 34px; 
        font-weight: 700; 
        color: #FF4B4B; 
        letter-spacing: -0.5px;
        margin-bottom: 5px;
    }
    .section-subtitle {
        font-size: 16px;
        color: #64748B;
        margin-bottom: 25px;
    }
    .course-card { 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #FF4B4B; 
        margin-bottom: 20px; 
        background-color: rgba(255, 75, 75, 0.05);
        border-top: 1px solid rgba(0,0,0,0.05);
        border-right: 1px solid rgba(0,0,0,0.05);
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    .pool-banner {
        background: linear-gradient(135deg, #FF4B4B 0%, #991B1B 100%);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)


# --- 4. PERSISTENT APPLICATION RUN STATS ---
if "quiz_level" not in st.session_state:
    st.session_state.quiz_level = "Medium"
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "current_course_quiz" not in st.session_state:
    st.session_state.current_course_quiz = "HIM 212: Programming II"
if "active_student" not in st.session_state:
    st.session_state.active_student = None
if "competition_pool" not in st.session_state:
    st.session_state.competition_pool = {}


# --- 5. HUB MODULE 1: COURSE MATERIAL DISTRIBUTION ---
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
    
    st.markdown(f"<div class='course-card'><h3 style='margin:0; font-weight:600;'>Current Portal: {course_selection}</h3></div>", unsafe_allow_html=True)
    
    # 1. HIM 212: PROGRAMMING II
    if "HIM 212" in course_selection:
        st.write("#### Handouts & Slide Decks")
        files = [
            "1. WEEK 1_Python Functions_May 2026.pdf",
            "WEEK4_Introduction to GUI Programs (2).pptx",
            "PROGRAMMING AND SOFTWARE DEV. II_HIM 212_OUTLINE_May_2026 (2).pdf",
            "Python GUI Programming_P2_JUNE2025 (2).pptx"
        ]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 212 Lecture Content Stub.")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f"him212_{f}")

    # 2. HIM 208: PATHOPHYSIOLOGY II
    elif "HIM 208" in course_selection:
        st.write("#### Presentation Media")
        files = [
            "CANCER.pptx",
            "diet-and-health-ppt-1114he3 (3).pptx",
            "Fever-HIM NEW (2).pptx",
            "Introduction to Pathophysiology I.ppt"
        ]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 208 Lecture Content Stub.")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f"him208_{f}")

    # 3. HIM 204: DATABASE STRUCTURES
    elif "HIM 204" in course_selection:
        st.write("#### Database Architecture Handouts")
        files = [
            "HIM 204 LECTURE 1 - INTRODUCTION TO DBMS (3).pdf",
            "HIM 204 LECTURE 2 - DBMS ARCHITECTURE (2).pdf",
            "HIM 204 LECTURE 3 - ENTITY RELATION MODEL.pdf",
            "HIM 204 LECTURE 4 - WORKING WITH ER DIAGRAMS.pdf",
            "HIM 204 LECTURE 5 - NORMALIZATION IN DBMS.pdf",
            "HIM 204 LECTURE 6 - NORMAL FORMS.pdf",
            "HIM 204 LECTURE 7 - INTRODUCTION TO DATABASE QUERIES.pdf",
            "HIM 204 LECTURE 8 - TUTORIAL SESSION.pdf"
        ]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 204 Lecture Content Stub.")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f"him204_{f}")

    # 4. HIM 210: DISEASE CLASSIFICATION AND CODING
    elif "HIM 210" in course_selection:
        st.write("#### Chapter Folders & Structural Slide Decks")
        files = [
            "Lecture_01_Introduction to Basic ICD_10_HIM210_The meaning of cl (2).pdf",
            "Lecture_02_Introduction to Basic ICD_10_HIM210_Basic principles (2).pdf",
            "Lecture_03_Introduction to Basic ICD_10_HIM210_ICD_10 convention (2).pdf",
            "Lecture_04_Introduction to Basic ICD_10_HIM210_ICD Structure of (2).pdf",
            "Lecture_05_Chapter_I__Certain_infectious_and_parasitic_diseases.pdf",
            "Lecture 06_Chapter II neoplasms (C00-D49)_HIM210.pdf",
            "Lecture_07_Chapter_XXI_Factors_influencing_health_status_and_con.pdf"
        ]
        for f in files:
            st.code(f"📁 Path: Users/ADMIN/Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 210 Disease Classification Reference.")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f"him210_{f}")
                
        st.markdown("---")
        search_query = st.text_input("🔍 ICD-10 Search Engine Tool Matrix:")
        if search_query:
            mock_hits = pd.DataFrame([
                {"Term Match": search_query.capitalize(), "ICD-10 Code block": "B15-B19", "Volume Registry": "Vol 3 Index"},
                {"Term Match": f"{search_query.capitalize()} (unspecified)", "ICD-10 Code block": "K75.9", "Volume Registry": "Vol 1 Tabular"}
            ])
            st.dataframe(mock_hits, use_container_width=True)

    # 5. PHL 205: CRITICAL THINKING AND PRACTICAL REASONING
    elif "PHL 205" in course_selection:
        st.write("#### Logical Inference Core Books")
        files = ["Critical Thinking book 3.pdf"]
        for f in files:
            st.code(f"📁 Path: Users/ADMIN/Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("PHL 205 Critical Thinking Text Book.")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f"phl205_{f}")

    # 6. HIM 206: DATA COMMUNICATION AND NETWORKS IN HEALTHCARE
    elif "HIM 206" in course_selection:
        st.write("#### Telehealth Infrastructure & Transmission Slides")
        files = [
            "Data Comm and Networks in Healthcare_OUTLINE_MAY-2026.pdf",
            "INTRO. DATA COMM AND NETWORKS IN HEALTHCARE_MAY 2026 (2).pdf",
            "2.WEEK 3_Data Transmission_May 2026 (3).pdf",
            "COMMUNICATION MEDIA_JUNE2026.pptx"
        ]
        for f in files:
            st.code(f"📁 Path: Users/ADMIN/Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write("HIM 206 Telecommunications Infrastructure Slide Asset.")
            with open(f, "rb") as b_file:
                st.download_button(label=f"📥 Download {f}", data=b_file, file_name=f, key=f"him206_{f}")

    else:
        st.write("#### Course Materials")
        st.info("🔄 Setup complete. Place additional file arrays inside the repository script path to active download nodes.")


# --- 6. HUB MODULE 2: ADAPTIVE QUIZ ARENA ---
elif app_mode == "📝 Adaptive Quiz Arena":
    st.markdown("<h1 class='main-title'>📝 Multi-Level Adaptive Revision Arena</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Answer questions correctly to step up the difficulty from Medium ➡️ Intermediate ➡️ Super Difficult.</p>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.active_student is None:
        st.warning("⚠️ Access Denied: You must register your name profile inside the 'Student Leaderboard Pool' tab first to join and compete live!")
    else:
        st.info(f"👤 Active Competitor Session: **{st.session_state.active_student}** | Tier Points Accumulated: `{st.session_state.quiz_score}`")
        
        st.session_state.current_course_quiz = st.selectbox(
            "🎯 Select Topic Base to Test",
            ["HIM 212: Programming II", "HIM 208: Pathophysiology II", "HIM 204: Database Structures", "PHL 205: Critical Thinking"]
        )
        
        levels = ["Medium", "Intermediate", "Super Difficult"]
        current_lvl = st.session_state.quiz_level
        st.progress((levels.index(current_lvl) + 1) / len(levels))
        
        st.write(f"#### Active Question Tier: **{current_lvl}**")

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
                "Medium": {"q": "Which error type describes an attack targeted straight on an opponent's character rather than structural arguments?", "o": ["Ad Hominem", "Straw Man Fallacy", "Slippery Slope"], "c": "Ad Hominem"},
                "Intermediate": {"q": "What type of reasoning draws logically certain conclusions from general premises?", "o": ["Deductive reasoning", "Inductive inference", "Abductive assumption"], "c": "Deductive reasoning"},
                "Super Difficult": {"q": "Which condition is met when a premise's truth absolute forces a true conclusion, yet its premises remain false?", "o": ["Soundness criteria met", "Valid structure only", "Cognitive structural fallacy"], "c": "Valid structure only"}
            }
        }

        q_package = quiz_matrix[st.session_state.current_course_quiz][current_lvl]
        user_choice = st.radio(f"❓ Question: {q_package['q']}", q_package['o'])
        
        if st.button("🚀 Process Choice & Update"):
            if user_choice == q_package['c']:
                st.success("🎯 Masterful! That choice is absolutely correct.")
                st.session_state.quiz_score += 50
                
                st.session_state.competition_pool[st.session_state.active_student] = {
                    "Score (pts)": st.session_state.quiz_score,
                    "Highest Tier": current_lvl
                }
                
                if current_lvl == "Medium":
                    st.session_state.quiz_level = "Intermediate"
                elif current_lvl == "Intermediate":
                    st.session_state.quiz_level = "Super Difficult"
                elif current_lvl == "Super Difficult":
                    st.balloons()
                    st.success("🏆 Incredible! You have completely conquered this course challenge tier layout!")
                st.rerun()
            else:
                st.error("❌ Incorrect choice path! Review your downloaded material cache and try again.")

        if st.button("🔄 Reset Personal Arena Run"):
            st.session_state.quiz_level = "Medium"
            st.session_state.quiz_score = 0
            if st.session_state.active_student in st.session_state.competition_pool:
                st.session_state.competition_pool[st.session_state.active_student] = {"Score (pts)": 0, "Highest Tier": "Medium"}
            st.rerun()


# --- 7. HUB MODULE 3: LEADERBOARD RANKING POOL ---
elif app_mode == "🏆 Student Leaderboard Pool":
    st.markdown("<h1 class='main-title'>🏆 Live Roster Competition Pool</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Real-time ranking of real students who log onto the hub and decide to participate.</p>", unsafe_allow_html=True)
    st.write("---")
    
    # PROFILE ENTRY PANEL
    st.markdown("""
        <div class='pool-banner'>
            <h3 style='margin:0 0 5px 0; font-weight:600; color:#FFFFFF;'>📝 Active Profile Entrance</h3>
            <p style='margin:0; opacity:0.9; font-size:14px; color:#FFFFFF;'>Enter your real name or unique campus alias to open an active tracking scorecard stream!</p>
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
                st.success(f"🎉 Active session profile locked to: **{clean_name}**. Navigate to the Quiz tab to compete!")
                st.rerun()
            else:
                st.error("❌ Identification error: Input field blank!")
                
    st.write("---")
    
    # DYNAMIC CHART AND LEADERBOARD GENERATION POOL
    if len(st.session_state.competition_pool) == 0:
        st.info("📊 The competition pool is currently empty. Be the first to type in your name above, hop into the Quiz Arena, and log points!")
    else:
        pool_records = []
        for name, data in st.session_state.competition_pool.items():
            pool_records.append({
                "Student Name": name,
                "Score (pts)": data["Score (pts)"],
                "Highest Tier": data["Highest Tier"]
            })
            
        df_pool = pd.DataFrame(pool_records)
        df_pool = df_pool.sort_values(by="Score (pts)", ascending=False).reset_index(drop=True)
        df_pool.index += 1  
        
        col_board, col_chart = st.columns([1, 1])
        
        with col_board:
            st.write("### 📊 Active Standing Board")
            st.dataframe(df_pool, use_container_width=True)
            
        with col_chart:
            st.write("### 📈 Class Ranking Visual Spread")
            st.bar_chart(data=df_pool, x="Student Name", y="Score (pts)", color="#FF4B4B")
            
        st.sidebar.info(f"🔥 Active Competitors in Pool: {len(pool_records)}")
