from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from .settings import Settings
from .database import get_engine, get_session_local, init_db, User, Todo

app = FastAPI(title="Todo List API", description="API для управления задачами")
settings = Settings()

# Инициализация базы данных
engine = get_engine(str(settings.DATABASE_URL))
SessionLocal = get_session_local(engine)

# Создаем таблицы при запуске
init_db(engine)


# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic модели
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    user_id: int
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True


# Роуты для пользователей
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    # Проверяем, существует ли пользователь с таким email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    # Создаем нового пользователя
    new_user = User(email=user_data.email, password_hash=user_data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить информацию о пользователе"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# Роуты для задач (todos)
@app.get("/users/{user_id}/todos", response_model=List[TodoResponse])
def get_todos(user_id: int, db: Session = Depends(get_db)):
    """Получить все задачи пользователя"""
    # Проверяем существование пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    todos = db.query(Todo).filter(Todo.user_id == user_id).all()
    return todos


@app.get("/users/{user_id}/todos/{todo_id}", response_model=TodoResponse)
def get_todo(user_id: int, todo_id: int, db: Session = Depends(get_db)):
    """Получить конкретную задачу"""
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return todo


@app.post("/users/{user_id}/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(user_id: int, todo_data: TodoCreate, db: Session = Depends(get_db)):
    """Создать новую задачу"""
    # Проверяем существование пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=user_id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.put("/users/{user_id}/todos/{todo_id}", response_model=TodoResponse)
def update_todo(user_id: int, todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db)):
    """Обновить задачу"""
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.is_completed is not None:
        todo.is_completed = todo_data.is_completed
    
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/users/{user_id}/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user_id: int, todo_id: int, db: Session = Depends(get_db)):
    """Удалить задачу"""
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    db.delete(todo)
    db.commit()
    return None


@app.get("/")
def read_root():
    """Корневой эндпоинт"""
    return {"message": "Добро пожаловать в Todo List API!", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)