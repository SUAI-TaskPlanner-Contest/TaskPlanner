# Базовые принципы работы с CalDav

1. Всегда нужно начинать с инициирования объекта *caldav.DAVClient*, этот объект содержит данные аутентификации для сервера.
2. Из объекта *client* можно получить доступ к объекту *caldav.Principal*, представляющий вошедшего в систему участника.
3. Из объекта *principal* можно извлекать / генерировать *caldav.Calendar* объекты.
4. Из объекта *calendar* можно извлекать / генерировать *caldav.Event* объекты и *caldav.Todo* объекты (а также *caldav.Journal* объекты). В конечном счете библиотека также может извлекать объекты базового класса (*caldav.objects.CalendarObjectResource*).

# Основные функции CalDav для работы с календарём

Настройка клиентского объекта *caldav* и *principal* объекта:
```python
with caldav.DAVClient(url=url, username=username, password=password) as client:
    my_principal = client.principal()
    ...
```
Извлечение календарей:
```python
calendars = my_principal.calendars()
```
Создание календаря:
```python
my_new_calendar = my_principal.make_calendar(name="Test calendar")
```
Можно извлечь календарь с известным URL-адресом, не проходя через *principal*:
```python
the_same_calendar = client.calendar(url=my_new_calendar.url)
```
Удаление календаря (или, в принципе, любого объекта):
```python
my_new_calendar.delete()
```
Создание списка задач:
```python
my_new_tasklist = my_principal.make_calendar(
            name="Test tasklist", supported_calendar_component_set=['VTODO'])
```
name - название списка объектов

supported_calendar_component_set - поддерживаемые объекты списка. Могут быть VEVENT - событие, VTODO - задача, VJOURNAL - заметка

Добавление задачи в список задач:
```python
my_new_tasklist.save_todo(
    ics = "RRULE:FREQ=YEARLY",
    summary="Поход по магазинам",
    dtstart=date(2023, 4, 1),
    due=date(2023,4,2),
    categories=['family', 'finance'],
    status='NEEDS-ACTION')
```
RRULE - правило повторения. Можно указать частоту повторения (FREQ), интервал повторения (INTERVAL), счётчик (COUNT) и другие параметры (больше примеров и информации: https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html).

Пример RRULE:  "RRULE:FREQ=DAILY;INTERVAL=2;COUNT=3". При заданных параметрах, задача будет повторяться каждые два дня, пока счётчик повторений не достигнет отметки 3. Например, если время начала задачи задано на 02.04.2023, то задача повторится 04.04.2023 и 06.04.2023.

summary: в спецификации сказано, что это краткое описание задачи или её заголовок.

dtstart - дата начала задачи. Обычно передаётся в формате: 20220223T230000, что означает 23 фев. 2022 года, 23 часа. Можно преобразовывать дату к нужному формату в самой функции, с помощью date().

due - дата окончания задачи. Передаётся в том же формате, что и dtstart.

categories - категории задачи.

status - статус задачи. Определены следующие статусы задач: NEEDS-ACTION - задача нуждается в действии, COMPLETED - задача выполнена, IN-PROCESS - задача в процессе выполнения, CANCELLED - задача была отменена.

Извлечение задач:
```python
todos = my_new_tasklist.todos()
```
Поиск задач в заданном временном интервале:
```python
todos = my_new_calendar.search(
    start=datetime(2023, 1, 1), end=datetime(2024, 1, 1),
    compfilter='VTODO',event=True, expand=True)
```

* start - левая граница поиска;
* end - правая граница поиска;
* compfilter - VTODO или VEVENT;
* event - True или False.

Отметка о выполнении задачи:
```python
todos[0].complete()
```

# Описание классов и функций CalDav

## Класс DAV client
```python
class caldav.davclient.DAVClient(url, proxy=None, username=None, 
password=None, auth=None, timeout=None, 
ssl_verify_cert=True, ssl_cert=None, headers={}, huge_tree=False)
```
Базовый клиент для webdav, использует библиотеку запросов; предоставляет доступ к низкоуровневым операциям с сервером caldav.

