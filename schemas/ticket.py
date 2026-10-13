from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from models.ticket import TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: TicketStatus | None = None
    priority: TicketPriority | None = None

    @model_validator(mode="after")
    def require_update_field(self):
        if not self.model_fields_set:
            raise ValueError(
                "Provide at least one field to update"
            )
        return self


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime


class TicketListResponse(BaseModel):
    items: list[TicketResponse]
    total: int
    page: int
    limit: int


class TicketStatusCount(BaseModel):
    status: TicketStatus
    count: int


class TicketStatsResponse(BaseModel):
    total: int
    by_status: list[TicketStatusCount]