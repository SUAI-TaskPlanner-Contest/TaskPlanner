from . import *

class ServerValidate(BaseModel):
    user_email: StrictStr
    user_password: StrictStr
    server_name: StrictStr
    calendar_name: StrictStr
    server_uri: StrictStr

    class Config:
        orm_mode = True

    # @validator('user_email')
    # def email_format_check(cls, email: str):
    #     validate_email(
    #         email,
    #         check_deliverability=False
    #     )
    #     return email

    @validator('user_email')
    def email_format_check(cls, email: str):
        assert len(email) > 0, "Вы не ввели имя сервера"
        return email

    @validator('server_name')
    def server_name_check(cls, server_name: str):
        assert len(server_name) > 0, "Вы не ввели имя сервера"
        return server_name

    @validator('calendar_name')
    def calendar_name_check(cls, calendar_name: str):
        assert len(calendar_name) > 0, "Вы не ввели имя календаря"
        return calendar_name

    @validator('user_password')
    def password_check(cls, password: str):
        assert len(password) > 0, 'Вы не ввели пароль'
        return password

    @validator('server_uri')
    def server_uri_check(cls, server_uri: str):
        assert urlparse(server_uri).netloc, 'Вы ввели некорректный uri-адрес сервера'
        return server_uri