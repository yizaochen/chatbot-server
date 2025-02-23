from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    String,
    DateTime,
    Enum,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


FileStatusEnum = Enum(
    "wait-for-process",
    "processing",
    "upload-failed",
    "uploaded",
    "wait-for-delete",
    "deleted",
    "delete-failed",
    "failed",
    name="file_status_enum",
    create_constraint=True,  # Ensures only allowed values are stored
    validate_strings=True,  # Ensures case-insensitive validation
)


user_index_association = Table(
    "user_index",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("index_id", Integer, ForeignKey("ai_search_index.id"), primary_key=True),
)
assistant_index_association = Table(
    "assistant_index",
    Base.metadata,
    Column("assistant_id", Integer, ForeignKey("assistants.id"), primary_key=True),
    Column("index_id", Integer, ForeignKey("ai_search_index.id"), primary_key=True),
)
user_assistant_association = Table(
    "user_assistant",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("assistant_id", Integer, ForeignKey("assistants.id"), primary_key=True),
)


class AISearchIndex(Base):
    __tablename__ = "ai_search_index"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    index_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    users = relationship(
        "User",
        secondary=user_index_association,
        back_populates="index_list",
        lazy="selectin",
    )
    assistants = relationship(
        "Assistant",
        secondary=assistant_index_association,
        back_populates="index_list",
        lazy="selectin",
    )


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

    index_list = relationship(
        "AISearchIndex",
        secondary=user_index_association,
        back_populates="users",
        lazy="selectin",
    )
    assistants = relationship(
        "Assistant",
        secondary=user_assistant_association,
        back_populates="users",
        lazy="selectin",
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

    # Relationship to Threads
    threads = relationship(
        "Thread",
        back_populates="assistant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Relationship to Users
    users = relationship(
        "User",
        secondary=user_assistant_association,
        back_populates="assistants",
        lazy="selectin",
    )

    # Relationship to AISearchIndex
    index_list = relationship(
        "AISearchIndex",
        secondary=assistant_index_association,
        back_populates="assistants",
        lazy="selectin",
    )


class Thread(Base):
    """
    In chatbot, a thread is a conversation session between a user and the AI model.
    """

    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(None), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    assistant_id: Mapped[int] = mapped_column(
        ForeignKey("assistants.id"), index=True, nullable=True
    )
    activated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=func.now()
    )

    # Relationship to Messages
    messages = relationship(
        "Message",
        back_populates="thread",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    thread_id: Mapped[int] = mapped_column(
        ForeignKey("threads.id"), index=True, nullable=False
    )
    ai_generated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    content: Mapped[str] = mapped_column(String(None), nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[int] = mapped_column(Integer, nullable=True)
    created_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )

    # Relationship to Sources
    sources = relationship(
        "SourceInfoSQL",
        back_populates="message",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Relationship to Threads
    thread = relationship("Thread", back_populates="messages", lazy="selectin")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id"), index=True, nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    feedback: Mapped[str] = mapped_column(String(255), nullable=False)
    created_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )

    # Relationship to Message
    message = relationship("Message", back_populates="feedbacks", lazy="selectin")


class SourceInfoSQL(Base):
    __tablename__ = "source_info"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id"), index=True, nullable=True
    )
    source_file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    page_number_list: Mapped[str] = mapped_column(String(255), nullable=True)
    image_path_list: Mapped[str] = mapped_column(String(1000), nullable=True)

    file_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationship to Message
    message = relationship("Message", back_populates="sources", lazy="selectin")


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    index_id: Mapped[int] = mapped_column(
        ForeignKey("ai_search_index.id"), index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    file_dir_name: Mapped[str] = mapped_column(String(128), nullable=False)
    n_pages: Mapped[int] = mapped_column(Integer, nullable=False)
    size: Mapped[float] = mapped_column(Float, nullable=False)
    process_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[Enum] = mapped_column(
        FileStatusEnum,
        nullable=False,
        default="wait-for-process",
        index=True,
    )
    last_change_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
