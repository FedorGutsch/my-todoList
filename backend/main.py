from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

from .settings import Settings


app = FastAPI()
settings = Settings()
engine = create_engine(str(settings.postgres_link))


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
