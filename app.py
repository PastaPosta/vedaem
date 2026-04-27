import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="AI Career Predictor", page_icon="🤖", layout="centered")

# --- СЛОВАРИ С ПРЕДМЕТАМИ ИЗ СИЛЛАБУСОВ NARXOZ ---
# Оставляем ключи на английском, так как они используются в логике рекомендаций
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
    st.title("🎓 AI Career Predictor")
    st.caption("Research Simulation / Симуляция исследования / Зерттеу симуляциясы")
    
    st.info("""
    🇬🇧 **Welcome!** This system uses advanced algorithmic logic to predict your optimal career path based on your academic profile.  
    🇷🇺 **Добро пожаловать!** Эта система использует передовые алгоритмы для прогнозирования оптимального карьерного пути на основе вашего академического профиля.  
    🇰🇿 **Қош келдіңіз!** Бұл жүйе сіздің академиялық профиліңізге негізделген оңтайлы мансап жолын болжау үшін озық алгоритмдерді пайдаланады.
    """)
    
    st.header("Step 1 / Шаг 1 / 1-қадам")
    
    st.session_state.course = st.selectbox(
        "🇬🇧 Year of Study / 🇷🇺 Курс обучения / 🇰🇿 Оқу курсы:",["1st Year (1 курс)", "2nd Year (2 курс)", "3rd Year (3 курс)", "4th Year (4 курс)"]
    )
    
    # IV2: Practical Experience
    st.session_state.experience = st.radio(
        "🇬🇧 Have you ever held an IT internship or relevant job? \n\n🇷🇺 Был ли у вас опыт стажировки или работы в IT? \n\n🇰🇿 IT саласында тағылымдамадан немесе жұмыстан өтіп көрдіңіз бе?", 
        ["Yes / Да / Иә", "No / Нет / Жоқ"]
    )
    
    st.button("Next / Далее / Келесі ➡️", on_click=next_step)

# --- ШАГ 2: ВЫБОР НАПРАВЛЕНИЯ И ПРЕДМЕТОВ ---
elif st.session_state.step == 2:
    st.header("Step 2 / Шаг 2 / 2-қадам")
    
    st.session_state.major = st.selectbox(
        "🇬🇧 Select your Major/Program \n\n🇷🇺 Выберите вашу специальность/программу \n\n🇰🇿 Мамандығыңызды/бағдарламаңызды таңдаңыз:", 
        list(majors_data.keys())
    )
    
    st.markdown("""
    **🇬🇧 Select your top 3 favorite subjects:** Choose the subjects where you feel most confident or interested in.  
    **🇷🇺 Выберите 3 ваших любимых предмета:** Выберите предметы, в которых вы чувствуете себя наиболее уверенно или которые вам интересны.  
    **🇰🇿 Өзіңізге ұнайтын 3 пәнді таңдаңыз:** Өзіңізді сенімді сезінетін немесе қызықтыратын пәндерді таңдаңыз.
    """)
    
    # Динамически подгружаем предметы на основе выбранного Major
    subjects_list = majors_data[st.session_state.major]
    
    st.session_state.selected_subjects = st.multiselect(
        "🇬🇧 Choose exactly 3 subjects / 🇷🇺 Выберите ровно 3 предмета / 🇰🇿 Нақты 3 пәнді таңдаңыз:", 
        subjects_list,
        max_selections=3
    )
    
    if len(st.session_state.selected_subjects) == 3:
        st.button("Analyze my profile / Анализировать профиль / Профилімді талдау 🚀", on_click=next_step)
    else:
        st.warning("""
        🇬🇧 Please select exactly 3 subjects to proceed.  
        🇷🇺 Пожалуйста, выберите ровно 3 предмета для продолжения.  
        🇰🇿 Жалғастыру үшін нақты 3 пәнді таңдаңыз.
        """)


