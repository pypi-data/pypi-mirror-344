MineLead Python Library
=======================

Огляд
-----
`mine_lead` — це Python SDK для роботи з API MineLead. Бібліотека дозволяє шукати компанії, домени, та отримувати email-адреси за допомогою запитів до MineLead API.

Встановлення
------------
Встановити бібліотеку можна через `pip`:

.. code-block:: bash

    pip install mine_lead

(Або через встановлення залежностей із `requirements.txt`.)

Структура проєкту
-----------------
- **enums**: Перерахування статусів пошуку.
- **exceptions**: Класи для обробки винятків при роботі з API.
- **responses**: Моделі відповідей для різних типів запитів.
- **MineLead.py**: Основний клієнт для взаємодії з API.

Використання
------------

.. code-block:: python

    from mine_lead import MineLead

    ml = MineLead(api_key="YOUR_API_KEY")

    # Пошук email за доменом
    response = ml.search_email(domain="example.com")
    for email in response.emails:
        print(email.address)

    # Пошук компанії
    company_info = ml.search_company(name="Example Company")
    print(company_info.name)

Документація модулів
---------------------

- **mine_lead.enums**

  - `MLSearchStatus`: Статуси запитів пошуку в MineLead.

- **mine_lead.exceptions**

  - `MLException`: Базовий клас винятків.
  - Інші спеціалізовані винятки для обробки помилок API.

- **mine_lead.responses**

  - `MLResponse`: Базовий клас відповіді API.
  - `MLSearchEmailResponse`: Відповідь при пошуку email за доменом.
  - `MLSearchResponse`: Відповідь при пошуку компаній.

Ліцензія
--------
Цей проєкт ліцензований під MIT License.

