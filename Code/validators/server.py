from . import *

class ServerValidate(BaseModel):
    user_email: StrictStr
    user_password: StrictStr
    server_name: StrictStr
    calendar_name: StrictStr
    server_uri: StrictStr

    class Config:
        orm_mode = True

    @validator('user_email')
    def email_format_check(cls, email):
        reg = r"[^@]+@[\w]+[.][\w]+"
        assert len(re.findall(reg, email)) > 0, 'email неправильного формата'
        return email

    @validator('server_name')
    def name_check(cls, name):
        assert len(name) > 0, 'Вы не ввели имя сервера'
        return

    @validator('calendar_name')
    def name_check(cls, name):
        assert len(name) > 0, 'Вы не ввели имя календаря'
        return

    @validator('user_password')
    def password_check(cls, password):
        assert len(password) > 0, 'Вы не ввели пароль'
        return password