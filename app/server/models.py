# models here - db diagram : https://dbdiagram.io/d/6304c4b5f1a9b01b0fc7dc8a

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


# user class
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('rolePermissions.role_id'))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    reg_at = Column(DateTime)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

    users = relationship("RolePermission", back_populates='roleId')

# rolePermission Table
class RolePermission(Base):
    __tablename__ = 'rolePermissions'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), unique=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    roleId = relationship("User", back_populates='users')
    roles = relationship("Role", back_populates='userRole')
    permission = relationship("Permission", back_populates='userPermission')

# Role table
class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    active = Column(Boolean)
    created_At = Column(DateTime)
    updated_At = Column(DateTime)
    content = Column(String)

    userRole = relationship("RolePermission", back_populates='roles')

# permission table
class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    content = Column(String)

    userPermission = relationship("RolePermission", back_populates='permission')
