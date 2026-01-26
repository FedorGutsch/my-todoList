from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uvicorn

from .settings import Settings

app = FastAPI()
settings = Settings()
engine = create_engine(str(settings.postgres_link))

class UserData(BaseModel):
    email: EmailStr
    password: str



@app.get("/users/{user_id}/todos")
def get_everything(user_id: int):
    try:
        with engine.connect() as connection:
            # Безопасный параметризованный запрос
            result = connection.execute(
                text("SELECT id, title, is_completed FROM todos WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            todos = [dict(row._mapping) for row in result]
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    
    
@app.post("/users/login")
def add_user(userData: UserData):
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("INSERT INTO users(email, password_hash) VALUES(:email, :password)"),
                {'email': userData.email, 'password': userData.password}
            )
        return "User has been created"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    
if __name__ == "__main__":
    uvicorn.run(app)