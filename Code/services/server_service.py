from . import *

class ServerService():

    def __init__(self, repo, pincode):
        self.repo = repo
        self.pincode = pincode

    @staticmethod
    def create_copy(item):
        return deepcopy(item)

    @staticmethod
    def encrypt_data(item, pincode) -> Server:
        item = ServerService.create_copy(item)
        item.user_email=encrypt(item.user_email, pincode)
        item.user_password=encrypt(item.user_password, pincode)
        return item

    @staticmethod
    def decrypt_data(item, pincode) -> Server:
        item = ServerService.create_copy(item)
        item.user_email = decrypt(item.user_email, pincode)
        item.user_password = decrypt(item.user_password, pincode)
        return item

    @staticmethod
    def is_int(item_id: int) -> bool:
        return True if isinstance(item_id, int) else False

    def is_none(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if item is None:
            raise Invalid('Сервер не найден')

    def add(self, item: Server) -> None:
        ServerValidate.from_orm(item)
        self.add_labels(item)
        item = ServerService.encrypt_data(item, self.pincode)
        self.repo.add(item)

    def add_all(self, items: list[Server]) -> None:
        if not isinstance(items, list):
            raise Invalid(f"Невозможно добавить серверы")
        _ = [ServerValidate.from_orm(item) for item in items]
        new_items = []
        for item in items:
            self.add_labels(item)
            new_items.append(ServerService.encrypt_data(item, self.pincode))
        self.repo.add_all(new_items)

    def edit(self, old_item: Server) -> None:
        ServerValidate.from_orm(old_item)
        item = ServerService.encrypt_data(old_item, self.pincode)
        self.repo.edit(item)

    def delete(self, item: Server) -> None:
        ServerValidate.from_orm(item)
        item = ServerService.encrypt_data(item, self.pincode)
        self.repo.delete(item)

    def delete_by_id(self, item_id: int) -> None:
        if not ServerService.is_int(item_id):
            raise Invalid(f"Невозможно удалить сервер")
        self.repo.delete_by_id(item_id)

    def get_all(self) -> list[Server]:
        items = self.repo.get_all()
        return items

    def get_by_id(self, item_id: int) -> Server:
        if not ServerService.is_int(item_id):
            raise Invalid(f"Невозможно открыть сервер")
        self.is_none(item_id)
        item = self.repo.get_by_id(item_id)
        item = ServerService.decrypt_data(item, self.pincode)
        return item

    def get_many_by_ids(self, objects_ids: list[int]) -> list[Server]:
        if not isinstance(objects_ids, list):
            raise Invalid(f"Невозможно открыть серверы")
        check_ids = [ServerService.is_int(obj_id) for obj_id in objects_ids]
        if False in check_ids:
            raise Invalid(f"Невозможно открыть серверы")
        items = self.repo.get_many_by_ids(objects_ids)
        items_decrypt = []
        for item in items:
            items_decrypt.append(ServerService.decrypt_data(item, self.pincode))
        return items_decrypt

    def get_count(self, email: str) -> int:
        if not isinstance(email, str):
            raise Invalid(f"Некорректный email")
        all_items = self.get_all()
        items_encrypt = []
        for item in all_items:
            items_encrypt.append(ServerService.decrypt_data(item, self.pincode))
        servers_count = reduce(
            lambda count, x: count + int(x.user_email == email),
            items_encrypt,
            0
        )
        return servers_count

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

    def add_labels(self, server: Server):
        server.sizes = [
            Size(server=server, name="Маленький"),
            Size(server=server, name="Средний"),
            Size(server=server, name="Большой")
        ]
        server.typies = [
            Type(server=server, name="Разработка"),
            Type(server=server, name="Исследование"),
            Type(server=server, name="Баг"),
            Type(server=server, name="UI")
        ]
        server.statuses = [
            Status(server=server, name="Нет исполнителя"),
            Status(server=server, name="Нужна помощь"),
            Status(server=server, name="Выполняется"),
            Status(server=server, name="Дополняется")
        ]
        server.priorities = [
            Priority(server=server, name="Низкий"),
            Priority(server=server, name="Средний"),
            Priority(server=server, name="Высокий")
        ]