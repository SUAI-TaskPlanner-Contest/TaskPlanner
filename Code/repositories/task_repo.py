from Code.entities.db_entities import Task
from Code.repositories.abstract_repo import AbstractRepository, T


class TaskRepository(AbstractRepository[T]):

    def __init__(self, session):
        super(TaskRepository, self).__init__(session)

    def get_all_by_server_id(self, server_id) -> list[Task]:
        return self.session.query(Task)\
            .filter(Task.server_id == server_id)\
            .all()

    def get_children(self, task_id: int) -> list[Task]:
        return self.session.query(Task) \
            .get(task_id) \
            .children
