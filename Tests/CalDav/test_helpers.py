from Code.entities.db_entities import Task, Server, Label, Type, Size, Status, Priority
from Code.utils.time_helper import utc_now

current = 0


def generate_id() -> int:
    global current
    current = current + 1
    return current


def __create_type(server: Server, name: str) -> Type:
    label = Type(server, name)
    label.type_id = generate_id()
    return label


def __create_priority(server: Server, name: str) -> Priority:
    label = Priority(server, name)
    label.priority_id = generate_id()
    return label


def __create_size(server: Server, name: str) -> Size:
    label = Size(server, name)
    label.size_id = generate_id()
    return label


def __create_status(server: Server, name: str) -> Status:
    label = Status(server, name)
    label.status_id = generate_id()
    return label


def generate_labels(server: Server, task: Task) -> Label:
    label = Label(
        task,
        __create_priority(server=server, name="Low"),
        __create_size(server=server, name="Small"),
        __create_type(server=server, name="In progress"),
        __create_status(server=server, name="Needs action")
    )
    label.priority_id = label.priority.priority_id
    label.status_id = label.status.status_id
    label.type_id = label.type.type_id
    label.size_id = label.size.size_id
    label.label_id = generate_id()
    return label


def generate_task(server: Server) -> Task:
    task = Task(
        server=server,
        dtstamp=utc_now(),
        last_mod=utc_now(),
        dtstart=utc_now(),
        due=utc_now(),
        summary='I am a test task',
        description='My life purpose is a caldav service testing :(',
        tech_status=0,
        parent=None
    )
    task.label = generate_labels(server, task)
    task.id = generate_id()
    task.sync_time = utc_now()
    return task
