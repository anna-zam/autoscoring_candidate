import os
import openai
import streamlit as st
import toml
from parse_hh import get_candidate_info, get_job_description

# Установите API-ключ
secrets = toml.load(".streamlit/secrets.toml")
openai.api_key = secrets["OPENAI_API_KEY"]
client = openai.Client(
    api_key=secrets["OPENAI_API_KEY"]
)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.
Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу.
Потом представь результат в виде оценки от 1 до 10.
""".strip()

def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content

st.title("CV Scoring App")

job_description_url = st.text_area("Введите URL вакансии")
cv_url = st.text_area("Введите URL резюме")

if st.button("Оценить резюме"):
    with st.spinner("Оценка резюме..."):
        try:
            # Получение описания вакансии и резюме
            job_description = get_job_description(job_description_url)
            cv = get_candidate_info(cv_url)

            st.write("Описание вакансии:")
            st.write(job_description)
            st.write("Резюме:")
            st.write(cv)

            # Формируем запрос для GPT
            user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
            response = request_gpt(SYSTEM_PROMPT, user_prompt)

            st.write("Результат:")
            st.write(response)
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
