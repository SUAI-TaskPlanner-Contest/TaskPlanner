from . import *

class TaskService():

    def __init__(self, repo):
        self.repo = repo

    @staticmethod
    def is_int(item_id: int) -> bool:
        return True if isinstance(item_id, int) else False

    def is_none(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if item is None:
            raise Invalid('Объект не найден')

    def add(self, item: Task) -> None:
        TaskValidate.from_orm(item)
        self.repo.add(item)

    def add_all(self, items: list[Task]) -> None:
        if not isinstance(items, list):
            raise Invalid(f"Невозможно добавить задачи")
        _ = [TaskValidate.from_orm(item) for item in items]
        self.repo.add_all(items)

    def edit(self, item: Task) -> None:
        TaskValidate.from_orm(item)
        self.repo.edit(item)

    def delete(self, item: Task) -> None:
        TaskValidate.from_orm(item)
        self.repo.delete(item)

    def delete_by_id(self, item_id: int) -> None:
        if not TaskService.is_int(item_id):
            raise Invalid(f"Невозможно удалить задачу")
        self.repo.delete_by_id(item_id)

    def get_all(self) -> list[Task]:
        return self.repo.get_all()

    def get_by_id(self, item_id: int) -> Task:
        if not TaskService.is_int(item_id):
            raise Invalid(f"Невозможно открыть задачу")
        self.is_none(item_id)
        item = self.repo.get_by_id(item_id)
        return item

    def get_many_by_ids(self, objects_ids: list[int]) -> list[Task]:
        if not isinstance(objects_ids, list):
            raise Invalid(f"Невозможно открыть задачи")
        check_ids = [TaskService.is_int(obj_id) for obj_id in objects_ids]
        if False in check_ids:
            raise Invalid(f"Невозможно открыть задачи")
        return self.repo.get_many_by_ids(objects_ids)

    def get_all_by_server_id(self, server_id: int) -> list[Task]:
        if not TaskService.is_int(server_id):
            raise Invalid(f"Невозможно открыть задачи")
        return self.repo.get_all_by_server_id(server_id)

    def get_children_by_parent_id(self, parent_id: int) -> list[Task]:
        if not TaskService.is_int(parent_id):
            raise Invalid(f"Невозможно открыть задачи")
        return self.repo.get_children_by_parent_id(parent_id)

    def get_task_children_by_id(self, task_id: int) -> list[Task]:
        if not TaskService.is_int(task_id):
            raise Invalid(f"Невозможно открыть задачи")
        self.is_none(task_id)
        return self.repo.get_task_children_by_id(task_id)