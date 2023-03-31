import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSONB, datetime: DateTime(timezone=True)}
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    mongo_val: Mapped[Optional[dict[str, Any]]]
    username: Mapped[Optional[str]]
    password_hash: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    scope: Mapped[Optional[dict[str, Any]]]

    ssh_keys: Mapped[List["Sshkey"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Sshkey(Base):
    __tablename__ = "sshkey"
    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    mongo_val: Mapped[Optional[dict[str, Any]]]
    name: Mapped[Optional[str]]
    fingerprint: Mapped[Optional[str]]
    type: Mapped[Optional[str]]
    key: Mapped[Optional[str]]
    added: Mapped[Optional[datetime]]
    last_used: Mapped[Optional[datetime]]
    pkcs8_key: Mapped[Optional[str]]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="ssh_keys")
