from datetime import datetime, timezone
from uuid import UUID
from enum import Enum
from sqlalchemy import Enum as SAEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from authorization.models import User


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
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewed_by_id: Mapped[UUID | None] = mapped_column(ForeignKey('users.id'))
    reason: Mapped[str | None]

    address: Mapped["Address"] = relationship(back_populates="shop")
    owner: Mapped["User"] = relationship(back_populates='shops', foreign_keys=[owner_id])
    reviewed_by: Mapped["User"] = relationship(back_populates='review_application', foreign_keys=[reviewed_by_id])
    shop_versions: Mapped[list["ShopVersion"]] = relationship(back_populates='shop')

class Address(Base):
    __tablename__ = 'addresses'
    city: Mapped[str]
    street: Mapped[str]
    home: Mapped[str]
    flat: Mapped[int | None]
    entrance: Mapped[int | None]
    latitude: Mapped[float]
    longitude: Mapped[float]

    shop: Mapped["Shop"] = relationship(back_populates='address')
    address_version: Mapped["ShopVersion"] = relationship(back_populates='address')


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
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewed_by_id: Mapped[UUID | None] = mapped_column(ForeignKey('users.id'))
    reason: Mapped[str | None]

    address: Mapped["Address"] = relationship(back_populates="address_version")
    owner: Mapped["User"] = relationship(back_populates='shops_versions', foreign_keys=[owner_id])
    reviewed_by: Mapped["User"] = relationship(back_populates='review_application_version', foreign_keys=[reviewed_by_id])
    shop: Mapped["Shop"] = relationship(back_populates='shop_versions')
