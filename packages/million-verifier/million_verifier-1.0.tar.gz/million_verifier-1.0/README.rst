Million Verifier Python Library
================================

Огляд
-----
Бібліотека `million_verifier` — це зручний Python SDK для роботи з API MillionVerifier. Вона дозволяє завантажувати файли, перевіряти email-адреси, отримувати результати перевірки та обробляти відповіді API.

Встановлення
------------
Встановити бібліотеку можна через `pip`:

.. code-block:: bash

    pip install million_verifier

(Або використати `requirements.txt` для встановлення залежностей.)

Структура проєкту
-----------------
- **enums**: Перерахування статусів і помилок.
- **exceptions**: Обробка винятків API.
- **responses**: Класи відповідей для різних типів запитів.
- **MillionVerifier.py**: Основний клієнт для взаємодії з API.

Використання
------------

.. code-block:: python

    from million_verifier import MillionVerifier

    mv = MillionVerifier(api_key="YOUR_API_KEY")

    # Перевірка однієї email-адреси
    response = mv.verify_email("example@example.com")
    print(response.status)

    # Завантаження файлу для масової перевірки
    file_response = mv.upload_file("emails.csv")
    print(file_response.file_id)

Документація модулів
---------------------

- **million_verifier.enums**

  - `MVError`: Типи можливих помилок API.
  - `MVStatus`: Статуси результатів перевірки email-адрес.

- **million_verifier.exceptions**

  - `MVException`: Базовий клас винятків.
  - Інші спеціалізовані винятки для обробки помилок API.

- **million_verifier.responses**

  - `MVResponse`: Базова модель відповіді API.
  - `MVVerifyResponse`: Відповідь на перевірку email.
  - `MVFileResponse`: Відповідь при обробці файлів.
  - `MVUploadFileResponse`: Відповідь на завантаження файлу.
  - `MVGetFileResponse`: Отримання результатів перевірки файлів.

Ліцензія
--------
Цей проєкт ліцензований під MIT License.

