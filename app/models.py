from sqlalchemy import TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class EmailTask(Base):
    __tablename__ = "email_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    to: Mapped[str] = mapped_column(nullable=False)
    subject: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
    is_html: Mapped[bool] = mapped_column(default=False)
    status: Mapped[Enum[TaskStatus]] = mapped_column(default=TaskStatus.PENDING)
    created_at: Mapped[TIMESTAMP] = mapped_column(default=TIMESTAMP)
    updated_at: Mapped[TIMESTAMP] = mapped_column(default=TIMESTAMP)
