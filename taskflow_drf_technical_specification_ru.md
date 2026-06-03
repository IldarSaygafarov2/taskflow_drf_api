# Техническое задание
# Проект: TaskFlow API
# Стек: Django + Django REST Framework

---

# 1. Общая информация о проекте

## Название проекта
TaskFlow API

## Тип проекта
REST API система управления задачами.

## Назначение проекта
Проект предназначен для практического обучения студентов разработке backend-приложений с использованием Django REST Framework.

В рамках проекта студенты должны разработать production-ready API для системы управления задачами, проектами и командами.

Проект должен максимально приближать студентов к реальной backend-разработке.

---

# 2. Основные цели проекта

## Основные задачи

Студенты должны научиться:

- проектировать REST API;
- работать с Django REST Framework;
- строить архитектуру backend-приложений;
- реализовывать аутентификацию и авторизацию;
- работать с PostgreSQL;
- использовать Celery и Redis;
- реализовывать бизнес-логику;
- оптимизировать запросы;
- работать с Docker;
- документировать API;
- подготавливать backend к production.

---

# 3. Технологический стек

## Backend
- Python 3.11+
- Django 5+
- Django REST Framework

## База данных
- PostgreSQL

## Асинхронные задачи
- Celery
- Redis

## Документация
- drf-spectacular
- Swagger UI

## Аутентификация
- JWT (SimpleJWT)

## DevOps
- Docker
- Docker Compose
- Gunicorn
- Nginx

## Тестирование
- Pytest
- pytest-django
- factory-boy

---

# 4. Архитектура проекта

## Структура приложений

Проект должен быть разделен на отдельные Django apps:

- users
- workspaces
- projects
- boards
- tasks
- comments
- attachments
- notifications
- activity_logs
- common

---

# 5. Пользовательская система

## Модель пользователя

Необходимо реализовать кастомную модель пользователя.

## Поля пользователя

- id
- email
- username
- first_name
- last_name
- avatar
- password
- is_active
- is_staff
- created_at
- updated_at

## Функциональность

### Регистрация
Пользователь должен иметь возможность:
- зарегистрироваться;
- получить JWT токен;
- подтвердить email.

### Авторизация
Пользователь должен иметь возможность:
- войти в систему;
- обновить access token;
- выйти из системы.

### Профиль
Пользователь должен иметь возможность:
- просматривать профиль;
- редактировать профиль;
- менять пароль.

### Восстановление пароля
Необходимо реализовать:
- отправку email;
- reset token;
- смену пароля.

---

# 6. Workspace система

## Назначение
Workspace — это рабочее пространство команды.

## Модель Workspace

### Поля
- id
- name
- slug
- description
- owner
- created_at
- updated_at

## Модель WorkspaceMember

### Поля
- workspace
- user
- role
- joined_at

## Роли пользователей

Необходимо реализовать роли:

- Owner
- Admin
- Manager
- Member
- Guest

## Функциональность

### Workspace

Пользователь должен иметь возможность:

- создать workspace;
- редактировать workspace;
- удалить workspace;
- просматривать список workspaces;
- приглашать участников.

### Участники

Необходимо реализовать:

- добавление участников;
- удаление участников;
- изменение ролей;
- список участников.

---

# 7. Система проектов

## Назначение
Каждый workspace может содержать несколько проектов.

## Модель Project

### Поля
- id
- workspace
- name
- description
- status
- start_date
- end_date
- created_by
- created_at
- updated_at

## Статусы проекта

Необходимо реализовать:

- Active
- Archived
- Completed

## Функциональность

### Проекты

Пользователь должен иметь возможность:

- создавать проекты;
- редактировать проекты;
- архивировать проекты;
- удалять проекты;
- просматривать список проектов.

---

# 8. Kanban доски

## Назначение

Приложение boards отвечает за реализацию Kanban логики проекта.

Kanban система должна обеспечивать:

- создание досок;
- создание колонок;
- изменение порядка колонок;
- перемещение задач между колонками;
- поддержку drag-and-drop логики;
- хранение workflow проекта.

---

## Django app

Необходимо создать отдельное приложение:

- boards

---

## Модель Board

### Назначение

Board представляет Kanban доску внутри проекта.

### Поля

- id
- project
- name
- created_at
- updated_at

---

## Модель Column

