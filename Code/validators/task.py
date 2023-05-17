from . import *
from Code.entities.db_entities import Server, Task

class TaskValidate(BaseModel):
    server: Server
    parent: Task = None
    dtstamp: datetime
    dtstart: datetime
    due: datetime
    last_mod: datetime
    tech_status: StrictInt
    summary: StrictStr
    description: StrictStr

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @validator('summary')
    def str_check(cls, summary: str):
        assert len(summary) > 0, "Вы не ввели название задачи"
        return summary
