from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models import Ticket, TicketPriority, TicketStatus
from schemas.ticket import (
    TicketCreate,
    TicketListResponse,
    TicketResponse,
    TicketStatsResponse,
    TicketStatusCount,
    TicketUpdate,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
) -> Ticket:
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get("", response_model=TicketListResponse)
def list_tickets(
    status_filter: TicketStatus | None = Query(
        default=None,
        alias="status",
    ),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> TicketListResponse:
    filters = []

    if status_filter is not None:
        filters.append(Ticket.status == status_filter)

    total = db.scalar(
        select(func.count(Ticket.id)).where(*filters)
    ) or 0

    statement = (
        select(Ticket)
        .where(*filters)
        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    tickets = db.scalars(statement).all()

    return TicketListResponse(
        items=tickets,
        total=total,
        page=page,
        limit=limit,
    )


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
) -> Ticket:
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)

    return ticket


@router.get("/stats", response_model=TicketStatsResponse)
def ticket_stats(
    db: Session = Depends(get_db),
) -> TicketStatsResponse:
    rows = db.execute(
        select(Ticket.status, func.count(Ticket.id))
        .group_by(Ticket.status)
    ).all()

    counts = {ticket_status: count for ticket_status, count in rows}

    by_status = [
        TicketStatusCount(
            status=ticket_status,
            count=counts.get(ticket_status, 0),
        )
        for ticket_status in TicketStatus
    ]

    return TicketStatsResponse(
        total=sum(item.count for item in by_status),
        by_status=by_status,
    )