import datetime

from Code.entities.db_entities import Server, Task, Label, Size, Priority, Type, Status
from .time_helper import local_to_utc0
from Code.chipher_module.chipher_module import encrypt

def add_data(session, pincode):
    """
        Add default data to database
    """

    servers = [
        Server(
            user_email=encrypt('local@host.ru', pincode),
            user_password=encrypt('123', pincode),
            server_uri='http://localhost:8000',
            server_name='local server',
            calendar_name='local calendar'
        )
    ]

    sizes = [
        Size(server=servers[0], name="Маленький"),
        Size(server=servers[0], name="Средний"),
        Size(server=servers[0], name="Большой")
    ]

    typies = [
        Type(server=servers[0], name="Разработка"),
        Type(server=servers[0], name="Исследование"),
        Type(server=servers[0], name="Баг"),
        Type(server=servers[0], name="UI")
    ]

    priorities = [
        Priority(server=servers[0], name="Низкий"),
        Priority(server=servers[0], name="Средний"),
        Priority(server=servers[0], name="Высокий")
    ]

    statuses = [
        Status(server=servers[0], name="Нет исполнителя"),
        Status(server=servers[0], name="Нужна помощь"),
        Status(server=servers[0], name="Выполняется"),
        Status(server=servers[0], name="Дополняется")
    ]

    example_task1 = Task(
        server=servers[0],
        dtstamp=local_to_utc0(datetime.datetime.now()),
        dtstart=local_to_utc0(datetime.datetime.now()),
        due=local_to_utc0(datetime.datetime.now() + datetime.timedelta(days=10)),
        last_mod=local_to_utc0(datetime.datetime.now()),
        summary='Пример задачи',
        description='Для создания новых задач нажмите на +',
        tech_status=0
    )
    example_task2 = Task(
        server=servers[0],
        dtstamp=local_to_utc0(datetime.datetime.now()),
        dtstart=local_to_utc0(datetime.datetime.now()),
        due=local_to_utc0(datetime.datetime.now() + datetime.timedelta(days=5)),
        last_mod=local_to_utc0(datetime.datetime.now()),
        summary='Пример задачи',
        description='Для создания новых задач нажмите на +',
        tech_status=0,
        parent=example_task1
    )

    labels = [
        Label(
            task=example_task1,
            priority=priorities[0],
            size=sizes[0],
            type=typies[0],
            status=statuses[0]
        ),
        Label(
            task=example_task2,
            priority=priorities[1],
            size=sizes[1],
            type=typies[1],
            status=statuses[1]
        ),
    ]

    session.add_all(servers)
    session.commit()