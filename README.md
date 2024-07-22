# Life Helper

Это веб-приложение на базе Django, предлагающее широкий спектр функций, включая аутентификацию, интеграцию с API погоды и отслеживание финансов. Пользователи могут регистрироваться, входить в систему и управлять своими профилями, отслеживать расходы с помощью визуализации в виде круговой диаграммы, добавлять и редактировать категории расходов, просматривать список друзей и добавлять их в друзья(завершено),вести с ними диалог(посредством websocket) (функция находится в разработке и завершена на 80%). Вся система упакована в Docker и Docker Compose для удобного развертывания и масштабируемости.

## Особенности

1. **Аутентификация и Регистрация**:
   - Пользователи могут создавать учетные записи и безопасно входить в систему, чтобы получить доступ к функциям приложения.

2. **Интеграция с API Погоды**:
   - Приложение интегрируется с API погоды, чтобы предоставлять пользователям информацию о погоде в реальном времени.
   - Содержит самые разнообразные данные начиная от температуры/уф индекса/направления ветра и заканчивания фазой луны/восходом/состоянием погоды, на ближайшие 3 дня

3. **Отслеживание Финансов**:
   - Включает в себя визуализацию в виде круговой диаграммы для отслеживания расходов.
   - Пользователи могут добавлять, редактировать и категоризировать расходы.

4. **Список Друзей и Управление ими**:
   - Пользователи могут просматривать список друзей и добавлять новых друзей.
   - Могут вести диалог с ними(для это нужно перейти в список друзей и нажать на кнопку чата с другом)

5. **Редактирование Профиля**:
   - Пользователи могут редактировать свои профили для обновления личной информации.

## Установка и Настройка

Чтобы запустить проект локально, выполните следующие шаги:

1. **Склонируйте этот репозиторий:**
```bash
git clone https://github.com/atomsis/VC.git
```
--------------------------------------------
Если планируете запускать НЕ через контейнер
--------------------------------------------
2. (**Without_docker.**)
```bash
pip install -r requirements.txt
```
--------------------------------------------
2. (**With_docker.**)
   - Установите Docker и Docker Compose, если они еще не установлены.

4. **Соберите и запустите контейнеры Docker:**
```bash
docker compose up --build
```

4. **Получите доступ к приложению в веб-браузере по адресу `http://localhost:8000`.**

## Использование

После запуска приложения пользователи могут:

- Зарегистрировать новую учетную запись или войти с существующими учетными данными.
- Получить информацию о погоде через соответствующую интеграцию API.
- Отслеживать расходы, добавлять новые расходы, редактировать категории и визуализировать шаблоны расходов.
- Управлять своим списком друзей: добавлять,удалять,вести с ними диалог.
- Редактировать свои профили.

## Вклад

Приветствуются вклады! Если у вас есть предложения, отчеты об ошибках или запросы на добавление функций, пожалуйста, откройте задачу или отправьте запрос на добавление в GitHub.


## Благодарности

- Отдельная благодарность сообществу Django за отличную документацию и поддержку.
- Погодные данные предоставлены WeatherAPI.com.
- Визуализация в виде круговой диаграммы вдохновлена [вставьте сами где видели такое :) ].

## Контакт

По всем вопросам или поддержке не стесняйтесь связаться с сопровождающим проекта по адресу atomsis01@mail.ru.