* proxy - Строка, определяющая прокси-сервер: "hostname:port" ("имя хоста:порт");
* username и password - должны быть переданы в качестве аргументов или в URL-адресе;
* auth, timeout и ssl_verify_cert - передаются в requests.request.
* ssl_verify_cert - может быть путем к CA-bundle или False. (CA-bundle - файл, который содержит корневые и промежуточные сертификаты в определенном порядке.)
* huge_tree - логическое значение (т.е. True или False). Позволяет XMLParser huge_tree обрабатывать большие события.

### Функции DAV client
```python
calendar(**kwargs)
```
Возвращает объект calendar.

Как правило, в качестве именованного параметра (это и есть **kwargs) должен быть указан  URL-адрес (url=)

Если URL-адрес календаря не известен, вместо этого следует использовать client.principal().calendar(...) или client.principal().calendars()

```python
close()
```
Закрывает сессию объекта DAVClient.

```python
delete(url)
```
Отправляет запрос на удаление.

```python
post(url, body, headers={})
```
Отправляет запрос на публикацию.

* body - тело запроса;
* headers - заголовки как в HTTP протоколе.

```python
principal(*largs, **kwargs)
```
Этот метод возвращает объект caldav.Principal с методами более высокого уровня для работы с календарями участников.

```python
propfind(url=None, props=”, depth=0)
```
Отправляет запрос на propfind. propfind - получение свойств файла или каталога.

• url: url для корня propfind;

• props = (xml запрос), нужные нам свойства. Примеры xml-запросов тут (начиная с пункта №14): http://www.webdav.org/specs/rfc4918.html#xml.element.definitions;

• depth: максимальная глубина рекурсии.

```python
proppatch(url, body, dummy=None)
```
Отправляет запрос на proppatch. proppatch - изменение свойств файла или каталога.

• url: url для корня propfind.

• body: XML propertyupdate запрос. Для примеров перейти по ссылке, указанной в функции propfind;

• dummy: параметр совместимости

```python
put(url, body, headers={})
```
Отправляет запрос на put.

```python
report(url, query=”, depth=0)
```
Отправляет запрос на report.

• url: url для корня propfind.

• query: XML запрос

• depth: максимальная глубина рекурсии

```python
request(url, method=’GET’, body=”, headers={})
```
Фактически отправляет запрос и выполняет аутентификацию.


## Класс DAV response

```python
class caldav.davclient.DAVResponse(response, davclient=None)
```
Этот класс является ответом на запрос DAV. Он создается из клиентского класса DAV. 
Поскольку мы получаем XML-ответы, он пытается разобрать их в self.tree

### Функции DAV response

```python
expand_simple_props(props=[], multi_value_props=[], xpath=None)
```
Функция find_objects_and_props() остановится на xml-элементе под тегом prop. Этот метод превратит эти реквизиты в текст.

Выполняет find_objects_and_props, если он еще не запущен, затем изменяет и возвращает self.objects

```python
find_objects_and_props()
```
Проверяет ответ сервера, проверяет, ожидаемый ли формат имеет ответ сервера, находит hrefs and props из него и проверяет статус доставки.

Проанализированные данные будут помещены в self.objects, dict {href: {proptag: prop_element}}.

self.sync_token будет заполнен, если найден, self.objects будет заполнен.

```python
validate_status(status)
```
Статус - это строка типа: “HTTP/1.1 404 Not Found”. 200, 207 и 404 считаются хорошими статусами.

## Класс Objects
“Объект DAV” - это все, что мы получаем с сервера caldav или загружаем на сервер caldav, в частности, основные элементы, календари и события календаря.

```python
class caldav.objects.Calendar(client=None, url=None, 
parent=None, name=None, id=None, props=None, **extra)
```
Объект Calendar используется для представления коллекции календарей.

### Функции Calendar

```python
add_todo(ical=None, no_overwrite=False, no_create=False, **ical_data)
```
Добавит новую задачу в календарь с заданным ical.

• ical - ical объект.

