from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Server(Base):
    __tablename__ = 'server'

    # primary key
    id = Column("server_id", Integer, primary_key=True, autoincrement=True)

    # other fields
    user_email = Column(String)
    user_password = Column(String)

    server_uri = Column(String)
    server_name = Column(String)
    calendar_name = Column(String)

    # 1:M
    tasks = relationship("Task", cascade="all,delete", back_populates="server")
    priorities = relationship("Priority", cascade="all,delete", back_populates="server")
    sizes = relationship("Size", cascade="all,delete", back_populates="server")
    types = relationship("Type", cascade="all,delete", back_populates="server")
    statuses = relationship("Status", cascade="all,delete", back_populates="server")

    def __init__(self, user_email: str, user_password: str,
                 server_name: str, calendar_name: str, server_uri: str):
        self.user_email = user_email
        self.user_password = user_password
        self.server_name = server_name
        self.calendar_name = calendar_name
        self.server_uri = server_uri


class Task(Base):
    __tablename__ = "task"

    # keys
    id = Column("task_id", Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.server_id', ondelete='CASCADE'))
    parent_id = Column(Integer, ForeignKey("task.task_id", ondelete='CASCADE'))

    # M:1
    server = relationship("Server", back_populates="tasks")

    # 1:1
    label = relationship("Label", cascade="all,delete", uselist=False, back_populates="task")

    # 1:M
    children = relationship("Task", cascade="all", backref=backref("parent", remote_side="Task.id"))

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

    def __init__(self, server: Server, summary: str, description: str,
                 dtstamp: datetime, dtstart: datetime, due: datetime,
                 last_mod: datetime, tech_status: int, parent=None):
        self.dtstamp = dtstamp
        self.dtstart = dtstart
        self.due = due
        self.last_mod = last_mod
        self.summary = summary
        self.description = description
        self.tech_status = tech_status
        self.server = server
        self.parent = parent


class Label(Base):
    __tablename__ = 'label'

    id = Column("label_id", Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('task.task_id', ondelete='CASCADE'))
    priority_id = Column(Integer, ForeignKey('priority.priority_id'))
    size_id = Column(Integer, ForeignKey('size.size_id'))
    type_id = Column(Integer, ForeignKey('type.type_id'))
    status_id = Column(Integer, ForeignKey('status.status_id'))

    task = relationship("Task", back_populates="label")
    priority = relationship("Priority", back_populates="labels")
    size = relationship("Size", back_populates="labels")
    type = relationship("Type", back_populates="labels")
    status = relationship("Status", back_populates="labels")

    def __init__(self, task, priority=None, size=None, type=None, status=None):
        self.task = task
        self.priority = priority
        self.size = size
        self.type = type
        self.status = status


class Priority(Base):
    __tablename__ = 'priority'

    id = Column("priority_id", Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.server_id', ondelete='CASCADE'))
    name = Column(String)

    # M:1
    server = relationship("Server", back_populates="priorities")

    # 1:M
    labels = relationship("Label", back_populates="priority")

    def __init__(self, server: Server, name: str):
        self.server = server
        self.name = name


class Size(Base):
    __tablename__ = 'size'

    id = Column("size_id", Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.server_id', ondelete='CASCADE'))
    name = Column(String)

    server = relationship("Server", back_populates="sizes")

    # 1:M
    labels = relationship("Label", back_populates="size")

    def __init__(self, server: Server, name: str):
        self.server = server
        self.name = name


class Status(Base):
    __tablename__ = 'status'

    id = Column("status_id", Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.server_id', ondelete='CASCADE'))
    name = Column(String)

    server = relationship("Server", back_populates="statuses")

    # 1:M
    labels = relationship("Label", back_populates="status")

    def __init__(self, server, name: str):
        self.server = server
        self.name = name


class Type(Base):
    __tablename__ = 'type'

    id = Column("type_id", Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.server_id', ondelete='CASCADE'))
    name = Column(String)

    # M:1
    server = relationship("Server", back_populates="types")

    # 1:M
    labels = relationship("Label", back_populates="type")

    def __init__(self, server: Server, name: str):
        self.server = server
        self.name = name


engine = create_engine('sqlite:///test.db', echo=False)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
