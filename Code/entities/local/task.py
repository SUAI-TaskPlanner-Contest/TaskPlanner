from utils.base import Base
from entities.local.server import Server
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Task(Base):

    __tablename__ = "task"
    
    # keys
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.server_id', ondelete='CASCADE'))
    parent_id = Column(Integer, ForeignKey("task.task_id", ondelete='CASCADE'))
    
    # M:1
    server = relationship("Server", back_populates="tasks")
    
    # 1:1
    label = relationship("Label", back_populates="task")

    # 1:M
    children = relationship("Task", cascade="all", backref=backref("parent", remote_side="Task.task_id"))

    # other fields
    # caldav fields
    dtstamp = Column(DateTime)
    dtstart = Column(DateTime)
    due = Column(DateTime)
    last_mod = Column(DateTime)

    summary = Column(String)
    description = Column(String)

    # own fields
    tech_status = Column(Integer)

    def __init__(self, server: Server, dtstamp: datetime, dtstart: datetime, due: datetime, 
                 last_mod: datetime, summary: str, description: str, 
                 tech_status: int, parent=None):
        self.dtstamp = dtstamp
        self.dtstart = dtstart
        self.due = due
        self.last_mod = last_mod
        self.summary = summary
        self.description = description
        self.tech_status = tech_status
        self.server = server
        self.parent = parent