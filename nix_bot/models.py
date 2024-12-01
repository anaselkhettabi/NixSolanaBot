from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    chat_id = Column(String, unique=True, nullable=False)
    subscription_status = Column(Boolean, default=False)
    wallet_public_key = Column(String, unique=True, nullable=True)
    wallet_private_key = Column(String, nullable=True)

class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    wallet_address = Column(String, unique=True, nullable=False)
    kol_name = Column(String, nullable=False)
