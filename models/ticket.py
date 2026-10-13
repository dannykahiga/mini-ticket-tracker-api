from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    DateTime,
    Enum,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class TicketStatus(str, PyEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class TicketPriority(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Ticket(Base):
    __tablename__ = "tickets"

    __table_args__ = (
        Index("ix_tickets_status", "status"),
        Index("ix_tickets_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[TicketStatus] = mapped_column(
        Enum(
            TicketStatus,
            name="ticket_status",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
        ),
        nullable=False,
        default=TicketStatus.OPEN,
        server_default="open",
    )

    priority: Mapped[TicketPriority] = mapped_column(
        Enum(
            TicketPriority,
            name="ticket_priority",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
        ),
        nullable=False,
        default=TicketPriority.MEDIUM,
        server_default="medium",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )