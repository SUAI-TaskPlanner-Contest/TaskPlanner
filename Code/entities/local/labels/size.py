from utils.base import Base
from entities.local.server import Server
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class Size(Base):
    __tablename__ = 'size'

    size_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.server_id', ondelete='CASCADE'))
    name = Column(String)

    server = relationship("Server", back_populates="sizes")

    # 1:M
    labels = relationship("Label", back_populates="size")

    def __init__(self, server: Server, name: str):
        self.server = server
        self.name = name