### Назначение

Column представляет колонку Kanban доски.

### Поля

- id
- board
- name
- position
- created_at
- updated_at

---

## Базовые колонки

При создании новой доски необходимо автоматически создавать базовые колонки:

- Todo
- In Progress
- Review
- Done

---

## Функциональность

### Boards

Пользователь должен иметь возможность:

- создавать доски;
- редактировать доски;
- удалять доски;
- получать список досок проекта;
- получать детали доски.

---

### Columns

Пользователь должен иметь возможность:

- создавать колонки;
- редактировать колонки;
- удалять колонки;
- изменять порядок колонок;
- получать список колонок доски.

---

## Reorder логика

Необходимо реализовать:

- изменение позиции колонок;
- изменение позиции задач;
- drag-and-drop backend логику.

---

## Перемещение задач

Пользователь должен иметь возможность:

- перемещать задачи между колонками;
- менять порядок задач внутри колонки.

---

## Требования к реализации

Необходимо продемонстрировать:

- atomic transactions;
- ordering logic;
- business logic services;
- race condition protection.

---

## Рекомендуемые service functions

Необходимо реализовать отдельный service layer.

Примеры:

- move_task()
- reorder_columns()
- reorder_tasks()
- create_default_columns()

---

## Что должны изучить студенты

В рамках boards app студенты должны изучить:

- ordering fields;
- drag-and-drop backend logic;
- transactions;
- service layer architecture;
- separation of concerns;
- business logic isolation.

---

# 9. Система задач

## Назначение
Основной модуль проекта.

## Модель Task

### Поля
- id
- project
- board_column
- title
- description
- status
- priority
- assignee
- reporter
- deadline
- estimated_hours
- spent_hours
- is_completed
- created_at
- updated_at

## Приоритеты

Необходимо реализовать:

- Low
- Medium
- High
- Critical

## Статусы задач

Необходимо реализовать:

- Todo
- In Progress
- Review
- Done

## Функциональность

### Задачи

Пользователь должен иметь возможность:

- создавать задачи;
- редактировать задачи;
- удалять задачи;
- назначать исполнителей;
- изменять статус;
- изменять приоритет;
- добавлять дедлайн;
- перемещать задачи между колонками.

### Дополнительные возможности

Необходимо реализовать:

- soft delete;
- фильтрацию;
- сортировку;
- поиск;
- пагинацию.

---

# 10. Комментарии

## Модель Comment

### Поля
- id
- task
- author
- content
- created_at
- updated_at

## Функциональность

Пользователь должен иметь возможность:

- добавлять комментарии;
- редактировать комментарии;
- удалять комментарии;
- просматривать комментарии задачи.

---

# 11. Attachments

## Назначение
Система загрузки файлов.

## Модель Attachment

### Поля
- id
- task
- file
- uploaded_by
- created_at

## Функциональность

Пользователь должен иметь возможность:

- загружать файлы;
- удалять файлы;
- просматривать список файлов задачи.

## Ограничения

Необходимо реализовать:

- ограничение размера файла;
- валидацию типов файлов.

---

# 12. Labels

## Модель Label

### Поля
- id
- project
- name
- color

## Функциональность

Пользователь должен иметь возможность:

- создавать labels;
- удалять labels;
- назначать labels задачам;
- фильтровать задачи по labels.

---

# 13. Notifications

## Назначение
Система уведомлений.

## Модель Notification

### Поля
- id
- user
- title
- message
- is_read
- created_at

## События уведомлений

Необходимо отправлять уведомления при:

- назначении задачи;
- комментарии к задаче;
- изменении статуса;
- приближении дедлайна.

## Реализация

Уведомления должны отправляться через:

- Celery;
- Redis.

---

# 14. Activity Log

## Назначение
Логирование действий пользователей.

## Модель ActivityLog

### Поля
- id
- user
- action
- entity_type
- entity_id
- description
- created_at

## События

Необходимо логировать:

- создание задач;
- изменение задач;
- удаление задач;
- изменение статусов;
- создание комментариев.

---

# 15. Permissions

## Требования

Необходимо реализовать object-level permissions.

## Правила доступа

### Owner
Полный доступ.

### Admin
Управление проектами и участниками.

### Manager
Управление задачами.

### Member
Работа только со своими задачами.

