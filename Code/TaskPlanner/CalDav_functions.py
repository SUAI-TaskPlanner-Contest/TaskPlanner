from datetime import date
from datetime import datetime
from datetime import timedelta
import caldav

## Данные о календаре и пользователе: URL календаря (взят в настройках GOOGLE календаря), имя пользователя и пароль

caldav_url = ""  # ссылка на календарь
username = ""  # имя пользователя, для некоторых календарей почта
password = ""  # пароль пользователя

def run_examples():
    """
    Все примеры запускаются один за другим
    """
    ## Запрос к ресурсу
    ## Client хранит в себе: http session information, username, password, etc.
    with caldav.DAVClient(
        url=caldav_url, username=username, password=password
    ) as client:

        ## Первый шаг для связи с сервером.
        ## This will cause communication with the server.
        my_principal = client.principal()

        ## The principals calendars can be fetched like this:
        calendars = my_principal.calendars()

        ## Вывод информации о календаре
        print_calendars_demo(calendars)

        ## Удаление тестового календаря
        find_delete_calendar_demo(my_principal, "Test calendar from caldav examples")

        ## Создание нового календаря
        ## Может вызвать ошибку по нескольким причинам:
        ## * server may not support it (it's not mandatory in the CalDAV RFC)
        ## * principal may not have the permission to create calendars
        ## * some cloud providers have a global namespace
        my_new_calendar = my_principal.make_calendar(
            name="Test calendar from caldav examples"
        )

        ## Доступ к календарю через URL
        calendar_by_url_demo(client, my_new_calendar.url)

        ## Удаление ивентов или календарей
        ## Очевидно, ивент удаляется вместе с календарём
        my_new_calendar.delete()


def calendar_by_url_demo(client, url):
    """Sometimes one may have a calendar URL.  Sometimes maybe one would
    not want to fetch the principal object from the server (it's not
    even required to support it by the caldav protocol).
    """
    ## No network traffic will be initiated by this:
    calendar = client.calendar(url=url)


def search_calendar_demo(calendar):
    """
    some examples on how to fetch objects from the calendar
    """
    ## search can be done by other things, i.e. keyword
    tasks_fetched = calendar.search(todo=True, category="outdoor")
    assert len(tasks_fetched) == 1

    ## This those should also work:
    all_objects = calendar.objects()
    # updated_objects = calendar.objects_by_sync_token(some_sync_token)
    # some_object = calendar.object_by_uid(some_uid)
    # some_event = calendar.event_by_uid(some_uid)
    children = calendar.children()
    events = calendar.events()
    tasks = calendar.todos()
    assert len(events) + len(tasks) == len(all_objects)
    assert len(children) == len(all_objects)
    ## TODO: Some of those should probably be deprecated.
    ## children is a good candidate.

    ## Tasks can be completed
    tasks[0].complete()

    ## They will then disappear from the task list
    assert not calendar.todos()

    ## But they are not deleted
    assert len(calendar.todos(include_completed=True)) == 1

    ## Let's delete it completely
    tasks[0].delete()

    return events_fetched[0]


def print_calendars_demo(calendars):
    """
    This example prints the name and URL for every calendar on the list
    """
    if calendars:
        ## Some calendar servers will include all calendars you have
        ## access to in this list, and not only the calendars owned by
        ## this principal.
        print("your principal has %i calendars:" % len(calendars))
        for c in calendars:
            print("    Name: %-36s  URL: %s" % (c.name, c.url))
    else:
        print("your principal has no calendars")


def find_delete_calendar_demo(my_principal, calendar_name):
    """
    This example takes a calendar name, finds the calendar if it
    exists, and deletes the calendar if it exists.
    """
    ## Let's try to find or create a calendar ...
    try:
        ## This will raise a NotFoundError if calendar does not exist
        demo_calendar = my_principal.calendar(name="Test calendar from caldav examples")
        assert demo_calendar
        print(
            f"We found an existing calendar with name {calendar_name}, now deleting it"
        )
        demo_calendar.delete()
    except caldav.error.NotFoundError:
        ## Calendar was not found
        pass


def add_stuff_to_calendar_demo(calendar):
    """
    This demo adds some stuff to the calendar
    Unfortunately the arguments that it's possible to pass to save_* is poorly documented.
    https://github.com/python-caldav/caldav/issues/253
    """

    ## not all calendars supports tasks ... but if it's supported, it should be
    ## told here:
    acceptable_component_types = calendar.get_supported_components()
    assert "VTODO" in acceptable_component_types

    ## Add a task that should contain some ical lines
    ## Note that this may break on your server:
    ## * not all servers accepts tasks and events mixed on the same calendar.
    ## * not all servers accepts tasks at all
    dec_task = calendar.save_todo(
        ical_fragment="""DTSTART;VALUE=DATE:20201213
DUE;VALUE=DATE:20201220
SUMMARY:Chop down a tree and drag it into the living room
RRULE:FREQ=YEARLY
PRIORITY: 2
CATEGORIES: outdoor"""
    )

    ## ical_fragment parameter -> just some lines
    ## ical parameter -> full ical object

