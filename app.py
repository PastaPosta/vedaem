import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="AI Career Predictor", layout="centered")

# --- СЛОВАРИ ДАННЫХ ---
majors_data = {
    "Statistics & Data Science / Статистика и Data Science / Статистика және Деректер ғылымы":[
        "Machine Learning", "Big Data Analytics", "Introduction to Deep Learning", 
        "Mathematical modeling", "Optimization methods", "Game Theory and Operations Research"
    ],
    "Cybersecurity / Кибербезопасность / Киберқауіпсіздік":[
        "Information Security Fundamentals", "Introduction to Cryptography", 
        "Ethical Hacking", "Network administration", "Reverse Engineering Fundamentals", "Operating system security"
    ],
    "Digital Management & Design / Цифровой Менеджмент и Дизайн / Цифрлық Менеджмент және Дизайн":[
        "UX/UI Fundamentals", "Digital Marketing", "Project Management", 
        "Front end development", "3D Modeling and Animation", "Principles of Marketing"
    ],
    "Digital Engineering / Цифровая Инженерия / Цифрлық Инженерия":[
        "Algorithms and Data Structure", "Computer Architecture and Operating Systems", 
        "Full stack development", "iOS/Android mobile applications development", "DevOps engineering", "Software Engineering"
    ]
}

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ ---
if 'step' not in st.session_state:
    st.session_state.step = 0 

def next_step():
    st.session_state.step += 1

# --- ШАГ 0: ЭТИКА (CONSENT, ANONYMITY, DISCLAIMER) ---
if st.session_state.step == 0:
    st.title("AI Career Predictor")
    st.subheader("Research Information & Consent | Информационное согласие")
    
    st.markdown("""
    **English:**
    This survey is part of a student research project for the **"Research Methods"** course. 
    * **Anonymity:** No names, student IDs, or emails are collected. Your data is processed in aggregate form.
    * **Voluntary:** You can stop the survey at any time by closing this page.
    * **Purpose:** To analyze how different algorithmic logics influence student perceptions.

    **Русский:**
    Этот опрос является частью студенческого проекта по курсу **"Research Methods"**.
    * **Анонимность:** Мы не собираем имена, ID студентов или адреса почты. Данные обрабатываются в обобщенном виде.
    * **Добровольность:** Вы можете прекратить участие в любое время, просто закрыв страницу.
    * **Цель:** Проанализировать, как различная логика алгоритмов влияет на восприятие студентов.
    """)

    st.warning("""
    **IMPORTANT DISCLAIMER / ВАЖНОЕ УВЕДОМЛЕНИЕ:**
    "The scenarios and system outputs presented here are hypothetical and simplified for research purposes only. They do not represent official career recommendations or a guarantee of success."
    
    "Сценарии и результаты системы являются гипотетическими и упрощенными, представлены исключительно в исследовательских целях и не являются официальными карьерными рекомендациями."
    """)

    st.markdown("---")
    st.caption("By clicking the button below, you confirm that you are an IT student and agree to participate / Нажимая кнопку, вы подтверждаете, что являетесь IT-студентом и согласны на участие.")
    
    st.button("I Agree & Start / Согласен и Начать", on_click=next_step, use_container_width=True)

# --- ШАГ 1: ДЕМОГРАФИЯ ---
elif st.session_state.step == 1:
    st.header("Step 1 | Шаг 1 | 1-қадам")
    st.subheader("General Information / Общая информация")
    
    st.session_state.course = st.selectbox(
        "Year of Study / Курс обучения / Оқу курсы:",
        ["1st Year (1 курс)", "2nd Year (2 курс)", "3rd Year (3 курс)", "4th Year (4 курс)"]
    )
    
    st.session_state.experience = st.radio(
        "Have you ever held an IT internship or relevant job? \n\nБыл ли у вас опыт стажировки или работы в IT? \n\nIT саласында тәжірибеңіз бар ма?",
        ["Yes / Да / Иә", "No / Нет / Жоқ"]
    )
    
    st.button("Next / Далее / Келесі", on_click=next_step, use_container_width=True)

# --- ШАГ 2: ВВОД ДАННЫХ (MAJOR + SUBJECTS) ---
elif st.session_state.step == 2:
    st.markdown("<style>button[data-testid='stMultiSelectSelectAll'] { display: none !important; }</style>", unsafe_allow_html=True)
    
    st.header("Step 2 | Шаг 2 | 2-қадам")
    st.subheader("Select your Major / Выберите специальность:")
    
    st.session_state.major = st.selectbox("Major Selection", list(majors_data.keys()), label_visibility="collapsed")
    
    st.divider()
    st.caption("Select exactly 3 favorite/confident subjects / Выберите ровно 3 предмета:")
    
    subjects_list = majors_data[st.session_state.major]
    st.session_state.selected_subjects = st.multiselect(
        "Subjects", subjects_list, max_selections=3, label_visibility="collapsed"
    )
    
    if len(st.session_state.selected_subjects) == 3:
        st.button("Analyze profile / Анализировать профиль", on_click=next_step, use_container_width=True)
    else:
        st.warning("Please select exactly 3 subjects / Выберите ровно 3 предмета / Нақты 3 пәнді таңдаңыз.")

