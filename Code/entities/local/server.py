from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.base import Base


class Server(Base):
    __tablename__ = 'server'

    # primary key
    server_id = Column(Integer, primary_key=True, autoincrement=True)

    # other fields
    email = Column(String)
    name = Column(String)
    password = Column(String)
    uri = Column(String)

    # 1:M
    tasks = relationship("Task", cascade="all,delete", back_populates="server")
    priorities = relationship("Priority", cascade="all,delete", back_populates="server")
    sizes = relationship("Size", cascade="all,delete", back_populates="server")
    types = relationship("Type", cascade="all,delete", back_populates="server")
    statuses = relationship("Status", cascade="all,delete", back_populates="server")

    def __init__(self, email, name, password, uri):
        self.email = email
        self.name = name
        self.password = password
        self.uri = uri
