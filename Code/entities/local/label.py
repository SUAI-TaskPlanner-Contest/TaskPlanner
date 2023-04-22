from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from utils.base import Base


class Label(Base):
    __tablename__ = 'label'

    label_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('task.task_id', ondelete='CASCADE'))
    priority_id = Column(Integer, ForeignKey('priority.priority_id'))
    size_id = Column(Integer, ForeignKey('size.size_id'))
    type_id = Column(Integer, ForeignKey('type.type_id'))
    status_id = Column(Integer, ForeignKey('status.status_id'))

    task = relationship("Task", back_populates="label")
    priority = relationship("Priority", back_populates="labels")
    size = relationship("Size", back_populates="labels")
    _type = relationship("Type", back_populates="labels")
    status = relationship("Status", back_populates="labels")

    def __init__(self, task, priority=None, size=None, _type=None, status=None):
        self.task = task
        self.priority = priority
        self.size = size
        self.type = type
        self.status = status