```python
build_search_xml_query(comp_class=None, todo=None, ignore_completed1=None, 
ignore_completed2=None, ignore_completed3=None, event=None,
filters=None, expand=None, start=None, end=None, **kwargs)
```
Этот метод создаст поисковый запрос caldav в виде объекта etree.

```python
freebusy_request(start, end)
```
Выполняет поиск по календарю, но возвращает только информацию о free/busy (занят или нет).

• start = datetime.today().

• end = такой же формат, как в start.

```python
get_supported_components()
```
Возвращает список типов компонентов, поддерживаемых календарем, в строковом формате (typically [‘VJOURNAL’, ‘VTODO’, ‘VEVENT’])

```python
objects(sync_token=None, load_objects=False)
```
Этот метод вернет все объекты в календаре, если sync_token не передан или если sync_token неизвестен серверу. Если передан synctoken, известный серверу, он вернет объекты, которые были добавлены, удалены или изменены с момента последней установки токена синхронизации.

Если для параметра load_objects установлено значение True, объекты будут загружены - в противном случае будут возвращены пустые объекты CalendarObjectResource.

```python
objects_by_sync_token(sync_token=None, load_objects=False)
```
То же, что и objects

```python
save()
```
Метод сохранения календаря пока используется только для его создания.

```python
save_todo(ical=None, no_overwrite=False, no_create=False, **ical_data)
```
Добавляет новую задачу в календарь с заданным ical.

• ical - ical object

```python
save_with_invites(ical, attendees, **attendeeoptions)
```
Отправляет запрос schedule на сервер. Эквивалентно save_event, save_to do и т.д., Но участники будут добавлены в объект ical перед отправкой его на сервер.

```python
search(xml=None, comp_class=None, todo=None, include_completed=False, 
sort_keys=(), split_expanded=True, **kwargs)
```
Создает XML-запрос, отправляет запрос REPORT на сервер и возвращает найденные объекты, в конечном итоге сортируя их перед доставкой.

Этот метод содержит некоторую специальную логику, гарантирующую, что он может последовательно возвращать список ожидающих выполнения задач в любой серверной реализации. В будущем это может также включать обходные пути и фильтрацию на стороне клиента, чтобы убедиться в согласованности других результатов поиска в разных серверных реализациях.

Параметры:

• xml - если используем этот поисковый запрос, игнорируем другие параметры фильтра

• comp_class - можно установить на event, todo или journal, чтобы ограничить поиск этим типом ресурса.

• todo - устанавливает comp_class в значение todo и ограничивает поиск ожидающими задачами

• include_completed - включает в поиск выполненные задачи

• event - устанавливает comp_class в значение event

• text attribute search parameters: поиск по параметрам формата ical: category, uid, summary, сomment, description, location, status

• no-category, no-summary, etc . . . поиск объектов, у которых нет этих атрибутов.

• expand - do server side expanding of recurring events/tasks

• start, end: поиск по заданному промежутку времени

• filters - другие типы фильтров (в формате xml-дерева)

• sort_keys - список атрибутов, используемых при сортировке

```python
todos(sort_keys=(’due’, ’priority’), include_completed=False)
```
Извлекает список событий todo

• sort_keys: используйте это поле в VTODO для сортировки (повторяемая строка в нижнем регистре, т.е. (‘priority’,’due’)).

• include_completed: логическое значение (True или False)- по умолчанию отображаются только отложенные задачи.


## Класс Calendar Object Resource

```python
class caldav.objects.CalendarObjectResource(client=None, url=None, 
data=None, parent=None, id=None, props=None)
```
Согласно RFC 4791, раздел 4.1, “Ресурсом объекта календаря” может быть событие, элемент задач, запись в журнале или запись "свободен/занят".

### Функции Calendar Object Resource

```python
add_attendee(attendee, no_default_parameters=False, **parameters)
```
Для текущего (события/задачи/журнала) добавляет участника.

Участником может быть любой из следующих: 
* *A principal * Адрес электронной почты с добавлением “mailto:” (Mailto – это префикс в адресе ссылки, благодаря которому можно автоматически открывать почтовый клиент с заполненными данными. Пример: mailto:bernard@example.com)
* *Адрес электронной почты без префикса “mailto:” * Кортеж из двух элементов, содержащий общее имя и адрес электронной почты