### Guest
Только просмотр.

---

# 16. Фильтрация и поиск

## Требования

Необходимо реализовать:

- filtering;
- search;
- ordering;
- pagination.

## Фильтрация задач

По:

- статусу;
- приоритету;
- исполнителю;
- дедлайну;
- labels;
- проекту.

---

# 17. API документация

## Требования

Необходимо реализовать:

- OpenAPI schema;
- Swagger UI;
- Redoc.

## Документация должна содержать

- описание endpoints;
- примеры запросов;
- примеры ответов;
- описание ошибок.

---

# 18. Тестирование

## Требования

Необходимо покрыть тестами:

- authentication;
- permissions;
- CRUD операции;
- бизнес-логику;
- API endpoints.

## Используемые инструменты

- pytest;
- pytest-django;
- factory-boy.

---

# 19. Оптимизация

## Требования

Необходимо продемонстрировать:

- select_related;
- prefetch_related;
- оптимизацию запросов;
- решение проблемы N+1.

---

# 20. Docker окружение

## Требования

Необходимо создать:

- Dockerfile;
- docker-compose.yml.

## Сервисы

Проект должен запускать:

- Django app;
- PostgreSQL;
- Redis;
- Celery worker;
- Celery beat;
- Nginx.

---

# 21. Deployment

## Требования

Необходимо подготовить production deployment:

- Gunicorn;
- Nginx;
- HTTPS;
- environment variables;
- static/media handling.

---

# 22. Структура API

## Пример endpoints

### Auth
- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/refresh/
- POST /api/auth/logout/

### Users
- GET /api/users/me/
- PATCH /api/users/me/

### Workspaces
- GET /api/workspaces/
- POST /api/workspaces/
- GET /api/workspaces/{id}/
- PATCH /api/workspaces/{id}/
- DELETE /api/workspaces/{id}/

### Projects
- GET /api/projects/
- POST /api/projects/
- GET /api/projects/{id}/

### Tasks
- GET /api/tasks/
- POST /api/tasks/
- GET /api/tasks/{id}/
- PATCH /api/tasks/{id}/
- DELETE /api/tasks/{id}/

### Comments
- GET /api/tasks/{id}/comments/
- POST /api/tasks/{id}/comments/

### Attachments
- GET /api/tasks/{task_id}/attachments/
- POST /api/tasks/{task_id}/attachments/
- DELETE /api/tasks/{task_id}/attachments/{id}/

### Boards
- GET    /api/projects/{project_id}/boards/
- POST   /api/projects/{project_id}/boards/

- GET    /api/boards/{id}/
- PATCH  /api/boards/{id}/
- DELETE /api/boards/{id}/
- GET    /api/boards/{id}/kanban/

- GET    /api/boards/{id}/columns/
- POST   /api/boards/{id}/columns/

- GET    /api/columns/{id}/
- PATCH  /api/columns/{id}/
- DELETE /api/columns/{id}/

- POST   /api/boards/{id}/reorder-columns/

- POST   /api/boards/move-task/
- POST   /api/columns/{id}/reorder-tasks/


# 23. Требования к качеству кода

## Необходимо соблюдать

- PEP8;
- typing;
- разделение ответственности;
- чистую архитектуру;
- DRY;
- SOLID базового уровня.

---

# 24. Дополнительные возможности

## Рекомендуется реализовать

- WebSocket уведомления;
- realtime обновления;
- email reminders;
- soft delete;
- audit system;
- rate limiting.

---

# 25. Результат проекта

По завершению проекта студенты должны получить:

- production-ready REST API;
- опыт работы с DRF;
- опыт работы с PostgreSQL;
- понимание backend-архитектуры;
- опыт работы с Celery и Redis;
- навыки Docker deployment;
- полноценный backend проект для портфолио.

---

# 26. Рекомендуемая структура курса

## Этап 1 — Основы DRF
- модели;
- serializers;
- ViewSets;
- CRUD.

## Этап 2 — Авторизация и permissions
- JWT;
- permissions;
- roles.

## Этап 3 — Основная бизнес-логика
- tasks;
- comments;
- labels;
- filtering.

## Этап 4 — Продвинутые темы
- Celery;
- Redis;
- notifications;
- optimization.

## Этап 5 — Production
- Docker;
- deployment;
- testing;
- documentation.

