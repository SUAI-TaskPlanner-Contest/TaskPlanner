from . import *

class TaskService():

    def __init__(self, repo, pincode):
        self.repo = repo
        self.pincode = pincode

    @staticmethod
    def is_int(item_id: int) -> bool:
        return True if isinstance(item_id, int) else False

    @staticmethod
    def create_copy(item):
        return deepcopy(item)

    @staticmethod
    def convert_time_to_local(item: Task):
        item = TaskService.create_copy(item)
        item.dtstamp = utc0_to_local(item.dtstamp)
        item.dtstart = utc0_to_local(item.dtstart)
        item.due = utc0_to_local(item.due)
        item.last_mod = utc0_to_local(item.last_mod)
        return item

    @staticmethod
    def convert_time_to_utc(item: Task):
        item = TaskService.create_copy(item)
        item.dtstamp = local_to_utc0(item.dtstamp)
        item.dtstart = local_to_utc0(item.dtstart)
        item.due = local_to_utc0(item.due)
        item.last_mod = local_to_utc0(item.last_mod)
        return item

    @staticmethod
    def encrypt_data(item, pincode) -> Server:
        item = TaskService.create_copy(item)
        item.user_email = encrypt(item.user_email, pincode)
        item.user_password = encrypt(item.user_password, pincode)
        return item

    def is_none(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if item is None:
            raise Invalid('Объект не найден')

    def add(self, item: Task) -> None:
        TaskValidate.from_orm(item)
        self.add_label(item)
        item.server = TaskService.encrypt_data(item.server, self.pincode)
        item = TaskService.convert_time_to_utc(item)
        self.repo.add(item)

    def add_all(self, items: list[Task]) -> None:
        if not isinstance(items, list):
            raise Invalid(f"Невозможно добавить задачи")
        _ = [TaskValidate.from_orm(item) for item in items]
        new_items = []
        for item in items:
            self.add_label(item)
            item.server = TaskService.encrypt_data(item.server, self.pincode)
            item = TaskService.convert_time_to_utc(item)
            new_items.append(item)
        self.repo.add_all(new_items)

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
        items = self.repo.get_all()
        items_local = []
        for item in items:
            items_local.append(TaskService.convert_time_to_local(item))
        return items_local

    def get_by_id(self, item_id: int) -> Task:
        if not TaskService.is_int(item_id):
            raise Invalid(f"Невозможно открыть задачу")
        self.is_none(item_id)
        item = self.repo.get_by_id(item_id)
        item = TaskService.convert_time_to_local(item)
        return item

    def get_many_by_ids(self, objects_ids: list[int]) -> list[Task]:
        if not isinstance(objects_ids, list):
            raise Invalid(f"Невозможно открыть задачи")
        check_ids = [TaskService.is_int(obj_id) for obj_id in objects_ids]
        if False in check_ids:
            raise Invalid(f"Невозможно открыть задачи")
        items = self.repo.get_many_by_ids(objects_ids)
        items_local = []
        for item in items:
            items_local.append(TaskService.convert_time_to_local(item))
        return items_local

    def get_all_by_server_id(self, server_id: int) -> list[Task]:
        if not TaskService.is_int(server_id):
            raise Invalid(f"Невозможно открыть задачи")
        items = self.repo.get_all_by_server_id(server_id)
        items_local = []
        for item in items:
            items_local.append(TaskService.convert_time_to_local(item))
        return items_local

    def get_children_by_parent_id(self, parent_id: int) -> list[Task]:
        if not TaskService.is_int(parent_id):
            raise Invalid(f"Невозможно открыть задачи")
        items = self.repo.get_children_by_parent_id(parent_id)
        items_local = []
        for item in items:
            items_local.append(TaskService.convert_time_to_local(item))
        return items_local

    def get_task_children_by_id(self, task_id: int) -> list[Task]:
        if not TaskService.is_int(task_id):
            raise Invalid(f"Невозможно открыть задачи")
        self.is_none(task_id)
        items = self.repo.get_task_children_by_id(task_id)
        items_local = []
        for item in items:
            items_local.append(TaskService.convert_time_to_local(item))
        return items_local

    def add_label(self, task: Task):
        task.label = Label(task=task)