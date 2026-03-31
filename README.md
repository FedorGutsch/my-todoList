# my-todoList

Небольшой проект на FastAPI + SQLAlchemy - полноценное To-Do приложение.

## 📋 Описание

Это полноценное To-Do приложение с:
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: HTML/CSS/JavaScript (адаптивный дизайн)
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker + Docker Compose

## 🚀 Быстрый старт

### 1. Запуск приложения

```bash
docker-compose up --build
```

### 2. Доступ к сервисам

- **Фронтенд (To-Do приложение)**: http://localhost:3000
- **API документация (Swagger)**: http://localhost:8000/docs
- **CloudBeaver (управление БД)**: http://localhost:8978

## 📁 Структура проекта

```
my-todoList/
├── backend/
│   ├── main.py          # Основной файл API
│   ├── database.py      # Модели базы данных
│   ├── settings.py      # Настройки приложения
│   └── Dockerfile       # Docker конфигурация бэкенда
├── frontend/
│   └── index.html       # Фронтенд приложение
├── docker-compose.yml   # Docker Compose конфигурация
├── requirements.txt     # Python зависимости
├── .env                 # Переменные окружения
└── README.md           # Этот файл
```

## 🔧 API Endpoints

### Пользователи
- `POST /users` - Регистрация нового пользователя
- `GET /users/{user_id}` - Получение информации о пользователе

### Задачи (Todos)
- `GET /users/{user_id}/todos` - Получить все задачи пользователя
- `GET /users/{user_id}/todos/{todo_id}` - Получить конкретную задачу
- `POST /users/{user_id}/todos` - Создать новую задачу
- `PUT /users/{user_id}/todos/{todo_id}` - Обновить задачу
- `DELETE /users/{user_id}/todos/{todo_id}` - Удалить задачу

## 💡 Использование

1. Откройте http://localhost:3000 в браузере
2. Введите email и пароль для регистрации
3. Нажмите "Зарегистрироваться / Войти"
4. Добавляйте, редактируйте и удаляйте задачи
5. Отмечайте задачи как выполненные

## 🛠 Технологии

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL 16
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **DevOps**: Docker, Docker Compose

## 📝 Примечания

- Данные пользователей сохраняются в базе данных PostgreSQL
- Пароли хранятся в открытом виде (для демонстрации)
- Приложение поддерживает несколько пользователей
- Каждая задача принадлежит конкретному пользователю 
