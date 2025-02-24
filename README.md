# Telegram Geometry Bot
## Автор: Чуев Савва, Б05-327
### Описание проекта и реализуемый функционал
Телеграм-бот предназначен для решения задач по геометрии.

Задачи разбиты на 3 категории:
  1. Легкий уровень
  2. Средний уровень
  3. Сложный уровень

Пользователь в любой момент может:

  1. Запросить новую задачу желаемой сложности
  2. Запросить решение последней задачи (это автоматически отмечает задачу решённой)
  3. Отметить последнюю задачу решённой

Решённые задачи больше не попадаются.
Для сброса списка решённых задач есть специальная команда "/reset_solved".
Для просмотра полного списка команд есть команда "/help".


### Архитектура проекта
Данный проект реализован на языке программирования Python и
использует следующие библиотеки:

  1. aiogram - для коммуникации с пользователем через телеграм-бота
  2. asyncio - для асинхронной обработки задач
  3. random - для выбора случайной задачи из списка нерешённых
  4. sqlalchemy - для асинхронной работы с базой данных

Проект имеет следующую структуру:

    app
        database
            models.py
            requests.py
        handlers.py
        keyboards.py
    db.sqlite3
    main.py
    README.md

  1. app - директория с кодом проекта.

  2. app/database - директория для коммуникации с базой данных.
  
  3. app/database/models.py - файл для создания базы данных
и объявления трёх её таблиц - User (хранится id
телеграм-аккаунта пользователя), Complexity (хранится сложность задачи),
Problem (хранится текст условия, текст решения, сложность).

  4. app/database/requests.py - файл для взаимодействия с базой данных
и добавления новых задач.

  5. app/handlers.py - файл для обработки запросов пользователя с
последующим запросом в базу данных через файл app/database/requests.py.

  6. app/keyboards.py - файл для создания окон с выбором сообщения.

  7. db.sqlite3 - база данных.

  8. main.py - файл для запуска телеграм-бота.

  9. README.md - файл с описанием проекта, его целей и архитектуры.

В проекте использованы следующие классы:

  1. class Base(AsyncAttrs, DeclarativeBase) -
Базовый класс для создания таблицы

  2. class User(Base) - таблица пользователей

  3. class Complexity(Base) - таблица сложностей

  4. class Problem(Base) - таблица задач

  5. class ProblemSolving(StatesGroup) - класс для поддержки
состояний во время взаимодействия с пользователем


### Возможные улучшения
1. Добавить больше задач.

2. К каждому условию и решению задачи прикреплять картинку
для более комфортного восприятия.

3. Добавить пользователям возможность оценивать задачу в формате
лайк/дизлайк. Это позволит выдавать задачи не случайно, а из
соотношения лайков и дизлайков.

4. Добавить ежедневную/еженедельную рассылку с задачей дня/недели.

5. Добавить возможность пользователям предлагать свои задачи, и
сохранять их в специальной таблице в базе данных. После чего администраторы
смогут одобрить или отклонить предложенную задачу.