# --- ШАГ 3: РЕЗУЛЬТАТЫ + ОЦЕНКА (Within-Subjects + Multi-item + Attention Check) ---
elif st.session_state.step == 3:
    st.title("AI Analysis Results")
    
    if 'analyzed' not in st.session_state:
        with st.spinner("Analyzing profile via different algorithmic logics..."):
            time.sleep(2.5) 
        st.session_state.analyzed = True
        
    st.success("""
    **Analysis Complete!** Please evaluate these 3 different models carefully. 
    (1 = Strongly Disagree, 5 = Strongly Agree)
    """)
    
    # Константы для логики (согласно твоему коду)
    major = st.session_state.major
    subjects = st.session_state.selected_subjects
    
    if "Data" in major:
        skill_rec, market_rec = "Data Analyst", "Data Engineer"
        interest_rec = "AI Researcher" if "Machine Learning" in subjects else "Quantitative Analyst"
    elif "Cyber" in major:
        skill_rec, market_rec = "InfoSec Specialist", "Cloud Security Architect"
        interest_rec = "Penetration Tester" if "Ethical Hacking" in subjects else "Cryptography Engineer"
    elif "Management" in major:
        skill_rec, market_rec = "Digital Product Designer", "IT Project Manager"
        interest_rec = "UX/UI Researcher" if "UX/UI Fundamentals" in subjects else "Creative Director"
    else: 
        skill_rec, market_rec = "Backend Engineer", "Full-Stack Developer"
        interest_rec = "Mobile Architect" if "iOS/Android mobile applications development" in subjects else "DevOps Engineer"

    # Рандомизация (защита от Order Bias)
    models =[
        {"id": "M1", "rec": skill_rec, "logic": "Academic Skill Matching"},
        {"id": "M2", "rec": market_rec, "logic": "Market Demand & Salary Trends"},
        {"id": "M3", "rec": interest_rec, "logic": "Individual Subject Interests"}
    ]
    
    if 'shuffled_models' not in st.session_state:
        random.shuffle(models)
        st.session_state.shuffled_models = models

    with st.form("results_form"):
        responses = {}
        
        for i, m in enumerate(st.session_state.shuffled_models):
            st.subheader(f"Recommendation {i+1}: **{m['rec']}**")
            st.caption(f"System Logic: {m['logic']}")
            
            # ACCURACY (Multi-item)
            st.write("— How accurately does this reflect your potential?")
            responses[f"{m['id']}_Acc1"] = st.radio(f"acc1_{m['id']}", [1,2,3,4,5], index=None, horizontal=True, key=f"q1_{m['id']}", label_visibility="collapsed")
            
            st.write("— This path aligns with my actual technical skills.")
            responses[f"{m['id']}_Acc2"] = st.radio(f"acc2_{m['id']}", [1,2,3,4,5], index=None, horizontal=True, key=f"q2_{m['id']}", label_visibility="collapsed")
            
            # INTENT (Multi-item)
            st.write("— How likely are you to follow this advice?")
            responses[f"{m['id']}_Int1"] = st.radio(f"int1_{m['id']}", [1,2,3,4,5], index=None, horizontal=True, key=f"q3_{m['id']}", label_visibility="collapsed")
            
            st.write("— I plan to research this career path further.")
            responses[f"{m['id']}_Int2"] = st.radio(f"int2_{m['id']}", [1,2,3,4,5], index=None, horizontal=True, key=f"q4_{m['id']}", label_visibility="collapsed")
            
            # ATTENTION CHECK (Reverse-coded)
            st.write("— I would **never** choose this career path.")
            responses[f"{m['id']}_Att"] = st.radio(f"att_{m['id']}", [1,2,3,4,5], index=None, horizontal=True, key=f"q5_{m['id']}", label_visibility="collapsed")
            st.divider()

        if st.form_submit_button("Submit Evaluations / Отправить оценки", use_container_width=True):
            if None in responses.values():
                st.error("Please answer all questions before submitting.")
            else:
                conn = st.connection("gsheets", type=GSheetsConnection)
                new_row = {
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Course": st.session_state.course, 
                    "Experience": st.session_state.experience,
                    "Major": st.session_state.major.split(" / ")[0],
                    "M1_Rec": skill_rec, "M1_Acc1": responses["M1_Acc1"], "M1_Acc2": responses["M1_Acc2"], "M1_Int1": responses["M1_Int1"], "M1_Int2": responses["M1_Int2"], "M1_Att": responses["M1_Att"],
                    "M2_Rec": market_rec, "M2_Acc1": responses["M2_Acc1"], "M2_Acc2": responses["M2_Acc2"], "M2_Int1": responses["M2_Int1"], "M2_Int2": responses["M2_Int2"], "M2_Att": responses["M2_Att"],
                    "M3_Rec": interest_rec, "M3_Acc1": responses["M3_Acc1"], "M3_Acc2": responses["M3_Acc2"], "M3_Int1": responses["M3_Int1"], "M3_Int2": responses["M3_Int2"], "M3_Att": responses["M3_Att"]
                }
                try:
                    df = conn.read(worksheet="Sheet1", ttl=0)
                    updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.session_state.step = 4
                    st.rerun()
                except Exception as e: 
                    st.error(f"Error connecting to database: {e}")

# --- ШАГ 4: ФИНАЛ ---
elif st.session_state.step == 4:
    st.title("Thank you! | Спасибо! | Рақмет!")
    st.balloons()
    st.success("Your responses have been recorded anonymously for our Research Methods project.")
    st.markdown("""
    Your contribution helps us understand how students interact with automated decision-making systems. 
    You may now close this tab.
    """)