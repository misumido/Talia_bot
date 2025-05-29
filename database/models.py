from sqlalchemy import (Column, Integer,
                        String, DateTime)
from database import Base
class Inactive_User(Base):
    __tablename__ = "inactive"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    reg_date = Column(DateTime)

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    name = Column(String)
    phone_number = Column(String)
    ref_amount = Column(Integer, default=0)
    user_lvl = Column(Integer, default=0)
    inviter = Column(String, nullable=True, default=None)
    reg_date = Column(DateTime)

class Materials(Base):
    __tablename__ = "meterials"
    id = Column(Integer,primary_key=True, autoincrement=True)
    type = Column(String)
    media_id = Column(Integer, nullable=True, default= None)
    text = Column(String, nullable=True, default= None)
    refs_amount = Column(Integer)
    level = Column(Integer, default=0)
    reg_date = Column(DateTime)
class AdminMessages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    media_id = Column(Integer, nullable=True, default= None)
    text = Column(String, nullable=True, default= None)
    reg_date = Column(DateTime)


class AdminUTM(Base):
    __tablename__ = "utm"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    amount = Column(Integer, default=0)
    reg_date = Column(DateTime)

class AdminChannel(Base):
    __tablename__ = "channel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, default=-1002149803283)
    channel_url = Column(String, default="https://t.me/+GJxLztYeOIMyZTQy")
    reg_date = Column(DateTime)




