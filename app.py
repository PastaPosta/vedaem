import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import os

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="AI Career Predictor", page_icon="🤖", layout="centered")

# --- СЛОВАРИ С ПРЕДМЕТАМИ ИЗ СИЛЛАБУСОВ NARXOZ ---
majors_data = {
    "Statistics and Data Science / Applied Math":[
        "Machine Learning", "Big Data Analytics", "Introduction to Deep Learning", 
        "Mathematical modeling", "Optimization methods", "Game Theory and Operations Research"
    ],
    "Cybersecurity":[
        "Information Security Fundamentals", "Introduction to Cryptography", 
        "Ethical Hacking", "Network administration", "Reverse Engineering Fundamentals", "Operating system security"
    ],
    "Digital Management and Design":[
        "UX/UI Fundamentals", "Digital Marketing", "Project Management", 
        "Front end development", "3D Modeling and Animation", "Principles of Marketing"
    ],
    "Digital Engineering":[
        "Algorithms and Data Structure", "Computer Architecture and Operating Systems", 
        "Full stack development", "iOS/Android mobile applications development", "DevOps engineering", "Software Engineering"
    ]
}

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (SESSION STATE) ---
if 'step' not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

# --- ШАГ 1: ОБЩИЕ ДАННЫЕ (Demographics & IV2) ---
if st.session_state.step == 1:
    st.title("🎓 AI Career Predictor (Research Simulation)")
    st.markdown("Welcome! This system uses advanced algorithmic logic to predict your optimal career path based on your academic profile.")
    
    st.header("Step 1: General Information")
    st.session_state.course = st.selectbox("Year of Study:", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
    
    # IV2: Practical Experience
    st.session_state.experience = st.radio(
        "Have you ever held an IT internship or relevant job? (Practical Experience)", 
        ["Yes", "No"]
    )
    
    st.button("Next ➡️", on_click=next_step)

# --- ШАГ 2: ВЫБОР НАПРАВЛЕНИЯ И ПРЕДМЕТОВ ---
elif st.session_state.step == 2:
    st.header("Step 2: Academic Profile")
    
    st.session_state.major = st.selectbox("Select your Major / Program:", list(majors_data.keys()))
    
    st.markdown("### Select your top 3 favorite subjects:")
    st.markdown("*Choose the subjects where you feel most confident or interested in.*")
    
    # Динамически подгружаем предметы на основе выбранного Major
    subjects_list = majors_data[st.session_state.major]
    
    st.session_state.selected_subjects = st.multiselect(
        "Choose exactly 3 subjects:", 
        subjects_list,
        max_selections=3
    )
    
    if len(st.session_state.selected_subjects) == 3:
        st.button("Analyze my profile 🚀", on_click=next_step)
    else:
        st.warning("Please select exactly 3 subjects to proceed.")


# --- ШАГ 3: ИМИТАЦИЯ ЗАГРУЗКИ И ВЫДАЧА РЕЗУЛЬТАТОВ (IV1 -> DV1, DV2) ---
elif st.session_state.step == 3:
    st.title("🧠 AI Analysis Results")
    
    # Эффект "работы ИИ" (покажется только один раз при загрузке шага 3)
    if 'analyzed' not in st.session_state:
        with st.spinner("Analyzing your academic inputs, matching with industry databases..."):
            time.sleep(2.5) # Искусственная задержка для реализма
        st.session_state.analyzed = True
        
    st.success("Analysis Complete! Here are your 3 tailored recommendations based on different AI logics.")
    st.markdown("Please evaluate **each** recommendation carefully.")
    
    # === ГЕНЕРАЦИЯ ЛОГИКИ В ЗАВИСИМОСТИ ОТ ВЫБОРА ===
    major = st.session_state.major
    subjects = st.session_state.selected_subjects
    
    # Дефолтные значения (Market и Skill обычно фиксированные для факультета)
    skill_rec = ""
    interest_rec = ""
    market_rec = ""
    
    if "Data" in major:
        skill_rec = "Data Analyst / Statistician"
        market_rec = "Data Engineer"
        interest_rec = "AI / Machine Learning Researcher" if "Machine Learning" in subjects else "Quantitative Analyst"
    
    elif "Cyber" in major:
        skill_rec = "Information Security Specialist"
        market_rec = "Cloud Security Architect"
        interest_rec = "Penetration Tester (Ethical Hacker)" if "Ethical Hacking" in subjects else "Cryptography Engineer"
        
    elif "Management" in major:
        skill_rec = "Digital Product Designer"
        market_rec = "IT Product / Project Manager"
        interest_rec = "UX/UI Researcher" if "UX/UI Fundamentals" in subjects else "Creative Director"
        
    else: # Digital Engineering
        skill_rec = "Backend Software Engineer"
        market_rec = "Full-Stack Web Developer"
        interest_rec = "Mobile Solutions Architect" if "iOS/Android mobile applications development" in subjects else "DevOps Engineer"

    # === ФОРМА СБОРКИ ОЦЕНОК (Likert Scales) ===
    with st.form("results_form"):
        # Model 1: Skill-Based
        st.subheader("🟢 Model 1: Technical Skill Matching Algorithm")
        st.markdown(f"**Recommendation:** **{skill_rec}**")
        st.caption("Logic: Matches your baseline academic skills with standard core technical roles.")
        acc_1 = st.slider("How accurately does this reflect your potential? (1 = Not at all, 5 = Perfectly)", 1, 5, 3, key='a1')
        int_1 = st.slider("How likely are you to pursue this career path?", 1, 5, 3, key='i1')
        st.divider()

        # Model 2: Market-Driven
        st.subheader("📈 Model 2: Market-Driven Algorithm")
        st.markdown(f"**Recommendation:** **{market_rec}**")
        st.caption("Logic: Prioritizes current industry demand, salary trends, and job availability.")
        acc_2 = st.slider("How accurately does this reflect your potential? (1 = Not at all, 5 = Perfectly)", 1, 5, 3, key='a2')
        int_2 = st.slider("How likely are you to pursue this career path?", 1, 5, 3, key='i2')
        st.divider()

        # Model 3: Interest-Based
        st.subheader("💡 Model 3: Subject Preference & Interest Algorithm")
        st.markdown(f"**Recommendation:** **{interest_rec}**")
        st.caption("Logic: Prioritizes your specific subject interests for niche/creative career satisfaction.")
        acc_3 = st.slider("How accurately does this reflect your potential? (1 = Not at all, 5 = Perfectly)", 1, 5, 3, key='a3')
        int_3 = st.slider("How likely are you to pursue this career path?", 1, 5, 3, key='i3')
        
        submitted = st.form_submit_button("Submit Evaluations")
        
        
        conn = st.connection("gsheets", type=GSheetsConnection)

        if submitted:
            # 1. Создаем DataFrame с новым ответом
            new_data = pd.DataFrame([{
                "Course": st.session_state.course,
                "Experience": st.session_state.experience,
                "Major": st.session_state.major,
                "Subjects": ", ".join(st.session_state.selected_subjects),
                "M1_Skill_Rec": skill_rec,
                "M1_Accuracy": acc_1,
                "M1_Intent": int_1,
                "M2_Market_Rec": market_rec,
                "M2_Accuracy": acc_2,
                "M2_Intent": int_2,
                "M3_Interest_Rec": interest_rec,
                "M3_Accuracy": acc_3,
                "M3_Intent": int_3
            }])

            try:
                # 2. Читаем существующие данные
                existing_data = conn.read(worksheet="Sheet1", ttl=0) # ttl=0 чтобы не кэшировало старое
                
                # 3. Добавляем новую строку
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                
                # 4. Обновляем таблицу
                conn.update(worksheet="Sheet1", data=updated_df)
                
                st.session_state.step = 4 # Переходим к финалу
                st.rerun()
            except Exception as e:
                st.error(f"Error saving to Google Sheets: {e}")

# --- ШАГ 4: ФИНАЛ ---
elif st.session_state.step == 4:
    st.balloons()
    st.title("✅ Thank you!")
    st.success("Your responses have been successfully recorded.")
    st.markdown("Your input is incredibly valuable for our research on Human-AI Interaction in career systems.")
    st.markdown("*Note: This was a simulated model for research purposes (Research Methods course).*")