from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from core import Base
from uuid import UUID, uuid4
from enum import Enum, auto


class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(primary_key=True,
                                     default=uuid4)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    role: Mapped[list["Role"]] = relationship('Role',
                                              secondary='user_role_associations',
                                              back_populates='user')

class Role(Base):
    __tablename__ = 'roles'
    title: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    permission: Mapped[list['Permission']] = relationship('Permission',
                                                          secondary='role_permission_associations',
                                                          back_populates='role')
    user: Mapped[list['User']] = relationship('User',
                                              secondary='user_role_associations',
                                              back_populates='role')

class PermissionEnum(str, Enum):
    pass


class Permission(Base):
    __tablename__ = 'permissions'
    title: Mapped[str] = mapped_column(unique=True)
    role: Mapped[list[Role]] = relationship('Role',
                                            secondary='role_permission_associations',
                                            back_populates='permission')



class RolePermissionAssociation(Base):
    __tablename__ = 'role_permission_associations'
    __table_args__ = (UniqueConstraint('role_id', 'permission_id', name='idx_role_permission'),)
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id))
    permission_id: Mapped[int] = mapped_column(ForeignKey(Permission.id))

class UserRoleAssociation(Base):
    __tablename__ = 'user_role_associations'
    __table_args__ = (UniqueConstraint('user_id', 'role_id', name='idx_user_role'),)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(User.id))
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id))