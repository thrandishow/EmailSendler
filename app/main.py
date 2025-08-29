from fastapi import FastAPI, BackgroundTasks
from .schemas import Email
from .email_service import generate_email_message,send_email

app = FastAPI()


@app.post("/send-email/")
async def email_worker(email_data: Email,background_tasks: BackgroundTasks):
    """Добавляет задачу в очередь"""
    email_object = await generate_email_message(to=email_data.to,subject=email_data.subject)
    background_tasks.add_task(send_email,email_object)
    return {"message": "Email добавлен в очередь на отправку"}
