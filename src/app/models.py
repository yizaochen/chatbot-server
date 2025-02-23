from datetime import datetime
from sqlalchemy import (
    Integer,
    Boolean,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )


class LLMModel(Base):
    __tablename__ = "llm_models"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # deployment name


class Assistant(Base):
    """
    This is corresponding to OpenAI GPTs (Assistant) in the chatbot.

    user_id: The creator of the assistant.
    """

    __tablename__ = "assistants"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    system_prompt: Mapped[str] = mapped_column(
        String(None), nullable=True, default=None
    )
    llm_model_id: Mapped[int] = mapped_column(
        ForeignKey("llm_models.id"), index=True, nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    activated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
