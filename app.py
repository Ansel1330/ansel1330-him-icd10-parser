import streamlit as st
import pandas as pd
import numpy as np
import os
import anthropic
import json
import re

# --- 1. PAGE SETUP & CONFIGURATION ---
st.set_page_config(page_title="UCC HIM Level 200 Hub", page_icon="🎓", layout="wide")

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

st.sidebar.markdown("<h3 style='font-size:16px; font-weight:700; color:#FF4B4B; margin-bottom:5px;'>📋 NAVIGATION PANEL</h3>", unsafe_allow_html=True)

app_mode = st.sidebar.radio(
    "Choose a session to navigate:",
    ["📚 Course Material Distribution", "📝 Adaptive Quiz Arena", "🏆 Student Leaderboard Pool", "📊 Academic Targeter"]
)

st.sidebar.markdown("---")
st.session_state.dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode Layout")

# --- 3. DYNAMIC THEMING ENGINE ---
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
    .pool-banner {{
        background: linear-gradient(135deg, #FF4B4B 0%, #991B1B 100%);
        padding: 25px; border-radius: 16px; margin-bottom: 25px;
    }}
    .ai-badge {{
        background: linear-gradient(135deg, #7C3AED, #4F46E5);
        color: white; padding: 4px 10px; border-radius: 20px;
        font-size: 12px; font-weight: 600; display: inline-block; margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)


# --- 4. PERSISTENT MEMORY ---
if "active_student" not in st.session_state: st.session_state.active_student = None
if "competition_pool" not in st.session_state: st.session_state.competition_pool = {}
if "quiz_index" not in st.session_state: st.session_state.quiz_index = 0
if "score" not in st.session_state: st.session_state.score = 0
if "prev_cgpa" not in st.session_state: st.session_state.prev_cgpa = 3.2
if "target_gpa" not in st.session_state: st.session_state.target_gpa = 3.3
if "ai_questions" not in st.session_state: st.session_state.ai_questions = []
if "current_topic" not in st.session_state: st.session_state.current_topic = None
if "answered" not in st.session_state: st.session_state.answered = False
if "last_correct" not in st.session_state: st.session_state.last_correct = None
if "explanation" not in st.session_state: st.session_state.explanation = ""

# --- 5. AI QUESTION GENERATOR ---
COURSE_CONTEXTS = {
    "HIM 212: Programming II": """
        You are a university lecturer generating exam questions for HIM 212: Programming and Software Development II 
        at the University of Cape Coast, Ghana. Topics include: Python functions and scope, GUI development with Tkinter, 
        object-oriented programming, file handling, error handling, modules, and building clinical health information system applications.
        Students are Level 200 Health Information Management undergraduates.
    """,
    "HIM 208: Pathophysiology II": """
        You are a university lecturer generating exam questions for HIM 208: Pathophysiology II 
        at the University of Cape Coast, Ghana. Topics include: fever mechanisms and pyrogens, 
        inflammatory responses, cancer pathophysiology, cardiovascular diseases, respiratory disorders, 
        endocrine disruptions, and immune system pathology. Students are Level 200 Health Information Management undergraduates.
    """,
    "HIM 204: Database Structures": """
        You are a university lecturer generating exam questions for HIM 204: Database Structures 
        at the University of Cape Coast, Ghana. Topics include: DBMS concepts and architecture, 
        Entity-Relationship (ER) modeling, relational database design, normalization (1NF, 2NF, 3NF, BCNF), 
        SQL queries, indexing, and health data management systems. Students are Level 200 Health Information Management undergraduates.
    """,
    "PHL 205: Critical Thinking": """
        You are a university lecturer generating exam questions for PHL 205: Critical Thinking 
        at the University of Cape Coast, Ghana. Topics include: logical fallacies (straw man, ad hominem, false dichotomy, etc.), 
        argument structure and evaluation, deductive vs inductive reasoning, cognitive biases, 
        and application of logic in healthcare decision-making. Students are Level 200 Health Information Management undergraduates.
    """
}

def generate_ai_questions(topic: str, num_questions: int = 10) -> list:
    """Generate real exam questions using Claude AI."""
    client = anthropic.Anthropic()
    context = COURSE_CONTEXTS.get(topic, "")
    
    prompt = f"""
{context}

Generate exactly {num_questions} multiple-choice questions for a semester exam. 
Each question must be academically rigorous, clinically relevant where applicable, and test real understanding.

Return ONLY a valid JSON array. No explanation, no markdown, no code blocks. Just the raw JSON.

Format:
[
  {{
    "q": "Full question text here?",
    "o": ["Option A", "Option B", "Option C", "Option D"],
    "c": "Option A",
    "explanation": "Brief explanation of why this answer is correct."
  }}
]

Rules:
- All 4 options must be plausible (no obviously wrong distractors)
- The correct answer ("c") must exactly match one of the options in "o"
- Questions must vary in difficulty (mix of recall, application, and analysis)
- Make questions specific, not vague or generic
- Avoid repeating the same concept
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    
    questions = json.loads(raw.strip())
    return questions


# --- 6. HUB MODULE 1: COURSE MATERIAL DISTRIBUTION ---
if app_mode == "📚 Course Material Distribution":
    st.markdown("<h1 class='main-title'>📚 Courseware Repository</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Access reference sheets, lecture files, and interactive clinical domain maps.</p>", unsafe_allow_html=True)
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
    
    st.markdown(f"<div class='course-card'><h3 style='margin:0; font-weight:600; color:{heading_color};'>Current Portal: {course_selection}</h3></div>", unsafe_allow_html=True)
    
    if "HIM 212" in course_selection:
        st.markdown("<div class='case-box'><strong>📖 Clinical Case Study:</strong> UCC Hospital needs a rapid UI form to register incoming clinical outpatients. If the programmer accidentally binds multiple text entry blocks to the same variable stream, old patient records get overwritten automatically. Functional local scopes prevent this error.</div>", unsafe_allow_html=True)
        st.info("💡 **Why this matters:** Think of a Python function like a private room in a library. Whatever variables you use inside that room stay private, preventing them from mixing up with other information outside.")
        
        files = ["1. WEEK 1_Python Functions_May 2026.pdf", "WEEK4_Introduction to GUI Programs (2).pptx", "PROGRAMMING AND SOFTWARE DEV. II_HIM 212_OUTLINE_May_2026 (2).pdf"]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write(f"Stub file for {f}")
            with open(f, "rb") as bf: st.download_button(label=f"📥 Download {f}", data=bf, file_name=f)

    elif "HIM 208" in course_selection:
        st.markdown("<div class='case-box'><strong>📖 Clinical Case Study:</strong> A 24-year-old student presenting at UCC clinic shows a temperature of 39°C. Lab tests reveal circulating lipopolysaccharides from Gram-negative bacteria acting as exogenous pyrogens, signaling the hypothalamus to spike body heat.</div>", unsafe_allow_html=True)
        st.info("💡 **Why this matters:** Fever isn't a broken system; it's a deliberate setting change! Think of your hypothalamus like a home thermostat. Pyrogens don't break the heater — they turn the dial up to fight infections.")
        
        files = ["CANCER.pptx", "diet-and-health-ppt-1114he3 (3).pptx", "Fever-HIM NEW (2).pptx"]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write(f"Stub file for {f}")
            with open(f, "rb") as bf: st.download_button(label=f"📥 Download {f}", data=bf, file_name=f)

    elif "HIM 204" in course_selection:
        st.markdown("<div class='case-box'><strong>📖 Clinical Case Study:</strong> A clinical database lists patient records alongside their doctors' home addresses in the same file. If a doctor resigns, deleting them accidentally deletes the patient's history. Relational normalization isolates these facts into separate linked tables.</div>", unsafe_allow_html=True)
        st.info("💡 **Why this matters:** Normalization is like packing a smart travel bag. Instead of throwing clothes, food, and electronics into one giant pile, you separate them into custom compartments so nothing gets damaged or lost.")
        
        files = ["HIM 204 LECTURE 1 - INTRODUCTION TO DBMS (3).pdf", "HIM 204 LECTURE 2 - DBMS ARCHITECTURE (2).pdf", "HIM 204 LECTURE 5 - NORMALIZATION IN DBMS.pdf"]
        for f in files:
            st.code(f"📁 Path: Downloads/.../{f}")
            if not os.path.exists(f): 
                with open(f, "w") as stub: stub.write(f"Stub file for {f}")
            with open(f, "rb") as bf: st.download_button(label=f"📥 Download {f}", data=bf, file_name=f)

    elif "HIM 210" in course_selection:
        st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>⚡ Integrated Functional Asset</h3>", unsafe_allow_html=True)
        st.info("💡 Below is your active ICD-10 Diagnostic Parser Engine embedded within its exact course module mapping!")
        st.markdown("---")
        
        search_query = st.text_input("🔍 ICD-10 Alpha-Index & Tabular Match Engine (Type Search Term):")
        if search_query:
            st.success(f"Parsing extracted hits for: '{search_query}' across Volume 1 and Volume 3 maps...")
            mock_hits = pd.DataFrame([
                {"Term Match": search_query.capitalize(), "ICD-10 Code block": "B15-B19", "Volume Registry": "Vol 3 Index (Page 328)"},
                {"Term Match": f"{search_query.capitalize()} (unspecified)", "ICD-10 Code block": "K75.9", "Volume Registry": "Vol 1 Tabular"}
            ])
            st.dataframe(mock_hits, use_container_width=True)


# --- 7. HUB MODULE 2: AI-POWERED ADAPTIVE QUIZ ARENA ---
elif app_mode == "📝 Adaptive Quiz Arena":
    st.markdown("<h1 class='main-title'>📝 AI-Powered Quiz Arena</h1>", unsafe_allow_html=True)
    st.markdown("<div class='ai-badge'>✨ Powered by Claude AI — Real Exam Questions Generated Live</div>", unsafe_allow_html=True)
    st.write("---")

    if st.session_state.active_student is None:
        st.warning("⚠️ Access Denied: You must register your name profile inside the 'Student Leaderboard Pool' tab first to participate!")
    else:
        st.info(f"👤 Competitor: **{st.session_state.active_student}** | Score: `{st.session_state.score} pts`")

        topic = st.selectbox("🎯 Select Subject Field:", list(COURSE_CONTEXTS.keys()))

        # If topic changed or no questions loaded yet, reset
        if topic != st.session_state.current_topic:
            st.session_state.ai_questions = []
            st.session_state.quiz_index = 0
            st.session_state.current_topic = topic
            st.session_state.answered = False
            st.session_state.last_correct = None
            st.session_state.explanation = ""

        num_q = st.slider("Number of questions to generate:", min_value=5, max_value=20, value=10, step=5)

        # Load / Regenerate button
        col_gen1, col_gen2 = st.columns([2, 3])
        with col_gen1:
            gen_label = "🤖 Generate New AI Questions" if st.session_state.ai_questions else "🤖 Generate AI Questions"
            if st.button(gen_label, use_container_width=True):
                with st.spinner("🧠 Claude AI is writing your exam questions... Please wait."):
                    try:
                        st.session_state.ai_questions = generate_ai_questions(topic, num_q)
                        st.session_state.quiz_index = 0
                        st.session_state.answered = False
                        st.session_state.last_correct = None
                        st.session_state.explanation = ""
                        st.success(f"✅ {len(st.session_state.ai_questions)} real questions generated for **{topic}**!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to generate questions: {e}")

        st.write("---")

        if not st.session_state.ai_questions:
            st.markdown("""
                <div style='text-align:center; padding:40px; opacity:0.6;'>
                    <h3>🤖 No questions loaded yet</h3>
                    <p>Click "Generate AI Questions" above to create a fresh set of real exam questions for your selected course.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            questions = st.session_state.ai_questions
            total_q = len(questions)
            idx = st.session_state.quiz_index

            if idx >= total_q:
                st.success(f"🏆 You've completed all {total_q} questions! Final score: **{st.session_state.score} pts**")
                st.balloons()
                if st.button("🔄 Generate a Fresh Set of Questions"):
                    st.session_state.ai_questions = []
                    st.session_state.quiz_index = 0
                    st.session_state.answered = False
                    st.session_state.last_correct = None
                    st.session_state.explanation = ""
                    st.rerun()
            else:
                q_data = questions[idx]

                # Progress
                st.markdown(f"### Question {idx + 1} of {total_q}")
                st.progress((idx + 1) / total_q)

                # Question card
                st.markdown(f"""
                    <div class='course-card'>
                        <p style='font-size:17px; font-weight:500; color:{heading_color}; margin:0;'>{q_data['q']}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Answer options
                if not st.session_state.answered:
                    u_choice = st.radio("Select your answer:", q_data['o'], label_visibility="collapsed")

                    if st.button("🚀 Submit Answer", use_container_width=False):
                        correct = u_choice == q_data['c']
                        st.session_state.last_correct = correct
                        st.session_state.explanation = q_data.get("explanation", "")
                        if correct:
                            st.session_state.score += 10
                            st.session_state.competition_pool[st.session_state.active_student]["Score (pts)"] = st.session_state.score
                        st.session_state.answered = True
                        st.rerun()
                else:
                    # Show result + explanation before moving on
                    if st.session_state.last_correct:
                        st.success("🎯 Correct! Well done.")
                    else:
                        st.error(f"❌ Incorrect. The correct answer was: **{q_data['c']}**")

                    if st.session_state.explanation:
                        st.markdown(f"""
                            <div style='background:#1E3A5F; padding:14px; border-radius:8px; border-left:4px solid #3B82F6; margin-top:10px;'>
                                <strong style='color:#93C5FD;'>📖 Explanation:</strong>
                                <p style='color:#E2E8F0; margin:6px 0 0 0;'>{st.session_state.explanation}</p>
                            </div>
                        """, unsafe_allow_html=True)

                    if st.button("➡️ Next Question", use_container_width=False):
                        st.session_state.quiz_index += 1
                        st.session_state.answered = False
                        st.session_state.last_correct = None
                        st.session_state.explanation = ""
                        st.rerun()


# --- 8. HUB MODULE 3: LEADERBOARD RANKING POOL ---
elif app_mode == "🏆 Student Leaderboard Pool":
    st.markdown("<h1 class='main-title'>🏆 Live Roster Competition Pool</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Real-time ranking of students participating in the hub challenges.</p>", unsafe_allow_html=True)
    st.write("---")
    
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
                    st.session_state.competition_pool[clean_name] = {"Score (pts)": st.session_state.score}
                st.success(f"🎉 Active session profile locked to: **{clean_name}**.")
                st.rerun()
                
    st.write("---")
    
    if len(st.session_state.competition_pool) == 0:
        st.info("📊 The competition pool is currently empty. Be the first to log points above!")
    else:
        pool_records = [{"Student Name": k, "Score (pts)": v["Score (pts)"]} for k, v in st.session_state.competition_pool.items()]
        df_pool = pd.DataFrame(pool_records).sort_values(by="Score (pts)", ascending=False).reset_index(drop=True)
        df_pool.index += 1  
        
        col_board, col_chart = st.columns([1, 1])
        with col_board:
            st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>📊 Active Standing Board</h3>", unsafe_allow_html=True)
            st.dataframe(df_pool, use_container_width=True)
        with col_chart:
            st.markdown(f"<h3 style='color:{heading_color}; font-weight:600;'>📈 Class Ranking Visual Spread</h3>", unsafe_allow_html=True)
            st.bar_chart(data=df_pool, x="Student Name", y="Score (pts)", color="#FF4B4B")


# --- 9. HUB MODULE 4: ACADEMIC TARGETER ---
elif app_mode == "📊 Academic Targeter":
    st.markdown("<h1 class='main-title'>📊 Personal CGPA & Semester Goal Targeter</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.session_state.prev_cgpa = st.number_input("Enter your previous cumulative CGPA:", value=st.session_state.prev_cgpa, step=0.1)
    with col_t2:
        st.session_state.target_gpa = st.number_input("Enter your target GPA for this Semester 2:", value=st.session_state.target_gpa, step=0.1)
        
    if st.button("📈 Calculate Target Benchmarks"):
        st.balloons()
        st.success(f"To raise your academic trajectory from a {st.session_state.prev_cgpa} up to a {st.session_state.target_gpa}, aim for a minimum grade score distribution profile of B+ or higher across your 7 fundamental Level 200 health information system modules!")
