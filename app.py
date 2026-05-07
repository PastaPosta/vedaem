import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="AI Career Predictor", layout="centered")

# --- СЛОВАРИ ДАННЫХ (Только Eng / Rus) ---
majors_data = {
    "Statistics & Data Science / Статистика и Data Science":[
        "Machine Learning", "Big Data Analytics", "Introduction to Deep Learning", 
        "Mathematical modeling", "Optimization methods", "Game Theory and Operations Research"
    ],
    "Cybersecurity / Кибербезопасность":[
        "Information Security Fundamentals", "Introduction to Cryptography", 
        "Ethical Hacking", "Network administration", "Reverse Engineering Fundamentals", "Operating system security"
    ],
    "Digital Management & Design / Цифровой Менеджмент и Дизайн":[
        "UX/UI Fundamentals", "Digital Marketing", "Project Management", 
        "Front end development", "3D Modeling and Animation", "Principles of Marketing"
    ],
    "Digital Engineering / Цифровая Инженерия":[
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
    st.header("Step 1 | Шаг 1")
    st.subheader("General Information / Общая информация")
    
    st.session_state.course = st.selectbox(
        "Year of Study / Курс обучения:",["1st Year (1 курс)", "2nd Year (2 курс)", "3rd Year (3 курс)", "4th Year (4 курс)"]
    )
    
    st.session_state.experience = st.radio(
        "Have you ever held an IT internship or relevant job? \n\nБыл ли у вас опыт стажировки или работы в IT?",
        ["Yes / Да", "No / Нет"]
    )
    
    st.button("Next / Далее", on_click=next_step, use_container_width=True)

# --- ШАГ 2: ВВОД ДАННЫХ (MAJOR + SUBJECTS) ---
elif st.session_state.step == 2:
    st.markdown("<style>button[data-testid='stMultiSelectSelectAll'] { display: none !important; }</style>", unsafe_allow_html=True)
    
    st.header("Step 2 | Шаг 2")
    st.subheader("Select your Major / Выберите специальность:")
    
    st.session_state.major = st.selectbox("Major Selection", list(majors_data.keys()), label_visibility="collapsed")
    
    st.divider()
    st.caption("Select exactly 3 favorite/confident subjects / Выберите ровно 3 предмета, в которых вы наиболее уверены:")
    
    subjects_list = majors_data[st.session_state.major]
    st.session_state.selected_subjects = st.multiselect(
        "Subjects", subjects_list, max_selections=3, label_visibility="collapsed"
    )
    
    if len(st.session_state.selected_subjects) == 3:
        st.button("Analyze profile / Анализировать профиль", on_click=next_step, use_container_width=True)
    else:
        st.warning("Please select exactly 3 subjects / Пожалуйста, выберите ровно 3 предмета.")

# --- ШАГ 3: РЕЗУЛЬТАТЫ + ОЦЕНКА ---
elif st.session_state.step == 3:
    st.title("AI Analysis Results | Результаты анализа ИИ")
    
    if 'analyzed' not in st.session_state:
        with st.spinner("Analyzing profile via different algorithmic logics... / Анализ профиля..."):
            time.sleep(2.5) 
        st.session_state.analyzed = True
        
    st.success("""
    **Analysis Complete! / Анализ завершен!** 
    Please evaluate these 3 different models carefully. / Пожалуйста, внимательно оцените эти 3 модели.
    (1 = Strongly Disagree / Абсолютно не согласен, 5 = Strongly Agree / Абсолютно согласен)
    """)
    
    major = st.session_state.major
    subjects = st.session_state.selected_subjects
    
    # Рекомендации с переводами (в базу данных пойдет только английская часть благодаря .split()[0] ниже)
    if "Data" in major:
        skill_rec, market_rec = "Data Analyst / Аналитик данных", "Data Engineer / Инженер данных"
        interest_rec = "AI Researcher / ИИ-исследователь" if "Machine Learning" in subjects else "Quantitative Analyst / Квант-аналитик"
    elif "Cyber" in major:
        skill_rec, market_rec = "InfoSec Specialist / Специалист по кибербезопасности", "Cloud Security Architect / Архитектор облачной безопасности"
        interest_rec = "Penetration Tester / Пентестер (Этичный хакер)" if "Ethical Hacking" in subjects else "Cryptography Engineer / Инженер-криптограф"
    elif "Management" in major:
        skill_rec, market_rec = "Digital Product Designer / Дизайнер цифровых продуктов", "IT Project Manager / IT Проджект-менеджер"
        interest_rec = "UX/UI Researcher / UX/UI Исследователь" if "UX/UI Fundamentals" in subjects else "Creative Director / Креативный директор"
    else: 
        skill_rec, market_rec = "Backend Engineer / Backend-разработчик", "Full-Stack Developer / Full-Stack Разработчик"
        interest_rec = "Mobile Architect / Мобильный архитектор" if "iOS/Android mobile applications development" in subjects else "DevOps Engineer / DevOps-инженер"

    # Рандомизация и логика с переводами
    models =[
        {"id": "M1", "rec": skill_rec, "logic": "Academic Skill Matching / Совпадение академических навыков"},
        {"id": "M2", "rec": market_rec, "logic": "Market Demand & Salary Trends / Востребованность на рынке и зарплаты"},
        {"id": "M3", "rec": interest_rec, "logic": "Individual Subject Interests / Индивидуальные предметные интересы"}
    ]
    
    if 'shuffled_models' not in st.session_state:
        random.shuffle(models)
        st.session_state.shuffled_models = models

    with st.form("results_form"):
        responses = {}
        
        for i, m in enumerate(st.session_state.shuffled_models):
            st.subheader(f"Recommendation {i+1} | Рекомендация {i+1}:")
            st.markdown(f"### **{m['rec']}**")
            st.caption(f"System Logic / Логика системы: *{m['logic']}*")
            
            # ACCURACY (Multi-item)
            st.write("— How accurately does this reflect your potential? / Насколько точно это отражает ваш потенциал?")
            responses[f"{m['id']}_Acc1"] = st.radio(f"acc1_{m['id']}",[1,2,3,4,5], index=None, horizontal=True, key=f"q1_{m['id']}", label_visibility="collapsed")
            
            st.write("— This path aligns with my actual technical skills. / Этот путь соответствует моим реальным техническим навыкам.")
            responses[f"{m['id']}_Acc2"] = st.radio(f"acc2_{m['id']}",[1,2,3,4,5], index=None, horizontal=True, key=f"q2_{m['id']}", label_visibility="collapsed")
            
            # INTENT (Multi-item)
            st.write("— How likely are you to follow this advice? / Насколько вероятно, что вы последуете этому совету?")
            responses[f"{m['id']}_Int1"] = st.radio(f"int1_{m['id']}", [1,2,3,4,5], index=None, horizontal=True, key=f"q3_{m['id']}", label_visibility="collapsed")
            
            st.write("— I plan to research this career path further. / Я планирую изучить этот карьерный путь подробнее.")
            responses[f"{m['id']}_Int2"] = st.radio(f"int2_{m['id']}", [1,2,3,4,5], index=None, horizontal=True, key=f"q4_{m['id']}", label_visibility="collapsed")
            
            # ATTENTION CHECK (Reverse-coded)
            st.write("— I would **never** choose this career path. / Я бы **никогда** не выбрал эту профессию.")
            responses[f"{m['id']}_Att"] = st.radio(f"att_{m['id']}",[1,2,3,4,5], index=None, horizontal=True, key=f"q5_{m['id']}", label_visibility="collapsed")
            st.divider()

        if st.form_submit_button("Submit Evaluations / Отправить оценки", use_container_width=True):
            if None in responses.values():
                st.error("Please answer all questions before submitting. / Пожалуйста, ответьте на все вопросы перед отправкой.")
            else:
                conn = st.connection("gsheets", type=GSheetsConnection)
                new_row = {
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Course": st.session_state.course.split(" ")[0], # Очистит "1st Year (1 курс)" -> "1st" 
                    "Experience": st.session_state.experience.split(" / ")[0], # Очистит "Yes / Да" -> "Yes"
                    "Major": st.session_state.major.split(" / ")[0], # Оставит только инглиш
                    "Subjects": ", ".join(st.session_state.selected_subjects), # <- ВОТ ТО, ЧТО БЫЛО УПУЩЕНО В ПРОШЛЫЙ РАЗ!
                    
                    # split(" / ")[0] очищает названия профессий до чистенького английского перед записью в гугл таблицу:
                    "M1_Rec": skill_rec.split(" / ")[0], "M1_Acc1": responses["M1_Acc1"], "M1_Acc2": responses["M1_Acc2"], "M1_Int1": responses["M1_Int1"], "M1_Int2": responses["M1_Int2"], "M1_Att": responses["M1_Att"],
                    "M2_Rec": market_rec.split(" / ")[0], "M2_Acc1": responses["M2_Acc1"], "M2_Acc2": responses["M2_Acc2"], "M2_Int1": responses["M2_Int1"], "M2_Int2": responses["M2_Int2"], "M2_Att": responses["M2_Att"],
                    "M3_Rec": interest_rec.split(" / ")[0], "M3_Acc1": responses["M3_Acc1"], "M3_Acc2": responses["M3_Acc2"], "M3_Int1": responses["M3_Int1"], "M3_Int2": responses["M3_Int2"], "M3_Att": responses["M3_Att"]
                }
                try:
                    df = conn.read(worksheet="Sheet1", ttl=0)
                    updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.session_state.step = 4
                    st.rerun()
                except Exception as e: 
                    st.error(f"Error connecting to database / Ошибка подключения к базе данных: {e}")

# --- ШАГ 4: ФИНАЛ ---
elif st.session_state.step == 4:
    st.title("Thank you! | Спасибо!")
    st.balloons()
    st.success("Your responses have been recorded anonymously for our Research Methods project. / Ваши ответы были анонимно записаны для нашего проекта по Research Methods.")
    st.markdown("""
    Your contribution helps us understand how students interact with automated decision-making systems. 
    You may now close this tab.
    
    Ваш вклад помогает нам понять, как студенты взаимодействуют с системами автоматического принятия решений. 
    Теперь вы можете закрыть эту вкладку.
    """)