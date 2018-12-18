# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String,Date, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
SQLITE = 'sqlite'

USERS = 'users'
MESSAGES = 'messages'

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id=Column(Integer,unique=True)
    telegram_id = Column(String,unique=True)
    date = Column(DateTime)
    messages = relationship("Messages")
    def __init__(self,user_id,telegram_id,date):
        self.user_id = user_id
        self.telegram_id = telegram_id
        self.date = date

    def __repr__(self):
        return "<User('%s','%s',%s')>" % (self.user_id,self.telegram_id, self.date)

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.telegram_id'))
    message_text = Column(String)
    last_message = Column(Boolean)

    def __init__(self,user_id,message_text,last_message):
        self.user_id = user_id
        self.message_text = message_text
        self.last_message = last_message
    def __repr__(self):
        return "<User('%s','%s,'%s')>" % (self.user_id, self.message_text,self.last_message)

# Создание таблицы
Base.metadata.create_all(engine)