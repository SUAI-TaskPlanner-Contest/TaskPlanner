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
    def email_format_check(cls, email: str):
        reg = r"[^@]+@[\w]+[.][\w]+"
        assert len(re.findall(reg, email)) > 0, "Вы ввели email неправильного формата"
        return email

    @validator('server_name')
    def name_check(cls, server_name: str):
        assert len(server_name) > 0, "Вы не ввели имя сервера"
        return server_name

    @validator('calendar_name')
    def name_check(cls, calendar_name: str):
        assert len(calendar_name) > 0, "Вы не ввели имя календаря"
        return calendar_name

    @validator('user_password')
    def password_check(cls, password: str):
        assert len(password) > 0, 'Вы не ввели пароль'
        return password