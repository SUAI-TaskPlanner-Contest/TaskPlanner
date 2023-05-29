from Code.repositories.abstract_repo import AbstractRepository, T
from Code.entities.db_entities import Task, Server, Status, Size, Type, Priority


class ServerRepository(AbstractRepository[T]):

    def __init__(self, session):
        super(ServerRepository, self).__init__(session)

    def delete_by_id(self, server_id: int) -> None:
        server_to_delete = self.session.query(Server) \
            .filter(Server.id == server_id)\
            .first()
        self.session.delete(server_to_delete)
        self.session.commit()

    def get_all(self) -> list[Server]:
        return self.session.query(Server)\
            .all()

    def get_by_id(self, server_id: int) -> Server:
        return self.session.query(Server)\
            .get(server_id)

    def get_many_by_ids(self, server_ids: list) -> list[T]:
        return self.session.query(Server) \
            .filter(Server.id.in_(server_ids)) \
            .all()

    def get_count(self, user_email: str) -> int:
        return self.session.query(Server) \
            .filter(Server.user_email == user_email) \
            .count()

    def get_tasks(self, server_id: int) -> list[Task]:
        return self.session.query(Server) \
            .get(server_id) \
            .tasks

    def get_statuses(self, server_id) -> list[Status]:
        return self.session.query(Server). \
            get(server_id)\
            .statuses

    def get_sizes(self, server_id) -> list[Size]:
        return self.session.query(Server). \
            get(server_id)\
            .sizes

    def get_priorities(self, server_id) -> list[Priority]:
        return self.session.query(Server). \
            get(server_id)\
            .priorities

    def get_types(self, server_id) -> list[Type]:
        return self.session.query(Server). \
            get(server_id)\
            .types