Может быть задано любое количество параметров участника, они будут использоваться по умолчанию, если для параметра no_default_parameters не установлено значение True:

* partstat=NEEDS-ACTION (статус объекта. Также существуют ACCEPTED - задача принята, DECLINED - задача отклонена, TENTATIVE - ???, DELEGATED - задача поручена, COMPLETED - задача выполнена, IN-PROCESS - в процессе выполнения)
* cutype=UNKNOWN (Calenar user type - Тип пользователя календаря. Существуют: INDIVIDUAL - индивидуальный, GROUP - группа отдельных лиц, RESOURCE - физический ресурс, ROOM - Ресурс комнаты, UNKNOWN - неизвестен)
* rsvp=TRUE (Параметр определяет ожидание ответа от пользователя календаря, указанного значением свойства. Этот параметр используется "Организатором" для запроса ответа о статусе участия от "Участника" группового запланированного мероприятия или текущих дел.)
* role=REQ-PARTICIPANT (роль участника)
* schedule-agent (агент планирования. Принимает значения SERVER, CLIENT, NONE. Указывает агента, который, как ожидается, будет доставлять сообщения о расписании соответствующему "Организатору" или "Участнику".)

```python
copy(keep_uid=False, new_parent=None)
```
События, задачи и т.д. могут быть скопированы в пределах того же календаря, в другой календарь или даже на другой сервер caldav

```python
data
```
vCal представление объекта в виде обычной строки

```python
get_duration()
```
Этот метод вернет длительность, если она установлена, в противном случае разница между DUE и DTSTART (если оба
из них установлены).

```python
load(only_if_unloaded=False)
```
Загружает объект с сервера caldav.

```python
save(no_overwrite=False, no_create=False, obj_type=None, 
increase_seqno=True, if_schedule_tag_match=False)
```
Сохранение объекта; можно использовать для создания и обновления.

no_overwrite и no_create проверят, существует ли объект. Эти два понятия взаимоисключают друг друга. Некоторые серверы не поддерживают поиск uid объекта без явного указания того, каким типом объекта он должен быть, следовательно, obj_type может быть передан. obj_type используется только в сочетании с no_over_write и no_create.

```python
set_relation(other, reltype=None, set_reverse=True)
```
Устанавливает связь между этим объектом и другим объектом (заданным uid или object).

```python
vobject_instance
```
vobject пример объекта.

```python
wire_data
```
vCal представление объекта в формате wire (UTF-8, CRLN)

## Класс Calendar Set

```python
class caldav.objects.CalendarSet(client=None, url=None, parent=None, 
name=None, id=None, props=None, **extra)
```
CalendarSet это набор календарей.

### Функции Calendar Set

```python
calendar(name=None, cal_id=None)
```
Метод calendar вернет объект calendar. Если он получит cal_id, но без имени, он не будет инициировать никакой связи с сервером

• name: возвращает календарь с заданным именем.

• cal_id: возвращает календарь с заданным идентификатором календаря или URL-адресом.

```python
calendars()
```
Перечисление всей коллекции календарей в этом наборе.

```python
make_calendar(name=None, cal_id=None, 
supported_calendar_component_set=None)
```
Метод для создания нового календаря.

• name: отображаемое имя нового календаря.

• cal_id: uuid нового календаря.

• supported_calendar_component_set: какой тип объекта должен поддерживать календарь (EVENT, VTODO, VFREEBUSY, VJOURNAL).

## Класс DAVObject

```python
class caldav.objects.DAVObject(client=None, url=None, parent=None, 
name=None, id=None, props=None, **extra)
```
Базовый класс для всех объектов DAV. Может быть создан с помощью клиента и абсолютного или относительного URL-адреса, а также из родительского объекта.

### Функции DAVObject

```python
children(type=None)
```
Перечисляет потомков объекта, используя propfind (тип ресурса) для родительского объекта, с глубиной = 1.

```python
delete()
```
Удаление объекта.

```python
get_display_name()
```
Получение имени календаря.

