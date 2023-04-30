from . import *
from entities.server import Server

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
    def str_check(cls, var):
        assert len(var) > 0, 'Вы не ввели название задачи'
        return var