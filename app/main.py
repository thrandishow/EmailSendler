import asyncio
import uuid
from fastapi import FastAPI, HTTPException, BackgroundTasks
from .worker import email_worker
from .database import init_db, async_session_generator
from .models import EmailTask, TaskStatus
from .redis_client import redis_pool

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()  # Создаём таблицы
    asyncio.create_task(email_worker())  # Запускаем воркер


app.post("/send-email")


async def send_email(to: str, subject: str, body: str, is_html: bool = False):
    # Генерируем ID и сохраняем в БД
    task_id = str(uuid.uuid4())
    async with async_session_generator() as session:
        task = EmailTask(
            id=task_id,
            to=to,
            subject=subject,
            body=body,
            is_html=is_html,
            status=TaskStatus.PENDING,
        )
        session.add(task)
        await session.commit()

    # Добавляем в очередь Redis
    redis = redis.Redis(connection_pool=redis_pool)
    await redis.rpush("email_queue", task_id)

    return {"task_id": task_id, "status": "queued"}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    async with async_session_generator() as session:
        task = await session.get(EmailTask, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {
            "id": task.id,
            "status": task.status,
            "to": task.to,
            "subject": task.subject,
            "retry_count": task.retry_count,
        }
