import asyncio
import time

from sqlalchemy import func
from .redis_client import redis_pool
from .database import async_session_generator
from .models import EmailTask, TaskStatus
import aiosmtplib
from email.mime.text import MIMEText
from .config import SMTP_CONFIG


async def proccess_email_task(task_id: str):
    redis = redis.Redis(connection_pool=redis_pool)
    async with async_session_generator() as session:
        task = await session.get(EmailTask, task_id)
        if not task:
            return None
        task.status = TaskStatus.PROCESSING
        await session.commit()

        try:
            msg = MIMEText(task.body, "html" if task.is_html else "plain")
            msg["Subject"] = task.subject
            msg["From"] = SMTP_CONFIG["from"]
            msg["To"] = task.to

            await aiosmtplib.send(
                msg,
                hostname=SMTP_CONFIG["host"],
                port=SMTP_CONFIG["port"],
                use_tls=True,
                username=SMTP_CONFIG["username"],
                password=SMTP_CONFIG["password"],
            )
            task.status = TaskStatus.COMPLETED
            task.updated_at = func.now()
        except Exception as e:
            task.status = TaskStatus.FAILED
            await session.commit()
            retry_after = min(60 * (task.retry_count + 1), 300)
            await redis.zadd("email_retry", {task_id: time.time() + retry_after})
            task.retry_count += 1


async def email_worker():
    redis = redis.Redis(connection_pool=redis_pool)
    while True:
        now = time.time()
        retry_tasks = await redis.zrangebyscore("email_retry", 0, now)
        for task_id in retry_tasks:
            await redis.rpush("email_queue", task_id)
            await redis.zrem("email_retry", task_id)

        _, task_id = await redis.brpop("email_queue", timeout=5)
        if task_id:
            asyncio.create_task(proccess_email_task(task_id))
