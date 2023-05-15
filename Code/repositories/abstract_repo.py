from typing import TypeVar, Generic
from abc import ABCMeta, abstractmethod

T = TypeVar('T')


class AbstractRepository(Generic[T]):
    __metaclass__ = ABCMeta

    def __init__(self, session):
        self.session = session

    @abstractmethod
    def add(self, item: T) -> None:
        self.session.add(item)
        self.session.commit()

    @abstractmethod
    def add_all(self, items: list[T]) -> None:
        self.session.add_all(items)
        self.session.commit()

    @abstractmethod
    def edit(self, item: T) -> None:
        self.session.merge(item)
        self.session.commit()

    @abstractmethod
    def delete_by_id(self, item_id: int) -> None:
        server_to_delete = self.session.query(T) \
            .get(item_id)
        self.session.delete(server_to_delete)
        self.session.commit()

    @abstractmethod
    def delete(self, item: T) -> None:
        self.session.delete(item)
        self.session.commit()

    @abstractmethod
    def get_all(self) -> list[T]:
        return self.session.query(T).all()

    @abstractmethod
    def get_by_id(self, item_id: int) -> T:
        return self.session.query(T).get(item_id)

    @abstractmethod
    def get_many_by_ids(self, object_ids: list) -> list[T]:
        return self.session.query(T) \
            .filter(T.id.in_(object_ids)) \
            .all()
