from datetime import datetime, timezone
from uuid import UUID
from enum import Enum
from sqlalchemy import Enum as SAEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class ApplicationStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECT = 'reject'


class Shop(Base):
    __tablename__ = 'shops'
    title: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]

    owner_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'))
    status: Mapped["ApplicationStatus"] = mapped_column(SAEnum(ApplicationStatus),
                                                        name='application_status',
                                                        default=ApplicationStatus.PENDING)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                  onupdate=lambda: datetime.now(tz=timezone.utc))
    reviewed_by_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    reason: Mapped[str | None] = None

class Address(Base):
    __tablename__ = 'addresses'
    city: Mapped[str]
    street: Mapped[str]
    home: Mapped[str]
    flat: Mapped[int | None]
    entrance: Mapped[int | None]
    latitude: Mapped[float]
    longitude: Mapped[float]



class ShopVersion(Base):
    __tablename__ = 'shop_versions'
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id'))
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]

    owner_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'))
    status: Mapped["ApplicationStatus"] = mapped_column(SAEnum(ApplicationStatus),
                                                        name='application_status',
                                                        default=ApplicationStatus.PENDING)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                  onupdate=lambda: datetime.now(tz=timezone.utc))
    reviewed_by_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    reason: Mapped[str | None] = None

