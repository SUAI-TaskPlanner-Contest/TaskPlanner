from Code.entities.db_entities import Task, Server, Status, Size, Type, Priority
from Code.repositories.abstract_repo import AbstractRepository, T


class ServerRepository(AbstractRepository[T]):

    def __init__(self, session):
        super(ServerRepository, self).__init__(session)

    def get_count(self, email: str) -> int:
        return self.session.query(Server) \
            .filter(Server.email == email) \
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
