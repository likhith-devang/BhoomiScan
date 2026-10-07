from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants import CASE_STATUS_ACTIVE
from app.database import Base


class PropertyCase(Base):
    __tablename__ = "property_cases"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    domain: Mapped[str] = mapped_column(String(32), nullable=False)
    property_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default=CASE_STATUS_ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="property_cases")
    documents: Mapped[list["Document"]] = relationship(
        back_populates="property_case", cascade="all, delete-orphan"
    )
    analyses: Mapped[list["Analysis"]] = relationship(
        back_populates="property_case", cascade="all, delete-orphan"
    )
    comparisons: Mapped[list["DocumentComparison"]] = relationship(
        back_populates="property_case", cascade="all, delete-orphan"
    )
    reports: Mapped[list["FinalReport"]] = relationship(
        back_populates="property_case", cascade="all, delete-orphan"
    )
