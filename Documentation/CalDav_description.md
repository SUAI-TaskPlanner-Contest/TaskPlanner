# Базовые принципы работы с CalDav

1. Всегда нужно начинать с инициирования объекта *caldav.DAVClient*, этот объект содержит данные аутентификации для сервера.
2. Из объекта *client* можно получить доступ к объекту *caldav.Principal*, представляющий вошедшего в систему участника.
3. Из объекта *principal* можно извлекать / генерировать *caldav.Calendar* объекты.
4. Из объекта *calendar* можно извлекать / генерировать *caldav.Event* объекты и *caldav.Todo* объекты (а также *caldav.Journal* объекты). В конечном счете библиотека также может извлекать объекты базового класса (*caldav.objects.CalendarObjectResource*).

# Основные функции CalDav для работы с календарём

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
Можно извлечь календарь с известным URL-адресом, не проходя через *principal*:
```bash
the_same_calendar = client.calendar(url=my_new_calendar.url)
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

# Описание классов и функций CalDav

## Класс DAV client
```bash
class caldav.davclient.DAVClient(url, proxy=None, username=None, 
password=None, auth=None, timeout=None, 
ssl_verify_cert=True, ssl_cert=None, headers={}, huge_tree=False)
```
Базовый клиент для webdav, использует библиотеку запросов; предоставляет доступ к низкоуровневым операциям с сервером caldav.
### Функции DAV client
```bash
calendar(**kwargs)
```
Возвращает объект calendar.

```bash
close()
```
Закрывает сессию объекта DAVClient.

```bash
delete(url)
```
Отправьте запрос на удаление.

```bash
post(url, body, headers={})
```
Отправляет запрос на публикацию.

```bash
principal(*largs, **kwargs)
```
Этот метод возвращает объект caldav.Principal с методами более высокого уровня для работы с календарями участников.

```bash
propfind(url=None, props=”, depth=0)
```
Отправляет запрос на propfind.

• url: url для корня propfind.

• props = (xml запрос), нужные нам свойства

• depth: максимальная глубина рекурсии

```bash
proppatch(url, body, dummy=None)
```
Отправляет запрос на proppatch.

• url: url for the root of the propfind.

• body: XML propertyupdate запрос

• dummy: compatibility parameter

```bash
put(url, body, headers={})
```
Отправляет запрос на put.

```bash
report(url, query=”, depth=0)
```
Отправляет запрос на report.

• url: url for the root of the propfind.

• query: XML request

• depth: maximum recursion depth

```bash
request(url, method=’GET’, body=”, headers={})
```
Фактически отправляет запрос и выполняет аутентификацию


## Класс DAV response

```bash
class caldav.davclient.DAVResponse(response, davclient=None)
```
Этот класс является ответом на запрос DAV. Он создается из клиентского класса DAV. 
Поскольку мы часто получаем XML-ответы, он пытается разобрать их в self.tree

### Функции DAV response

```bash
expand_simple_props(props=[], multi_value_props=[], xpath=None)
```
Функция find_objects_and_props() остановится на xml-элементе под тегом prop. Этот метод превратит эти реквизиты в текст.

Выполняет find_objects_and_props, если он еще не запущен, затем изменяет и возвращает self.objects

```bash
find_objects_and_props()
```
Check the response from the server, check that it is on an expected format, find hrefs and props from it and check statuses delivered.

The parsed data will be put into self.objects, a dict {href: {proptag: prop_element}}. Further parsing of the prop_element has to be done by the caller.

self.sync_token will be populated if found, self.objects will be populated.

```bash
validate_status(status)
```
status is a string like “HTTP/1.1 404 Not Found”. 200, 207 and 404 are considered good statuses. The SOGo caldav server even returns “201 created” when doing a sync-report, to indicate that a resource was created after the last sync-token. This makes sense to me, but I’ve only seen it from SOGo, and it’s not in accordance with the examples in rfc6578.

## Класс Objects
“Объект DAV” - это все, что мы получаем с сервера caldav или загружаем на сервер caldav, в частности, основные элементы, календари и события календаря.

```bash
class caldav.objects.Calendar(client=None, url=None, 
parent=None, name=None, id=None, props=None, **extra)
```
The Calendar object is used to represent a calendar collection.

### Функции Calendar

```bash
add_todo(ical=None, no_overwrite=False, no_create=False, **ical_data)
```
Add a new task to the calendar, with the given ical.

• ical - ical object (text)

```bash
build_date_search_query(start, end=None, compfilter=’VEVENT’, expand=’maybe’)
```

```bash
build_search_xml_query(comp_class=None, todo=None, ignore_completed1=None, 
ignore_completed2=None, ignore_completed3=None, event=None,
filters=None, expand=None, start=None, end=None, **kwargs)
```
Этот метод создаст поисковый запрос caldav в виде объекта etree.

```bash
freebusy_request(start, end)
```
Выполняет поиск по календарю, но возвращает только информацию о free/busy (занят или нет).

• start = datetime.today().

• end = same as above.

```bash
get_supported_components()
```
Возвращает список типов компонентов, поддерживаемых календарем, в строковом формате (typically [‘VJOURNAL’, ‘VTODO’, ‘VEVENT’])

```bash
objects(sync_token=None, load_objects=False)
```
Этот метод вернет все объекты в календаре, если sync_token не передан или если sync_token неизвестен серверу. Если передан synctoken, известный серверу, он вернет объекты, которые были добавлены, удалены или изменены с момента последней установки токена синхронизации.

Если для параметра load_objects установлено значение True, объекты будут загружены - в противном случае будут возвращены пустые объекты CalendarObjectResource.

```bash
objects_by_sync_token(sync_token=None, load_objects=False)
```
То же, что и objects

```bash
save()
```
Метод сохранения календаря пока используется только для его создания.

```bash
save_todo(ical=None, no_overwrite=False, no_create=False, **ical_data)
```
Добавляет новую задачу в календарь с заданным ical.

• ical - ical object (text)

```bash
save_with_invites(ical, attendees, **attendeeoptions)
```
Отправляет запрос schedule на сервер. Эквивалентно save_event, save_to do и т.д., Но участники будут добавлены в объект ical перед отправкой его на сервер.

```bash
search(xml=None, comp_class=None, todo=None, include_completed=False, 
sort_keys=(), split_expanded=True, **kwargs)
```
Создает XML-запрос, отправляет запрос REPORT на сервер и возвращает найденные объекты, в конечном итоге сортируя их перед доставкой.

Этот метод содержит некоторую специальную логику, гарантирующую, что он может последовательно возвращать список ожидающих выполнения задач в любой серверной реализации. В будущем это может также включать обходные пути и фильтрацию на стороне клиента, чтобы убедиться в согласованности других результатов поиска в разных серверных реализациях.

Параметры:

• xml - use this search query, and ignore other filter parameters

• comp_class - set to event, todo or journal to restrict search to this resource type. Some server implementations require this to be set.

• todo - sets comp_class to Todo, and restricts search to pending tasks, unless the next parameter is set . . .

• include_completed - include completed tasks

• event - sets comp_class to event

• text attribute search parameters: category, uid, summary, omment, description, location, status

• no-category, no-summary, etc . . . search for objects that does not have those attributes.

• expand - do server side expanding of recurring events/tasks

• start, end: do a time range search

• filters - other kind of filters (in lxml tree format)

• sort_keys - list of attributes to use when sorting

```bash
todos(sort_keys=(’due’, ’priority’), include_completed=False)
```
Извлекает список событий todo

• sort_keys: use this field in the VTODO for sorting (iterable of lower case string, i.e. (‘priority’,’due’)).

• include_completed: boolean - by default, only pending tasks are listed


## Класс Calendar Object Resource

```bash
class caldav.objects.CalendarObjectResource(client=None, url=None, 
data=None, parent=None, id=None, props=None)
```
Ref RFC 4791, section 4.1, a “Calendar Object Resource” can be an event, a todo-item, a journal entry, or a
free/busy entry

### Функции Calendar Object Resource

```bash
add_attendee(attendee, no_default_parameters=False, **parameters)
```
Для текущего (события/задачи/журнала) добавляет участника.

Участником может быть любой из следующих: 
* *A principal * An email address prepended with “mailto:” 
* *An email address without the “mailto:”-prefix * A two-item tuple containing a common name and an email address *

Может быть задано любое количество параметров участника, они будут использоваться по умолчанию, если для параметра no_default_parameters не установлено значение True:

partstat=NEEDS-ACTION cutype=UNKNOWN (unless a principal object is given) rsvp=TRUE role=REQ-PARTICIPANT schedule-agent is not set

```bash
copy(keep_uid=False, new_parent=None)
```
События, задачи и т.д. могут быть скопированы в пределах того же календаря, в другой календарь или даже на другой сервер caldav

```bash
data
```
vCal представление объекта в виде обычной строки

```bash
get_duration()
```
Этот метод вернет длительность, если она установлена, в противном случае разница между DUE и DTSTART (если оба
из них установлены).

```bash
instance
```
vobject instance of the object

```bash
load(only_if_unloaded=False)
```
Загружает объект с сервера caldav.

```bash
save(no_overwrite=False, no_create=False, obj_type=None, 
increase_seqno=True, if_schedule_tag_match=False)
```
Сохранение объекта; можно использовать для создания и обновления.

no_overwrite и no_create проверят, существует ли объект. Эти два понятия взаимоисключают друг друга. Некоторые серверы не поддерживают поиск uid объекта без явного указания того, каким типом объекта он должен быть, следовательно, obj_type может быть передан. obj_type используется только в сочетании с no_over_write и no_create.

```bash
set_relation(other, reltype=None, set_reverse=True)
```
Устанавливает связь между этим объектом и другим объектом (заданным uid или object).

```bash
vobject_instance
```
vobject instance of the object

```bash
wire_data
```
vCal representation of the object in wire format (UTF-8, CRLN)

## Класс Calendar Set

```bash
class caldav.objects.CalendarSet(client=None, url=None, parent=None, 
name=None, id=None, props=None, **extra)
```
A CalendarSet is a set of calendars.

### Функции Calendar Set

```bash
calendar(name=None, cal_id=None)
```
Метод calendar вернет объект calendar. Если он получит cal_id, но без имени, он не будет инициировать никакой связи с сервером

• name: return the calendar with this display name

• cal_id: return the calendar with this calendar id or URL

```bash
calendars()
```
Перечисление всей коллекции календарей в этом наборе.

```bash
make_calendar(name=None, cal_id=None, 
supported_calendar_component_set=None)
```
Utility method for creating a new calendar.

• name: the display name of the new calendar

• cal_id: the uuid of the new calendar

• supported_calendar_component_set: what kind of objects (EVENT, VTODO, VFREEBUSY, VJOURNAL) the calendar should handle.

## Класс DAVObject

```bash
class caldav.objects.DAVObject(client=None, url=None, parent=None, 
name=None, id=None, props=None, **extra)
```
Базовый класс для всех объектов DAV. Может быть создан с помощью клиента и абсолютного или относительного URL-адреса, а также из родительского объекта.

### Функции DAVObject

```bash
children(type=None)
```
List children, using a propfind (resourcetype) on the parent object, at depth = 1.

```bash
delete()
```
Удаление объекта.

```bash
get_display_name()
```
Получение имени календаря.

```bash
get_properties(props=None, depth=0, parse_response_xml=True, parse_props=True)
```
Получение свойств (PROPFIND) объекта.

С parse_response_xml и parse_props, установленными в True, будет предпринята наилучшая попытка декодирования XML, который мы получаем с сервера, но это работает только для свойств, которые не имеют сложных типов. Если для parse_response_xml установлено значение False, будет возвращен объект DAVResponse, и декодирование зависит от вызывающей стороны. Если для parse_props установлено значение false, а для parse_response_xml - значение true, будут возвращены xml-элементы, а не значения.

• props = [dav.ResourceType(), dav.DisplayName(), . . . ]

```bash
save()
```
Сохранение объекта. Это абстрактный метод, который реализуют все классы, производные от DAV Object.

```bash
set_properties(props=None)
```
Установление свойств (PROPPATCH) для объекта.

• props = [dav.DisplayName(‘name’), . . . ]


## Класс Free Busy

```bash
class caldav.objects.FreeBusy(parent, data, url=None, id=None)
```
Объект FreeBusy используется для представления freebusyresponse с сервера.

## Класс Principal

```bash
class caldav.objects.Principal(client=None, url=None)
```
This class represents a DAV Principal. It doesn’t do much, except keep track of the URLs for the calendarhome-set, etc.

### Функции Principal

```bash
calendar(name=None, cal_id=None, cal_url=None)
```
Метод calendar вернет объект calendar. Он не будет инициировать никакой связи с сервером.

```bash
calendar_user_address_set()
```
defined in RFC6638

```bash
calendars()
```
Возвращает principials календари.

```bash
get_vcal_address()
```
Возвращает principal как объект icalendar.vCalAddress

```bash
make_calendar(name=None, cal_id=None, supported_calendar_component_set=None)
```
Удобный метод, обходит объект self.calendar_home_set.

## Класс Todo

```bash
class caldav.objects.Todo(client=None, url=None, data=None, parent=None, 
id=None, props=None)
```
Объект Todo используется для представления элемента todo (TODO-задача). Todo-объект может быть завершен.

### Функции Todo

```bash
complete(completion_timestamp=None, handle_rrule=False, rrule_mode=’safe’)
```
Помечает задачу как выполненную.

• completion_timestamp - datetime object. Defaults to datetime.now().

• handle_rrule - if set to True, the library will try to be smart if the task is recurring. The default is
False, for backward compatibility. I may consider making this one mandatory.

• rrule_mode - The RFC leaves a lot of room for intepretation on how to handle recurring tasks,
and what works on one server may break at another. The following modes are accepted:

* this_and_future
* safe

```bash
get_due()
```
У VTODO может быть установлен срок выполнения или продолжительность выполнения. Возвращает или рассчитывает продолжительность выполнения.

```bash
set_due(due, move_dtstart=False, check_dependent=False)
```
RFC указывает, что VTODO не может иметь как due, так и duration, поэтому при установке due поле duration должно быть удалено. 

check_dependent=True вызовет некоторую ошибку, если существует родительский компонент календаря (через RELATED-TO), а родительский due или dtend находится перед новым dtend).

```bash
set_duration(duration, movable_attr=’DTSTART’)
```
Метод, обратный предыдущему.

```bash
uncomplete()
```
Помечает выполненную задачу как незавершенную.


## Класс Synchronizable Calendar Object Collection

```bash
class caldav.objects.SynchronizableCalendarObjectCollection(calendar, 
objects, sync_token)
```
Этот класс может содержать кэшированный snapshot(возможно, снимок) календаря, и изменения в календаре можно легко скопировать с помощью метода синхронизации.

Чтобы создать объект SynchronizableCalendarObjectCollection, используйте calendar.objects(load_objects=True)

### Функции Synchronizable Calendar Object Collection

```bash
objects_by_url()
```
Возвращает dict содержимого SynchronizableCalendarObjectCollection, URLs -> objects

```bash
sync()
```
Этот метод свяжется с сервером caldav, запросит у него все изменения и синхронизирует коллекцию.

