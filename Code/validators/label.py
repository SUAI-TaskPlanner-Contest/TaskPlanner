from . import *
from entities import Task, Priority, Status, Size, Type

class LabelValidate(BaseModel):
    task: Task
    priority: Priority = None
    status: Status = None
    size: Size = None
    type: Type = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True