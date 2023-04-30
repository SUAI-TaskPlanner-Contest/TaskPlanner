from . import *

class ServerValidate(BaseModel):
    email: StrictStr
    password: StrictStr
    name: StrictStr
    uri: StrictStr

    class Config:
        orm_mode = True

    @validator('email')
    def email_format_check(cls, email):
        reg = r"[^@]+@[\w]+[.][\w]+"
        assert len(re.findall(reg, email)) > 0, 'email неправильного формата'
        return email

    @validator('name')
    def name_check(cls, name):
        assert len(name) > 0, 'Вы не ввели имя сервера'
        return

    @validator('password')
    def password_check(cls, password):
        assert len(password) > 0, 'Вы не ввели пароль'
        return password