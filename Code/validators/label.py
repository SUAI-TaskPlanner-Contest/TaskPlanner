from . import *
from entities import Task, Priority, Status, Size, Type

class LabelValidate(BaseModel):
    task: Task
    priority: Priority
    status: Status
    size: Size
    type: Type

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True