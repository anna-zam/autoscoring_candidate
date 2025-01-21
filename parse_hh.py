import requests
from bs4 import BeautifulSoup


def get_html(url: str):
    """Функция для получения HTML-кода страницы по URL"""
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    response.raise_for_status()
    return response.text


def extract_vacancy_data(html):
    """Функция для извлечения данных вакансии"""
    soup = BeautifulSoup(html, "html.parser")

    # Заголовок вакансии
    title_element = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title_element.text.strip() if title_element else "Заголовок не найден"

    # Зарплата
    salary_element = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-gross"})
    salary = salary_element.text.strip() if salary_element else "Зарплата не указана"

    # Опыт работы
    experience_element = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience_element.text.strip() if experience_element else "Опыт работы не указан"

    # Тип занятости и режим работы
    employment_mode_element = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode_element.text.strip() if employment_mode_element else "Не указано"

    # Компания
    company_element = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company_element.text.strip() if company_element else "Компания не указана"

    # Местоположение
    location_element = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location_element.text.strip() if location_element else "Местоположение не указано"

    # Описание вакансии
    description_element = soup.find("div", {"data-qa": "vacancy-description"})
    description = description_element.text.strip() if description_element else "Описание не указано"

    # Ключевые навыки
    skills_elements = soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})
    skills = [skill.text.strip() for skill in skills_elements] if skills_elements else []

    # Формирование строки в формате Markdown
    skills_list = "\n- ".join(skills) if skills else "Навыки не указаны"
    markdown = f"""
    # {title}

    **Компания:** {company}
    **Зарплата:** {salary}
    **Опыт работы:** {experience}
    **Тип занятости и режим работы:** {employment_mode}
    **Местоположение:** {location}

    ## Описание вакансии
    {description}

    ## Ключевые навыки
    - {skills_list}
    """
    return markdown.strip()

def extract_candidate_data(html):
    """Функция для извлечения данных кандидата"""
    soup = BeautifulSoup(html, 'html.parser')

    # Имя кандидата
    name_element = soup.find('h2', {'data-qa': 'bloko-header-1'})
    name = name_element.text.strip() if name_element else "Имя не указано"

    # Местоположение
    location_element = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location_element.text.strip() if location_element else "Местоположение не указано"

    # Должность
    job_title_element = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title_element.text.strip() if job_title_element else "Должность не указана"

    # Статус поиска работы
    job_status_element = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status_element.text.strip() if job_status_element else "Статус поиска работы не указан"

    # Опыт работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experiences = []
    if experience_section:
        experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
        for item in experience_items:
            period = item.find('div', class_='bloko-column_s-2').text.strip()
            duration = item.find('div', class_='bloko-text').text.strip()
            company = item.find('div', class_='bloko-text_strong').text.strip()
            position = item.find('div', {'data-qa': 'resume-block-experience-position'}).text.strip()
            description = item.find('div', {'data-qa': 'resume-block-experience-description'}).text.strip()
            experiences.append(f"**{period} ({duration})**\n\n*{company}*\n\n**{position}**\n\n{description}")

    # Навыки
    skills_elements = soup.find_all('span', {'data-qa': 'bloko-tag__text'})
    skills = [skill.text.strip() for skill in skills_elements] if skills_elements else []

    # Формирование строки в формате Markdown
    markdown = f"# {name}\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    markdown += "\n\n".join(experiences) if experiences else "Опыт работы не указан\n\n"
    markdown += "## Навыки\n\n"
    markdown += ", ".join(skills) if skills else "Навыки не указаны\n"

    return markdown


def get_candidate_info(url: str):
    html = get_html(url)
    return extract_candidate_data(html)


def get_job_description(url: str):
    html = get_html(url)
    return extract_vacancy_data(html)