# --- ШАГ 3: ИМИТАЦИЯ ЗАГРУЗКИ И ВЫДАЧА РЕЗУЛЬТАТОВ (IV1 -> DV1, DV2) ---
elif st.session_state.step == 3:
    st.title("🧠 AI Analysis Results / Результаты ИИ / ЖИ талдау нәтижелері")
    
    # Эффект "работы ИИ"
    if 'analyzed' not in st.session_state:
        with st.spinner("🇬🇧 Analyzing... / 🇷🇺 Анализ... / 🇰🇿 Талдау..."):
            time.sleep(2.5) 
        st.session_state.analyzed = True
        
    st.success("""
    🇬🇧 Analysis Complete! Here are your 3 tailored recommendations based on different AI logics. Please evaluate **each** recommendation carefully.  
    🇷🇺 Анализ завершен! Вот 3 индивидуальные рекомендации, основанные на различных алгоритмах ИИ. Пожалуйста, внимательно оцените **каждую** из них.  
    🇰🇿 Талдау аяқталды! Міне, әртүрлі ЖИ алгоритмдеріне негізделген 3 жеке ұсыныс. **Әр** ұсынысты мұқият бағалауыңызды сұраймыз.
    """)
    
    # === ГЕНЕРАЦИЯ ЛОГИКИ В ЗАВИСИМОСТИ ОТ ВЫБОРА ===
    major = st.session_state.major
    subjects = st.session_state.selected_subjects
    
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
        # Model 1
        st.subheader("🟢 Model 1 / Модель 1 / 1-модель")
        st.markdown(f"**Recommendation / Рекомендация / Ұсыныс:** **{skill_rec}**")
        st.caption("""
        🇬🇧 Logic: Matches your baseline academic skills with standard core technical roles.  
        🇷🇺 Логика: Сопоставляет ваши академические навыки со стандартными техническими ролями.  
        🇰🇿 Логика: Негізгі академиялық дағдыларыңызды стандартты техникалық рөлдермен сәйкестендіреді.
        """)
        
        st.write("🇬🇧 How accurately does this reflect your potential? / 🇷🇺 Насколько точно это отражает ваш потенциал? / 🇰🇿 Бұл сіздің әлеуетіңізді қаншалықты дәл көрсетеді? *(1 = Min, 5 = Max)*")
        acc_1 = st.slider("Accuracy 1", 1, 5, 3, key='a1', label_visibility="collapsed")
        
        st.write("🇬🇧 How likely are you to pursue this career path? / 🇷🇺 Насколько вероятно, что вы выберете этот путь? / 🇰🇿 Бұл мансапты таңдау ықтималдығыңыз қандай? *(1 = Min, 5 = Max)*")
        int_1 = st.slider("Intent 1", 1, 5, 3, key='i1', label_visibility="collapsed")
        st.divider()

        # Model 2
        st.subheader("📈 Model 2 / Модель 2 / 2-модель")
        st.markdown(f"**Recommendation / Рекомендация / Ұсыныс:** **{market_rec}**")
        st.caption("""
        🇬🇧 Logic: Prioritizes current industry demand, salary trends, and job availability.  
        🇷🇺 Логика: Приоритет отдается текущему спросу на рынке, зарплатам и наличию вакансий.  
        🇰🇿 Логика: Нарықтағы ағымдағы сұранысқа, жалақы тенденцияларына және жұмыс орындарына басымдық береді.
        """)
        
        st.write("🇬🇧 How accurately does this reflect your potential? / 🇷🇺 Насколько точно это отражает ваш потенциал? / 🇰🇿 Бұл сіздің әлеуетіңізді қаншалықты дәл көрсетеді? *(1 = Min, 5 = Max)*")
        acc_2 = st.slider("Accuracy 2", 1, 5, 3, key='a2', label_visibility="collapsed")
        
        st.write("🇬🇧 How likely are you to pursue this career path? / 🇷🇺 Насколько вероятно, что вы выберете этот путь? / 🇰🇿 Бұл мансапты таңдау ықтималдығыңыз қандай? *(1 = Min, 5 = Max)*")
        int_2 = st.slider("Intent 2", 1, 5, 3, key='i2', label_visibility="collapsed")
        st.divider()

        # Model 3
        st.subheader("💡 Model 3 / Модель 3 / 3-модель")
        st.markdown(f"**Recommendation / Рекомендация / Ұсыныс:** **{interest_rec}**")
        st.caption("""
        🇬🇧 Logic: Prioritizes your specific subject interests for niche/creative career satisfaction.  
        🇷🇺 Логика: Отдает приоритет вашим интересам для узкоспециализированной/творческой карьеры.  
        🇰🇿 Логика: Тар профильді/шығармашылық мансапта қанағаттану үшін қызығушылықтарыңызға басымдық береді.
        """)
        
        st.write("🇬🇧 How accurately does this reflect your potential? / 🇷🇺 Насколько точно это отражает ваш потенциал? / 🇰🇿 Бұл сіздің әлеуетіңізді қаншалықты дәл көрсетеді? *(1 = Min, 5 = Max)*")
        acc_3 = st.slider("Accuracy 3", 1, 5, 3, key='a3', label_visibility="collapsed")
        
        st.write("🇬🇧 How likely are you to pursue this career path? / 🇷🇺 Насколько вероятно, что вы выберете этот путь? / 🇰🇿 Бұл мансапты таңдау ықтималдығыңыз қандай? *(1 = Min, 5 = Max)*")
        int_3 = st.slider("Intent 3", 1, 5, 3, key='i3', label_visibility="collapsed")
        
        submitted = st.form_submit_button("Submit Evaluations / Отправить оценки / Бағалауларды жіберу")
        
        conn = st.connection("gsheets", type=GSheetsConnection)

        if submitted:
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
                existing_data = conn.read(worksheet="Sheet1", ttl=0) 
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                
                st.session_state.step = 4 
                st.rerun()
            except Exception as e:
                st.error(f"Error saving to Google Sheets: {e}")

# --- ШАГ 4: ФИНАЛ ---
elif st.session_state.step == 4:
    st.balloons()
    st.title("✅ Thank you! / Спасибо! / Рақмет!")
    
    st.success("""
    🇬🇧 Your responses have been successfully recorded.  
    🇷🇺 Ваши ответы были успешно записаны.  
    🇰🇿 Сіздің жауаптарыңыз сәтті жазылды.
    """)
    
    st.markdown("""
    🇬🇧 Your input is incredibly valuable for our research on Human-AI Interaction in career systems.  
    🇷🇺 Ваш вклад невероятно ценен для нашего исследования взаимодействия человека и ИИ в карьерных системах.  
    🇰🇿 Сіздің үлесіңіз мансаптық жүйелердегі Адам мен ЖИ өзара әрекеттесуін зерттеуіміз үшін өте құнды.
    
    ---
    *🇬🇧 Note: This was a simulated model for research purposes (Research Methods course).*  
    *🇷🇺 Примечание: Это была симуляционная модель для исследовательских целей (Курс "Методы исследований").*  
    *🇰🇿 Ескерту: Бұл зерттеу мақсатындағы симуляциялық модель болды ("Зерттеу әдістері" курсы).*
    """)