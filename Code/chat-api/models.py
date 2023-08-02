from database import Base 
from sqlalchemy import Column, Integer, String

class Response(Base):
    __tablename__='response'
    id  = Column(Integer, primary_key=True,index=True)
    intent = Column(String(50),unique=True)
    reply = Column(String(100),unique=True)
    
