from datetime import date
from datetime import datetime
from datetime import timedelta
import caldav

## Данные о календаре и пользователе: URL календаря, имя пользователя и пароль

caldav_url = ""  # ссылка на календарь
username = ""  # имя пользователя, для некоторых календарей почта
password = ""  # пароль пользователя

def run_examples():
    """
    Все примеры запускаются один за другим
    """
    ## Запрос к ресурсу
    ## Client хранит в себе: информация о сеансе http, имя пользователя, пароль и т.д.
    with caldav.DAVClient(
        url=caldav_url, username=username, password=password
    ) as client:

        ## Первый шаг для связи с сервером.
        ## Это вызовет связь с сервером.
        my_principal = client.principal()

        ## Календари участника можно получить следующим образом:
        calendars = my_principal.calendars()

        ## Вывод информации о календаре:
        print_calendars_demo(calendars)

        ## Удаление тестового календаря.
        ## Для этого метода нужна общая информация о календаре, хранящаяся в данном примере
        ## в my_principal, также нужно название календаря.
        find_delete_calendar_demo(my_principal, "Test calendar from caldav examples")

        ## Создание нового календаря.
        ## Может вызвать ошибку по нескольким причинам:
        ## * сервер может не поддерживать это;
        ## * у участника может не быть разрешения на создание календарей;
        ## * некоторые облачные провайдеры имеют глобальное пространство имен.
        my_new_calendar = my_principal.make_calendar( name="Test calendar from caldav examples")

        ## Доступ к календарю через URL.
        ## В примере выше создаётся новый календарь, чтобы получить к нему доступ можно воспользоваться этим методом.
        ## В теории этот метод обходит метод principal, на практике не проверялся (пока).
        calendar_by_url_demo(client, my_new_calendar.url)

        ## Удаление ивентов, задач или календарей
        ## Очевидно, ивент или задача удаляется вместе с календарём
        my_new_calendar.delete()


def calendar_by_url_demo(client, url):
    """Если у нас есть URL-адрес календаря, то можно не извлекать principal
    объект с сервера, иначе говоря, обойти его. Тем не менее, нельзя обойтись без
    инициализации объекта client.
    """
    ## Можно извлечь календари следующим способом, без повторного запроса к серверу:
    calendar = client.calendar(url=url)


def search_calendar_demo(calendar):
    """
    несколько примеров того, как извлекать объекты из календаря
    """
    ## поиск может осуществляться по другим параметрам, например по ключевому слову
    ## (см. файл с документацией CalDav).
    tasks_fetched = calendar.search(todo=True, category="outdoor")
    assert len(tasks_fetched) == 1

    ## Этот метод извлечёт все объекты календаря:
    all_objects = calendar.objects()

    ## Этот метод извлечёт _________ календаря:
    updated_objects = calendar.objects_by_sync_token(some_sync_token)

    ## Этот метод извлечёт __________ календаря:
    some_object = calendar.object_by_uid(some_uid)

    ## Этот метод __________ календаря:
    children = calendar.children()

    ## Этот метод извлечёт все задачи календаря:
    tasks = calendar.todos()

    ## Задачи могут быть выполнены:
    tasks[0].complete()

    ## Затем они исчезнут из списка задач:
    assert not calendar.todos()

    ## Но они не полностью удалены:
    assert len(calendar.todos(include_completed=True)) == 1

    ## Полное удаление задачи:
    tasks[0].delete()

    return tasks_fetched


def print_calendars_demo(calendars):
    """
    В этом примере выводятся имя и URL-адрес для каждого календаря в списке
    """
    if calendars:
        ## Некоторые серверы календарей будут включать в этот список все календари,
        ## к которым у вас есть доступ, а не только календари,
        ## принадлежащие этому участнику.
        print("your principal has %i calendars:" % len(calendars))
        for c in calendars:
            print("    Name: %-36s  URL: %s" % (c.name, c.url))
    else:
        print("your principal has no calendars")


def find_delete_calendar_demo(my_principal, calendar_name):
    """
    В этом примере по известному имени календаря, находится календарь,
    если он существует, после чего удаляется, если он опять же существует.
    """
    ## Попробуем найти или создать календарь...
    try:
        ## Если календаря не существует, будет показана ошибка "Не найдено".
        demo_calendar = my_principal.calendar(name="Test calendar from caldav examples")
        assert demo_calendar
        print(
            f"We found an existing calendar with name {calendar_name}, now deleting it"
        )
        demo_calendar.delete()
    except caldav.error.NotFoundError:
        ## Календарь не был найден.
        pass


def add_stuff_to_calendar_demo(calendar):
    """
    Эта демонстрация добавляет задачу в календарь:
    """

    ## не все календари поддерживают задачи... но если они поддерживаются,
    ## это будет сказано здесь:
    acceptable_component_types = calendar.get_supported_components()
    assert "VTODO" in acceptable_component_types

    ## Добавляет задачу, которая должна содержать несколько ical строк
    dec_task = calendar.save_todo(
        ical_fragment="""DTSTART;VALUE=DATE:20201213 ## Дата начала задачи
DUE;VALUE=DATE:20201220 ## Дата окончания задачи
SUMMARY:Chop down a tree and drag it into the living room  ## Название задачи
RRULE:FREQ=YEARLY  ## Правило повторения.
PRIORITY: 2  ## Приоритет задачи
CATEGORIES: outdoor""" ## Категория задачи
    )
    ## RRULE: может повторяться каждый день, каждые 5 дней, каждые 8 месяцев и т.д.
    ## Доп. инфо по поводу RRULE: https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html