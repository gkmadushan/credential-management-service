from sqlalchemy import Boolean, Column, DateTime, LargeBinary, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Secret(Base):
    __tablename__ = 'secret'

    id = Column(UUID, primary_key=True)
    resource_id = Column(UUID, nullable=False)
    encrypted_key = Column(String(6000))
    public_key = Column(String(6000))
    expire_at = Column(DateTime)
    active = Column(Boolean, nullable=False, server_default=text("false"))