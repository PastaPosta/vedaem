import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="AI Career Predictor", layout="centered")

# --- СЛОВАРИ ---
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
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

# --- ШАГ 1: ОБЩИЕ ДАННЫЕ ---
if st.session_state.step == 1:
    st.title("AI Career Predictor")
    st.caption("Research Simulation | Симуляция исследования | Зерттеу симуляциясы")
    
    st.markdown("""
    **Welcome!** This system uses advanced algorithmic logic to predict your optimal career path based on your academic profile.
    
    **Добро пожаловать!** Эта система использует передовые алгоритмы для прогнозирования оптимального карьерного пути на основе вашего профиля.
    
    **Қош келдіңіз!** Бұл жүйе сіздің академиялық профиліңізге негізделген оңтайлы мансап жолын болжау үшін озық алгоритмдерді пайдаланады.
    """)
    
    st.divider()
    st.header("Step 1 | Шаг 1 | 1-қадам")
    
    st.session_state.course = st.selectbox(
        "Year of Study / Курс обучения / Оқу курсы:",["1st Year (1 курс)", "2nd Year (2 курс)", "3rd Year (3 курс)", "4th Year (4 курс)"]
    )
    
    st.session_state.experience = st.radio(
        "Have you ever held an IT internship or relevant job? \n\nБыл ли у вас опыт стажировки или работы в IT? \n\nIT саласында тағылымдамадан немесе жұмыстан өтіп көрдіңіз бе?",["Yes / Да / Иә", "No / Нет / Жоқ"]
    )
    
    st.button("Next / Далее / Келесі", on_click=next_step)

