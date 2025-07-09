Анализатор принадлежности сайта
Простое веб-приложение для проверки, принадлежит ли сайт указанной организации.

Как установить
Скачайте проект:

bash
git clone https://github.com/ваш-логин/website-ownership.git
cd website-ownership
Установите зависимости:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
Запустите:

bash
python manage.py migrate
python manage.py runserver
Откройте в браузере: http://127.0.0.1:8000

Как пользоваться
Введите:

Адрес сайта (например: example.com)

Название вашей организации

ОГРН организации

Нажмите "Проверить"

Получите результат:

Оценка от 0 до 100%

Что было проверено

Какие данные найдены

Что проверяет система
Данные о владельце домена

Упоминание организации на сайте

Наличие реквизитов (ОГРН/ИНН)

Контактные данные

Технологии
Python

Django

WHOIS

HTML анализ
