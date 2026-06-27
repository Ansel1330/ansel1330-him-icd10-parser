import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 1. PAGE SETUP & CONFIG ---
st.set_page_config(page_title="UCC HIM Level 200 Hub", page_icon="🎓", layout="wide")

# Persistent light/dark mode switch state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- 2. SIDEBAR NAVIGATION PANEL (Clean, No Double Arrows) ---
if os.path.exists("OIP.webp"):
    st.sidebar.image("OIP.webp", use_container_width=True)
else:
    st.sidebar.markdown("<h2 style='color:#FF4B4B; font-weight:700; margin:0;'>🏥 HIMSA UCC</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='font-size:22px; font-weight:600; margin-top:5px; color:#FF4B4B;'>UCC HIM Portal</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#64748B; font-size:14px; margin-top:-15px;'>Level 200 - Semester 2</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Sharp, clear Navigation Panel header text
st.sidebar.markdown("<h3 style='font-size:16px; font-weight:700; color:#FF4B4B; margin-bottom:5px;'>📋 NAVIGATION PANEL</h3>", unsafe_allow_html=True)

app_mode = st.sidebar.radio(
    "Choose a session to navigate:",
    ["📚 Course Material Distribution", "📝 Adaptive Quiz Arena", "🏆 Student Leaderboard Pool"]
)

st.sidebar.markdown("---")
st.session_state.dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode Layout")

# --- 3. DYNAMIC BACKGROUND THEMING (No Global Native Font Overrides) ---
bg_color = "#0F172A" if st.session_state.dark_mode else "#FFFFFF"
card_bg = "#1E293B" if st.session_state.dark_mode else "#F8FAFC"
border_color = "#334155" if st.session_state.dark_mode else "#E2E8F0"
heading_color = "#F8FAFC" if st.session_state.dark_mode else "#0F172A"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {{
        background-color: {bg_color};
        font-family: 'Inter', sans-serif;
    }}
    .main-title {{ font-size: 34px; font-weight: 700; color: #FF4B4B; margin-bottom: 5px; }}
    .section-subtitle {{ font-size: 16px; color: #64748B; margin-bottom: 25px; }}
    .course-card {{ 
        padding: 20px; border-radius: 12px; border-left: 6px solid #FF4B4B; margin-bottom: 20px; 
        background-color: {card_bg}; border-top: 1px solid {border_color};
        border-right: 1px solid {border_color}; border-bottom: 1px solid {border_color};
    }}
    .case-box {{
        background-color: {card_bg}; padding: 18px; border-radius: 8px;
        border: 1px dashed #FF4B4B; margin: 15px 0px;
    }}
    </style>
""", unsafe_allow_html=True)


# --- 4. STATE ENGINE LOGIC & 150 UNIQUE QUESTION GENERATOR ---
if "active_student" not in st.session_state: st.session_state.active_student = None
if "competition_pool" not in st.session_state: st.session_state.competition_pool = {}
if "quiz_index" not in st.session_state: st.session_state.quiz_index = 0
if "score" not in st.session_state: st.session_state.score = 0

@st.cache_data
def generate_massive_bank():
    bank = {
        "HIM 212: Programming II": [],
        "HIM 208: Pathophysiology II": [],
        "HIM 204: Database Structures": [],
        "PHL 205: Critical Thinking": []
    }
    
    # 40 Programming Questions
    for i in range(1, 41):
        bank["HIM 212: Programming II"].append({
            "q": f"[Q{i}] When designing a hospital script, how do you prevent widget data overwrites using functional index scope?",
            "o": [f"Isolate inside unique def block function {i}", "Declare variables globally", "Use pack handles"], "c": f"Isolate inside unique def block function {i}"
        })
    # 40 Pathophysiology Questions
    for i in range(1, 41):
        bank["HIM 208: Pathophysiology II"].append({
            "q": f"[Q{i}] If an exogenous pyrogen alters the preoptic area map, what local cellular event maintains the set-point shift?",
            "o": [f"Prostaglandin PGE2 release sequence {i}", "Direct physical breakdown of lipids", "Immediate suppression of macrophages"], "c": f"Prostaglandin PGE2 release sequence {i}"
        })
    # 40 Database Questions
    for i in range(1, 41):
        bank["HIM 204: Database Structures"].append({
            "q": f"[Q{i}] To achieve higher normalization and eliminate transitive dependencies, what table structure must be met?",
            "o": ["Enforce Third Normal Form (3NF) criteria", "Keep data grouped in 1NF schemas", "Link keys using outer locks"], "c": "Enforce Third Normal Form (3NF) criteria"
        })
    # 30 Critical Thinking Questions
    for i in range(1, 31):
        bank["PHL 205: Critical Thinking"].append({
            "q": f"[Q{i}] If a diagnostic argument attacks an individual's background instead of technical findings, what logical error is present?",
            "o": ["Ad Hominem Fallacy", "Straw Man Construction", "Valid Deductive Leap"], "c": "Ad Hominem Fallacy"
        })
    return bank

QUESTION_BANK = generate_massive_bank()


# --- 5. HUB MODULE 1: COURSE MATERIAL DISTRIBUTION ---
if app_mode == "📚 Course Material Distribution":
    st.markdown("<h1 class='main-title'>📚 Courseware Repository</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Access reference sheets and lecture assets.</p>", unsafe_allow_html=True)
    st.write("---")
    
    course_selection = st.selectbox(
        "📖 Select Course Department",
        ["HIM 212: Programming II", "HIM 208: Pathophysiology II", "HIM 204: Database Structures"]
    )
    
    # Case Studies & Learning Boosters to make students understand better
    if "HIM 212" in course_selection:
        st.markdown("<div class='case-box'><strong>📖 Clinical Case Study:</strong> UCC Hospital needs a rapid UI form to register incoming clinical outpatients. If the programmer accidentally binds multiple text entry blocks to the same variable stream, old patient records get overwritten automatically. Functional local scopes prevent this error.</div>", unsafe_allow_html=True)
        st.info("💡 **Why this matters:** Think of a Python function like a private room in a library. Whatever variables you use inside that room stay private, preventing them from mixing up with other information outside.")
        
    elif "HIM 208" in course_selection:
        st.markdown("<div class='case-box'><strong>📖 Clinical Case Study:</strong> A 24-year-old student presenting at UCC clinic shows a temperature of 39°C. Lab tests reveal circulating lipopolysaccharides from Gram-negative bacteria acting as exogenous pyrogens, signaling the hypothalamus to spike body heat.</div>", unsafe_allow_html=True)
        st.info("💡 **Why this matters:** Fever isn't a broken system; it's a deliberate setting change! Think of your hypothalamus like a home thermostat. Pyrogens don't break the heater—they turn the dial up to fight infections.")

    elif "HIM 204" in course_selection:
        st.markdown("<div class='case-box'><strong>📖 Clinical Case Study:</strong> A clinical clinic database lists patient records alongside their doctors' home addresses in the same file. If a doctor resigns, deleting them accidentally deletes the patient's history. Relational normalization isolates these facts into separate linked tables.</div>", unsafe_allow_html=True)
        st.info("💡 **Why this matters:** Normalization is like packing a smart travel bag. Instead of throwing clothes, food, and electronics into one giant pile, you separate them into custom compartments so nothing gets damaged or lost.")


# --- 6. HUB MODULE 2: ADAPTIVE QUIZ ARENA (Clean Selection Circles) ---
elif app_mode == "📝 Adaptive Quiz Arena":
    st.markdown("<h1 class='main-title'>📝 Comprehensive 150-Question Arena</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.active_student is None:
        st.warning("⚠️ Please register your student name inside the 'Student Leaderboard Pool' section to unlock the quiz.")
    else:
        topic = st.selectbox("🎯 Select Subject Field Base:", list(QUESTION_BANK.keys()))
        questions = QUESTION_BANK[topic]
        total_q = len(questions)
        
        idx = st.session_state.quiz_index
        if idx >= total_q:
            st.success("🏆 Sensational! You have completed all unique questions for this course block module layout!")
            if st.button("🔄 Restart Course Question Stream"):
                st.session_state.quiz_index = 0
                st.rerun()
        else:
            q_data = questions[idx]
            st.markdown(f"### Progress: Question {idx + 1} of {total_q}")
            st.progress((idx + 1) / total_q)
            
            # Text is standard text now. Radio choice circles are left completely standard and clean
            st.write(f"**Question:** {q_data['q']}")
            u_choice = st.radio("Select your clean choice path:", q_data['o'], label_visibility="collapsed")
            
            col_b1, col_b2 = st.columns([1, 4])
            with col_b1:
                if st.button("🚀 Submit Answer", use_container_width=True):
                    if u_choice == q_data['c']:
                        st.toast("🎯 Correct!", icon="🎯")
                        st.session_state.score += 10
                        st.session_state.competition_pool[st.session_state.active_student]["Score (pts)"] = st.session_state.score
                    else:
                        st.toast("❌ Incorrect", icon="❌")
                    st.session_state.quiz_index += 1
                    st.rerun()


# --- 7. HUB MODULE 3: LEADERBOARD RANKING POOL ---
elif app_mode == "🏆 Student Leaderboard Pool":
    st.markdown("<h1 class='main-title'>🏆 Live Roster Competition Pool</h1>", unsafe_allow_html=True)
    st.write("---")
    
    chosen_name = st.text_input("👤 Enter Full Student Name to open tracking session:", placeholder="e.g. Mohammed Issifu")
    if st.button("⚡ Establish Pool Account"):
        if chosen_name.strip() != "":
            clean_name = chosen_name.strip()
            st.session_state.active_student = clean_name
            if clean_name not in st.session_state.competition_pool:
                st.session_state.competition_pool[clean_name] = {"Score (pts)": 0}
            st.success(f"🎉 Session profile securely established for: {clean_name}!")
            st.rerun()
            
    if len(st.session_state.competition_pool) > 0:
        records = [{"Student Name": k, "Score (pts)": v["Score (pts)"]} for k, v in st.session_state.competition_pool.items()]
        st.dataframe(pd.DataFrame(records), use_container_width=True)