# --- ШАГ 2: ВЫБОР НАПРАВЛЕНИЯ И ПРЕДМЕТОВ ---
elif st.session_state.step == 2:
    # CSS только для скрытия 'Select all' в списке предметов
    st.markdown(
        """
        <style>
        button[data-testid="stMultiSelectSelectAll"] { display: none !important; }
        div[data-baseweb="popover"] ul li:first-child { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("Step 2 | Шаг 2 | 2-қадам")
    st.subheader("Select your Major/Program \nВыберите вашу специальность/программу \nМамандығыңызды/бағдарламаңызды таңдаңыз:")
    
    st.session_state.major = st.selectbox(
        "Major Selection", 
        list(majors_data.keys()),
        label_visibility="collapsed" 
    )
    
    st.divider()
    
    st.caption("""
    **Select your top 3 favorite subjects:** Choose the subjects where you feel most confident or interested in.  
    
    **Выберите 3 ваших любимых предмета:** Выберите предметы, в которых вы чувствуете себя наиболее уверенно или которые вам интересны.  
    
    **Өзіңізге ұнайтын 3 пәнді таңдаңыз:** Өзіңізді сенімді сезінетін немесе қызықтыратын пәндерді таңдаңыз.
    """)
    
    subjects_list = majors_data[st.session_state.major]
    st.session_state.selected_subjects = st.multiselect(
        "Choose exactly 3 subjects / Выберите ровно 3 предмета / Нақты 3 пәнді таңдаңыз:", 
        subjects_list,
        max_selections=3
    )
    
    if len(st.session_state.selected_subjects) == 3:
        st.button("Analyze my profile / Анализировать профиль / Профилімді талдау", on_click=next_step)
    else:
        st.warning("Please select exactly 3 subjects / Выберите ровно 3 предмета / Нақты 3 пәнді таңдаңыз.")


# --- ШАГ 3: РЕЗУЛЬТАТЫ И ОЦЕНКА ---
elif st.session_state.step == 3:
    st.title("AI Analysis Results | Результаты ИИ | ЖИ талдау нәтижелері")
    
    if 'analyzed' not in st.session_state:
        with st.spinner("Analyzing... / Анализ... / Талдау..."):
            time.sleep(2.5) 
        st.session_state.analyzed = True
        
    st.success("""
    **Analysis Complete!** Here are your 3 tailored recommendations. Please evaluate **each** carefully (1 = Strongly Disagree/Min, 5 = Strongly Agree/Max).  
    
    **Анализ завершен!** Вот 3 индивидуальные рекомендации. Пожалуйста, внимательно оцените **каждую** (1 = Абсолютно не согласен/Мин, 5 = Абсолютно согласен/Макс).  
    """)
    
    major = st.session_state.major
    subjects = st.session_state.selected_subjects
    
    # Логика рекомендаций
    if "Data" in major:
        skill_rec = "Data Analyst / Аналитик данных / Деректер талдаушысы"
        market_rec = "Data Engineer / Инженер данных / Деректер инженері"
        interest_rec = "AI Researcher / ИИ-исследователь / ЖИ-зерттеушісі" if "Machine Learning" in subjects else "Quantitative Analyst / Квант-аналитик / Кванттық талдаушы"
    elif "Cyber" in major:
        skill_rec = "InfoSec Specialist / Специалист по ИБ / АҚ маманы"
        market_rec = "Cloud Security Architect / Архитектор облачной безопасности / Бұлттық қауіпсіздік сәулетшісі"
        interest_rec = "Penetration Tester / Пентестер (Этичный хакер)" if "Ethical Hacking" in subjects else "Cryptography Engineer / Инженер-криптограф"
    elif "Management" in major:
        skill_rec = "Digital Product Designer / Дизайнер цифровых продуктов"
        market_rec = "IT Project Manager / IT Проджект-менеджер"
        interest_rec = "UX/UI Researcher / UX/UI Исследователь" if "UX/UI Fundamentals" in subjects else "Creative Director / Креативный директор"
    else: 
        skill_rec = "Backend Engineer / Backend-разработчик"
        market_rec = "Full-Stack Developer / Full-Stack Разработчик"
        interest_rec = "Mobile Architect / Мобильный архитектор" if "iOS/Android mobile applications development" in subjects else "DevOps Engineer / DevOps-инженер"

    # Формируем список моделей (это нужно для рандомизации)
    models =[
        {"id": "M1", "type": "Skill", "rec": skill_rec, "logic": "Academic skills matching"},
        {"id": "M2", "type": "Market", "rec": market_rec, "logic": "Market demand & salary"},
        {"id": "M3", "type": "Interest", "rec": interest_rec, "logic": "Subject interests"}
    ]
    
    # Рандомизируем порядок выдачи моделей (сохраняем в session_state, чтобы при клике не перемешивалось заново)
    if 'shuffled_models' not in st.session_state:
        random.shuffle(models)
        st.session_state.shuffled_models = models

    with st.form("results_form"):
        responses = {} # Словарь для сбора ответов
        
        # Выводим модели в случайном порядке
        for i, model in enumerate(st.session_state.shuffled_models):
            st.subheader(f"Model {i+1} | Модель {i+1} | {i+1}-модель")
            st.markdown(f"**Career / Профессия / Мансап:** **{model['rec']}**")
            st.caption(f"Logic: {model['logic']}")
            
            # --- Perceived Accuracy (2 вопроса) ---
            st.write("**Q1:** How accurately does this reflect your potential? / Насколько точно это отражает ваш потенциал?")
            responses[f"{model['id']}_Acc1"] = st.radio(f"A1_{model['id']}", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key=f"a1_{model['id']}", label_visibility="collapsed")
            
            st.write("**Q2:** This path matches my actual technical skills. / Этот путь соответствует моим реальным навыкам.")
            responses[f"{model['id']}_Acc2"] = st.radio(f"A2_{model['id']}", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key=f"a2_{model['id']}", label_visibility="collapsed")
            
            # --- Intent to Pursue (2 вопроса) ---
            st.write("**Q3:** How likely are you to pursue this? / Насколько вероятно, что вы выберете этот путь?")
            responses[f"{model['id']}_Int1"] = st.radio(f"I1_{model['id']}", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key=f"i1_{model['id']}", label_visibility="collapsed")
            
            st.write("**Q4:** I plan to research this career path further. / Я планирую изучить эту профессию подробнее.")
            responses[f"{model['id']}_Int2"] = st.radio(f"I2_{model['id']}", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key=f"i2_{model['id']}", label_visibility="collapsed")
            
            # --- ATTENTION CHECK (Reverse-coded item) ---
            st.write("**Q5:** I would never choose this career path. / Я бы никогда не выбрал эту профессию.")
            responses[f"{model['id']}_AttCheck"] = st.radio(f"Att_{model['id']}", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key=f"att_{model['id']}", label_visibility="collapsed")
            
            st.divider()

        submitted = st.form_submit_button("Submit Evaluations / Отправить оценки / Бағалауларды жіберу")
        
        if submitted:
            # Проверка, что на все 15 вопросов (3 модели * 5 вопросов) дан ответ
            if None in responses.values():
                st.error("Please answer all questions before submitting. / Пожалуйста, ответьте на все вопросы перед отправкой.")
            else:
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                # Формируем итоговый DataFrame (с добавлением колонок AttCheck)
                new_data = pd.DataFrame([{
                    "Course": st.session_state.course,
                    "Experience": st.session_state.experience,
                    "Major": st.session_state.major.split(" / ")[0],
                    "Subjects": ", ".join(st.session_state.selected_subjects),
                    
                    "M1_Skill_Rec": skill_rec.split(" / ")[0], 
                    "M1_Acc1": responses["M1_Acc1"], "M1_Acc2": responses["M1_Acc2"], 
                    "M1_Int1": responses["M1_Int1"], "M1_Int2": responses["M1_Int2"],
                    "M1_AttCheck": responses["M1_AttCheck"],
                    
                    "M2_Market_Rec": market_rec.split(" / ")[0], 
                    "M2_Acc1": responses["M2_Acc1"], "M2_Acc2": responses["M2_Acc2"], 
                    "M2_Int1": responses["M2_Int1"], "M2_Int2": responses["M2_Int2"],
                    "M2_AttCheck": responses["M2_AttCheck"],
                    
                    "M3_Interest_Rec": interest_rec.split(" / ")[0], 
                    "M3_Acc1": responses["M3_Acc1"], "M3_Acc2": responses["M3_Acc2"], 
                    "M3_Int1": responses["M3_Int1"], "M3_Int2": responses["M3_Int2"],
                    "M3_AttCheck": responses["M3_AttCheck"]
                }])
                
                try:
                    existing_data = conn.read(worksheet="Sheet1", ttl=0) 
                    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.session_state.step = 4 
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# --- ШАГ 4: ФИНАЛ ---
elif st.session_state.step == 4:
    st.title("Thank you! | Спасибо! | Рақмет!")
    st.success("Your responses have been successfully recorded.")
    st.markdown("Your input is incredibly valuable for our research.")
