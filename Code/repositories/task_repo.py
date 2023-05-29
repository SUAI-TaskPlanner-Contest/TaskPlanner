from Code.entities.db_entities import Task
from Code.repositories.abstract_repo import AbstractRepository, T


class TaskRepository(AbstractRepository[T]):

    def __init__(self, session):
        super(TaskRepository, self).__init__(session)

    def delete_by_id(self, task_id: int) -> None:
        task_to_delete = self.session.query(Task) \
            .filter(Task.id == task_id)\
            .first()
        self.session.delete(task_to_delete)
        self.session.commit()

    def get_all(self) -> list[Task]:
        return self.session.query(Task)\
            .all()

    def get_by_id(self, task_id: int) -> Task:
        return self.session.query(Task)\
            .get(task_id)

    def get_many_by_ids(self, task_ids: list) -> list[T]:
        return self.session.query(Task) \
            .filter(Task.id.in_(task_ids)) \
            .all()

    def get_all_by_server_id(self, server_id) -> list[Task]:
        return self.session.query(Task)\
            .filter(Task.server_id == server_id)\
            .all()

    def get_children_by_parent_id(self, parent_id: int) -> list[Task]:
        return self.session.query(Task) \
            .filter(Task.parent_id == parent_id) \
            .all()

    def get_task_children_by_id(self, task_id: int) -> list[Task]:
        return self.session.query(Task) \
            .get(task_id) \
            .children
