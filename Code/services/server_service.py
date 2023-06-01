from . import *

class ServerService():

    def __init__(self, repo):
        self.repo = repo

    @staticmethod
    def is_int(item_id: int) -> bool:
        return True if isinstance(item_id, int) else False

    def is_none(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if item is None:
            raise Invalid('Сервер не найден')

    def add(self, item: Server) -> None:
        ServerValidate.from_orm(item)
        self.repo.add(item)

    def add_all(self, items: list[Server]) -> None:
        if not isinstance(items, list):
            raise Invalid(f"Невозможно добавить серверы")
        _ = [ServerValidate.from_orm(item) for item in items]
        self.repo.add_all(items)

    def edit(self, item: Server) -> None:
        ServerValidate.from_orm(item)
        self.repo.edit(item)

    def delete(self, item: Server) -> None:
        ServerValidate.from_orm(item)
        self.repo.delete(item)

    def delete_by_id(self, item_id: int) -> None:
        if not ServerService.is_int(item_id):
            raise Invalid(f"Невозможно удалить сервер")
        self.repo.delete_by_id(item_id)

    def get_all(self) -> list[Server]:
        return self.repo.get_all()

    def get_by_id(self, item_id: int) -> Server:
        if not ServerService.is_int(item_id):
            raise Invalid(f"Невозможно открыть сервер")
        self.is_none(item_id)
        item = self.repo.get_by_id(item_id)
        return item

    def get_many_by_ids(self, objects_ids: list[int]) -> list[Server]:
        if not isinstance(objects_ids, list):
            raise Invalid(f"Невозможно открыть серверы")
        check_ids = [ServerService.is_int(obj_id) for obj_id in objects_ids]
        if False in check_ids:
            raise Invalid(f"Невозможно открыть серверы")
        return self.repo.get_many_by_ids(objects_ids)

    def get_count(self, email: str) -> int:
        if not isinstance(email, str):
            raise Invalid(f"Некорректный email")
        return self.repo.get_count(email)

    def get_tasks(self, server_id: int) -> list[Task]:
        if not ServerService.is_int(server_id):
            raise Invalid(f"Невозможно открыть задачи")
        self.is_none(server_id)
        return self.repo.get_tasks(server_id)

    def get_statuses(self, server_id) -> list[Status]:
        if not ServerService.is_int(server_id):
            raise Invalid(f"Невозможно открыть список статусов")
        self.is_none(server_id)
        return self.repo.get_statuses(server_id)

    def get_sizes(self, server_id) -> list[Size]:
        if not ServerService.is_int(server_id):
            raise Invalid(f"Невозможно открыть список размеров")
        self.is_none(server_id)
        return self.repo.get_sizes(server_id)

    def get_priorities(self, server_id) -> list[Priority]:
        if not ServerService.is_int(server_id):
            raise Invalid(f"Невозможно открыть список приоритетов")
        self.is_none(server_id)
        return self.repo.get_priorities(server_id)

    def get_types(self, server_id) -> list[Type]:
        if not ServerService.is_int(server_id):
            raise Invalid(f"Невозможно открыть список типов")
        self.is_none(server_id)
        return self.repo.get_types(server_id)