import streamlit as st
import pandas as pd
from PIL import Image
import os

# --- PAGE CONFIG & CUSTOM STYLES ---
st.set_page_config(page_title="HIM Study Hub & Parser", page_icon="🏥", layout="wide")

# Theme / Mode Switching Logic using Streamlit Session State
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("OIP.webp", use_container_width=True)
st.sidebar.title("HIM Navigation Portal")

# Theme Selector Widget
theme_choice = st.sidebar.selectbox("🌓 Choose Display Theme Mode", ["Dark Mode", "Light Mode"])
st.sidebar.markdown("---")

# Main Navigation Menu
menu_choice = st.sidebar.radio(
    "📂 Select Feature Section",
    [
        "🔍 ICD-10 Code Parser",
        "📝 Adaptive Revision Quiz",
        "📊 Medical Reference Tables",
        "📄 Course Materials & Downloads"
    ]
)

# Information Footer
st.sidebar.info("Designed for Health Information Management Students. Empowering academic excellence.")

# --- SECTION 1: ICD-10 PARSER ---
if menu_choice == "🔍 ICD-10 Code Parser":
    st.title("🏥 Health Information Management")
    st.subheader("ICD-10 Diagnostic Lead/Subterm Parser")
    st.write("---")
    
    search_query = st.text_input("🔍 Enter Diagnostic Lead Term or Subterm (e.g., Hepatitis, Diabetes):")
    
    if search_query:
        st.success(f"Results for search: '{search_query}'")
        # Placeholder for your existing PDF extraction logic
        st.info("Your underlying PDF matching logic executes here seamlessly.")

# --- SECTION 2: ADAPTIVE QUIZ SECTION ---
elif menu_choice == "📝 Adaptive Revision Quiz":
    st.title("📝 Adaptive Level-Advancing Revision Quiz")
    st.write("Test your knowledge! Answering correctly unlocks more difficult levels.")
    st.write("---")

    # Quiz Database Dictionary
    quiz_data = {
        "Medium": {
            "question": "Which of the following is characteristic of a Gram-positive bacterial cell wall?",
            "options": ["A thin peptidoglycan layer with outer membrane", "A thick peptidoglycan layer retaining crystal violet", "An outer lipopolysaccharide membrane layer"],
            "correct": "A thick peptidoglycan layer retaining crystal violet"
        },
        "Intermediate": {
            "question": "Which mechanism of horizontal gene transfer involves a bacteriophage virus injecting DNA into a bacterium?",
            "options": ["Conjugation via sex pilus", "Transformation of naked environmental DNA", "Transduction mediated by a viral vector"],
            "correct": "Transduction mediated by a viral vector"
        },
        "Advanced": {
            "question": "During a fever response, which endogenous pyrogen acts directly on the preoptic area of the hypothalamus to raise the thermal set-point?",
            "options": ["Interleukin-1 (IL-1)", "Prostaglandin E2 (PGE2)", "Tumor Necrosis Factor-alpha (TNF-α)"],
            "correct": "Prostaglandin E2 (PGE2)"
        }
    }

    # Initialize session state tracking variables
    if "quiz_level" not in st.session_state:
        st.session_state.quiz_level = "Medium"
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    current_level = st.session_state.quiz_level
    
    # Display Level Progress Bars
    level_order = ["Medium", "Intermediate", "Advanced"]
    progress_val = (level_order.index(current_level) + 1) / len(level_order)
    st.progress(progress_val)
    st.subheader(f"Current Difficulty Level: :orange[{current_level}]")

    # Render Current Question
    q_data = quiz_data[current_level]
    user_ans = st.radio(q_data["question"], q_data["options"])

    if st.button("Submit Answer"):
        if user_ans == q_data["correct"]:
            st.success("🎉 Correct Answer!")
            st.session_state.quiz_score += 10
            
            # Advancing Logic
            if current_level == "Medium":
                st.session_state.quiz_level = "Intermediate"
                st.rerun()
            elif current_level == "Intermediate":
                st.session_state.quiz_level = "Advanced"
                st.rerun()
            elif current_level == "Advanced":
                st.balloons()
                st.success(f"🏆 Genius Status Reached! Total Score: {st.session_state.quiz_score} pts!")
        else:
            st.error("❌ Incorrect answer. Review your notes and try again!")

    if st.button("🔄 Reset Quiz Tracker"):
        st.session_state.quiz_level = "Medium"
        st.session_state.quiz_score = 0
        st.rerun()

# --- SECTION 3: MEDICAL REFERENCE TABLES ---
elif menu_choice == "📊 Medical Reference Tables":
    st.title("📊 Essential Medical Reference Guides")
    st.write("Quick reference metrics for clinical classification and terminology verification.")
    st.write("---")

    tab1, tab2 = st.tabs(["Common Medical Prefixes", "Vital Signs Standards"])
    
    with tab1:
        prefix_data = {
            "Prefix / Suffix": ["Cardio-", "Hepa- / Hepato-", "Neuro-", "-itis", "-emia"],
            "Anatomical Meaning": ["Relating to the Heart", "Relating to the Liver", "Relating to the Nervous System", "Inflammation or Infection", "Presence in the Blood"]
        }
        st.table(pd.DataFrame(prefix_data))
        
    with tab2:
        vitals_data = {
            "Assessment Parameter": ["Adult Heart Rate", "Blood Pressure (Normal)", "Oral Core Temperature"],
            "Standard Reference Range": ["60 – 100 beats per minute", "120/80 mmHg or lower", "36.5°C – 37.5°C"]
        }
        st.table(pd.DataFrame(vitals_data))

# --- SECTION 4: COURSE MATERIALS & DOWNLOADS ---
elif menu_choice == "📄 Course Materials & Downloads":
    st.title("📄 Course Material Distribution Center")
    st.write("Download lecture notes and study guidelines directly onto your device.")
    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        st.info("### 📘 Medical Microbiology Reference Guide")
        st.write("Covers bacterial structural morphotyping, gram reaction classifications, and pathways.")
        # Create a blank test file if your actual file isn't uploaded yet
        if not os.path.exists("Microbiology_Study_Notes.pdf"):
            with open("Microbiology_Study_Notes.pdf", "w") as f: f.write("Microbiology Study Materials Placeholder Content.")
            
        with open("Microbiology_Study_Notes.pdf", "rb") as file:
            st.download_button(
                label="📥 Download Microbiology Notes (PDF)",
                data=file,
                file_name="Microbiology_Study_Notes.pdf",
                mime="application/pdf"
            )

    with col2:
        st.info("### 📙 Pathophysiology Lecture Summary")
        st.write("In-depth focus on homeostatic cell alterations, inflammation pathways, and pyrogen chains.")
        if not os.path.exists("Pathophysiology_Lecture_Summary.pdf"):
            with open("Pathophysiology_Lecture_Summary.pdf", "w") as f: f.write("Pathophysiology Summary Placeholder Content.")
            
        with open("Pathophysiology_Lecture_Summary.pdf", "rb") as file:
            st.download_button(
                label="📥 Download Pathophysiology Summary (PDF)",
                data=file,
                file_name="Pathophysiology_Lecture_Summary.pdf",
                mime="application/pdf"
            )
