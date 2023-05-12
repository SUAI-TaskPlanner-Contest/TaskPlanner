Для валидации используется библиотека pydantic. Сначала создадим необходимые сущности

    server = Server(server_name="23", user_email="example@mail.ru", user_password='32e2',
                calendar_name="toxic", server_uri="csd")
    size = Size(server=server, name='test1')
    type = Type(server=server, name='test1')
    priority = Priority(server=server, name='test1')
    status = Status(server=server, name='test1')
    task = Task(server=server, dtstamp=datetime.now(), dtstart=datetime.now(),
                due=datetime.now(), last_mod=datetime.now(), summary='fsef',
                description='fsef', tech_status=5)
    label = Label(task=task, size=3, priority=priority, type=type, status=status)

В исходном примере все сущности имеют правильные типы данных для соответсвующих атрибутов. Применение метода from_orm подтвердит это - он ничего не вернет. Валидатор `CategoryValidator` является общим для сущностей `Type, Priority, Status, Size` 

    ServerValidate.from_orm(server)
    TaskValidate.from_orm(task)
    LabelValidate.from_orm(label)
    CategoryValidator.from_orm(status)

Сделаем некоторые атрибуты неправильными 
#### Неверный формат почты (пользовательский валидатор)

    server = Server(server_name="23", user_email="example@.ru", user_password='32e2', calendar_name="toxic", server_uri="csd")
    ServerValidate.from_orm(server)

Исключение

    raise validation_error
    pydantic.error_wrappers.ValidationError: 1 validation error for ServerValidate
    email
      email неправильного формата (type=assertion_error)

#### Неверный тип данных (без ошибок маппинга)

    server = Server(server_name=["23"], user_email="example@mail.ru", user_password='32e2', calendar_name="toxic", server_uri="csd")
    ServerValidate.from_orm(server)
Исключение

    raise validation_error
    pydantic.error_wrappers.ValidationError: 1 validation error for ServerValidate
    name
      str type expected (type=type_error.str)

#### Ввод пустой строки

    server = Server(server_name="", user_email="example@mail.ru", user_password='32e2', calendar_name="toxic", server_uri="csd")
    ServerValidate.from_orm(server)
Исключение
    
    raise validation_error
    pydantic.error_wrappers.ValidationError: 1 validation error for ServerValidate
    name
      Вы не ввели имя сервера (type=assertion_error)