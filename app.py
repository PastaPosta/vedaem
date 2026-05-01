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
