from . import *
from entities import Server

class CategoryValidator(BaseModel):
    server: Server
    name: StrictStr

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @validator('name')
    def name_check(cls, name):
        assert len(name) > 0, 'Вы не ввели имя'
        return name