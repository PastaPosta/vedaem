import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

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
    
    **Добропло пожаловать!** Эта система использует передовые алгоритмы для прогнозирования оптимального карьерного пути на основе вашего профиля.
    
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
    **Analysis Complete!** Here are your 3 tailored recommendations. Please evaluate **each** carefully.  
    
    **Анализ завершен!** Вот 3 индивидуальные рекомендации. Пожалуйста, внимательно оцените **каждую** из них.  
    
    **Талдау аяқталды!** Міне 3 жеке ұсыныс. **Әр** ұсынысты мұқият бағалауыңызды сұраймыз.
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
        interest_rec = "Penetration Tester / Пентестер (Этичный хакер) / Пентестер" if "Ethical Hacking" in subjects else "Cryptography Engineer / Инженер-криптограф / Криптография инженері"
    elif "Management" in major:
        skill_rec = "Digital Product Designer / Дизайнер цифровых продуктов / Цифрлық өнім дизайнері"
        market_rec = "IT Project Manager / IT Проджект-менеджер / IT Жоба менеджері"
        interest_rec = "UX/UI Researcher / UX/UI Исследователь / UX/UI Зерттеушісі" if "UX/UI Fundamentals" in subjects else "Creative Director / Креативный директор / Креативті директор"
    else: 
        skill_rec = "Backend Engineer / Backend-разработчик / Backend-әзірлеуші"
        market_rec = "Full-Stack Developer / Full-Stack Разработчик / Full-Stack Әзірлеуші"
        interest_rec = "Mobile Architect / Мобильный архитектор / Мобильді сәулетші" if "iOS/Android mobile applications development" in subjects else "DevOps Engineer / DevOps-инженер / DevOps-инженері"

    with st.form("results_form"):
        # MODEL 1
        st.subheader("Model 1 | Модель 1 | 1-модель")
        st.markdown(f"**Career / Профессия / Мансап:** **{skill_rec}**")
        st.caption("Logic: Academic skills matching")
        
        st.write("How accurately does this reflect your potential? (1 = Min, 5 = Max)")
        acc_1 = st.radio("A1", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key='a1', label_visibility="collapsed")
        
        st.write("How likely are you to pursue this? (1 = Min, 5 = Max)")
        int_1 = st.radio("I1", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key='i1', label_visibility="collapsed")
        st.divider()

        # MODEL 2
        st.subheader("Model 2 | Модель 2 | 2-модель")
        st.markdown(f"**Career / Профессия / Мансап:** **{market_rec}**")
        st.caption("Logic: Market demand & salary")
        
        st.write("How accurately does this reflect your potential? (1 = Min, 5 = Max)")
        acc_2 = st.radio("A2", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key='a2', label_visibility="collapsed")
        
        st.write("How likely are you to pursue this? (1 = Min, 5 = Max)")
        int_2 = st.radio("I2", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key='i2', label_visibility="collapsed")
        st.divider()

        # MODEL 3
        st.subheader("Model 3 | Модель 3 | 3-модель")
        st.markdown(f"**Career / Профессия / Мансап:** **{interest_rec}**")
        st.caption("Logic: Subject interests")
        
        st.write("How accurately does this reflect your potential? (1 = Min, 5 = Max)")
        acc_3 = st.radio("A3", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key='a3', label_visibility="collapsed")
        
        st.write("How likely are you to pursue this? (1 = Min, 5 = Max)")
        int_3 = st.radio("I3", options=[1, 2, 3, 4, 5], index=None, horizontal=True, key='i3', label_visibility="collapsed")
        
        submitted = st.form_submit_button("Submit Evaluations / Отправить оценки / Бағалауларды жіберу")
        
        if submitted:
            if None in [acc_1, int_1, acc_2, int_2, acc_3, int_3]:
                st.error("Please answer all questions before submitting.")
            else:
                conn = st.connection("gsheets", type=GSheetsConnection)
                new_data = pd.DataFrame([{
                    "Course": st.session_state.course,
                    "Experience": st.session_state.experience,
                    "Major": st.session_state.major.split(" / ")[0],
                    "Subjects": ", ".join(st.session_state.selected_subjects),
                    "M1_Skill_Rec": skill_rec.split(" / ")[0], "M1_Accuracy": acc_1, "M1_Intent": int_1,
                    "M2_Market_Rec": market_rec.split(" / ")[0], "M2_Accuracy": acc_2, "M2_Intent": int_2,
                    "M3_Interest_Rec": interest_rec.split(" / ")[0], "M3_Accuracy": acc_3, "M3_Intent": int_3
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