```python
get_properties(props=None, depth=0, parse_response_xml=True, parse_props=True)
```
Получение свойств (PROPFIND) объекта.

С parse_response_xml и parse_props, установленными в True, будет предпринята наилучшая попытка декодирования XML, который мы получаем с сервера, но это работает только для свойств, которые не имеют сложных типов. Если для parse_response_xml установлено значение False, будет возвращен объект DAVResponse, и декодирование зависит от вызывающей стороны. Если для parse_props установлено значение false, а для parse_response_xml - значение true, будут возвращены xml-элементы, а не значения.

• props = [dav.ResourceType(), dav.DisplayName(), . . . ]

```python
save()
```
Сохранение объекта. Это абстрактный метод, который реализуют все классы, производные от DAV Object.

```python
set_properties(props=None)
```
Установление свойств (PROPPATCH) для объекта.

• props = [dav.DisplayName(‘name’), . . . ]


## Класс Free Busy

```python
class caldav.objects.FreeBusy(parent, data, url=None, id=None)
```
Объект FreeBusy используется для представления freebusyresponse с сервера.

## Класс Principal

```python
class caldav.objects.Principal(client=None, url=None)
```
Этот класс представляет DAV "Организатора". Он мало что делает, кроме отслеживания URL-адресов для набора calendarhome и т.д.

### Функции Principal

```python
calendar(name=None, cal_id=None, cal_url=None)
```
Метод calendar вернет объект calendar. Он не будет инициировать никакой связи с сервером.

```python
calendar_user_address_set()
```
описан в RFC6638. (ссылка: https://datatracker.ietf.org/doc/html/rfc6638)

```python
calendars()
```
Возвращает principials календари.

```python
get_vcal_address()
```
Возвращает principal как объект icalendar.vCalAddress

```python
make_calendar(name=None, cal_id=None, supported_calendar_component_set=None)
```
Удобный метод, обходит объект self.calendar_home_set.

## Класс Todo

```python
class caldav.objects.Todo(client=None, url=None, data=None, parent=None, 
id=None, props=None)
```
Объект Todo используется для представления элемента todo (TODO-задача). Todo-объект может быть завершен.

### Функции Todo

```python
complete(completion_timestamp=None, handle_rrule=False, rrule_mode=’safe’)
```
Помечает задачу как выполненную.

• completion_timestamp - объект datetime. По умолчанию используется datetime.now().

• handle_rrule - Значение по умолчанию False для обеспечения обратной совместимости.

• rrule_mode - RFC оставляет много возможностей для интерпретации того, как обрабатывать повторяющиеся задачи, и то, что работает на одном сервере, может сломаться на другом. Принимаются следующие режимы:

* this_and_future
* safe

```python
get_due()
```
У VTODO может быть установлен срок выполнения или продолжительность выполнения. Возвращает или рассчитывает продолжительность выполнения.

```python
set_due(due, move_dtstart=False, check_dependent=False)
```
RFC указывает, что VTODO не может иметь как due, так и duration, поэтому при установке due поле duration должно быть удалено. 

check_dependent=True вызовет некоторую ошибку, если существует родительский компонент календаря (через RELATED-TO), а родительский due или dtend находится перед новым dtend).

```python
set_duration(duration, movable_attr=’DTSTART’)
```
Метод, обратный предыдущему.

```python
uncomplete()
```
Помечает выполненную задачу как незавершенную.


## Класс Synchronizable Calendar Object Collection

```python
class caldav.objects.SynchronizableCalendarObjectCollection(calendar, 
objects, sync_token)
```
Этот класс может содержать кэшированный snapshot(возможно, снимок) календаря, и изменения в календаре можно легко скопировать с помощью метода синхронизации.

Чтобы создать объект SynchronizableCalendarObjectCollection, используйте calendar.objects(load_objects=True)

### Функции Synchronizable Calendar Object Collection

```python
objects_by_url()
```
Возвращает dict содержимого SynchronizableCalendarObjectCollection, URLs -> objects

```python
sync()
```
Этот метод свяжется с сервером caldav, запросит у него все изменения и синхронизирует коллекцию.

