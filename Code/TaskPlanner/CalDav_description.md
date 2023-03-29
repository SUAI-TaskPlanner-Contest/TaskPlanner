## Базовые принципы работы с CalDav

1. Всегда нужно начинать с инициирования объекта *caldav.DAVClient*, этот объект содержит данные аутентификации для сервера.
2. Из объекта *client* можно получить доступ к объекту *caldav.Principal*, представляющий вошедшего в систему участника.
3. Из объекта *principal* можно извлекать / генерировать *caldav.Calendar* объекты.
4. Из объекта *calendar* можно извлекать / генерировать *caldav.Event* объекты и *caldav.Todo* объекты (а также *caldav.Journal* объекты). В конечном счете библиотека также может извлекать объекты базового класса (*caldav.objects.CalendarObjectResource*).

## Основные функции CalDav для работы с календарём

Настройка клиентского объекта *caldav* и *principal* объекта:
```bash
with caldav.DAVClient(url=url, username=username, password=password) as client:
    my_principal = client.principal()
    ...
```
Извлечение календарей:
```bash
calendars = my_principal.calendars()
```
Создание календаря:
```bash
my_new_calendar = my_principal.make_calendar(name="Test calendar")
```
Добавление события в календарь:
```bash
my_event = my_new_calendar.save_event(
    dtstart=datetime.datetime(2023,3,30,15),
    dtend=datetime.datetime(2023,3,30,18),
    summary="Meeting",
    rrule={'FREQ': 'YEARLY'))
```
Поиск по дате в календаре:
```bash
events_fetched = my_new_calendar.search(
    start=datetime(2023, 1, 1), end=datetime(2024, 1, 1),event=True, expand=True)
```
Изменение события:
```bash
event.vobject_instance.vevent.summary.value = "День Победы!" 
event.save()
```
Можно извлечь календарь с известным URL-адресом, не проходя через *principal*:
```bash
the_same_calendar = client.calendar(url=my_new_calendar.url)
```
Извлечение всех событий из календаря:
```bash
all_events = the_same_calendar.events()
```
Удаление календаря (или, в принципе, любого объекта):
```bash
my_new_calendar.delete()
```
Создание списка задач:
```bash
my_new_tasklist = my_principal.make_calendar(
            name="Test tasklist", supported_calendar_component_set=['VTODO'])
```
Добавление задачи в список задач:
```bash
my_new_tasklist.save_todo(
    ics = "RRULE:FREQ=YEARLY",
    summary="Поход по магазинам",
    dtstart=date(2023, 4, 1),
    due=date(2023,4,2),
    categories=['family', 'finance'],
    status='NEEDS-ACTION')
```
Извлечение задач:
```bash
todos = my_new_tasklist.todos()
```
Поиск по задачам:
```bash
todos = my_new_calendar.search(
    start=datetime(2023, 1, 1), end=datetime(2024, 1, 1),
    compfilter='VTODO',event=True, expand=True)
```
Отметка о выполнении задачи:
```bash
todos[0].complete()
```