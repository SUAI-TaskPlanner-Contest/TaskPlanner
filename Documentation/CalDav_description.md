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
Basic client for webdav, uses the requests lib; gives access to low-level operations towards the caldav server.
### Функции DAV client
```bash
calendar(**kwargs)
```
Returns a calendar object.

```bash
close()
```
Closes the DAVClient’s session object

```bash
delete(url)
```
Send a delete request.

```bash
post(url, body, headers={})
```
Send a POST request.

```bash
principal(*largs, **kwargs)
```
Convenience method, it gives a bit more object-oriented feel to write client.principal() than Principal(client).
This method returns a caldav.Principal object, with higher-level methods for dealing with the principals calendars.

```bash
propfind(url=None, props=”, depth=0)
```
Send a propfind request.

• url: url for the root of the propfind.

• props = (xml request), properties we want

• depth: maximum recursion depth

```bash
proppatch(url, body, dummy=None)
```
Send a proppatch request.

• url: url for the root of the propfind.

• body: XML propertyupdate request

• dummy: compatibility parameter

```bash
put(url, body, headers={})
```
Send a put request.

```bash
report(url, query=”, depth=0)
```
Send a report request.

• url: url for the root of the propfind.

• query: XML request

• depth: maximum recursion depth

```bash
request(url, method=’GET’, body=”, headers={})
```
Actually sends the request, and does the authentication


## Класс DAV response

```bash
class caldav.davclient.DAVResponse(response, davclient=None)
```
This class is a response from a DAV request. It is instantiated from the DAVClient class. End users of the library
should not need to know anything about this class. Since we often get XML responses, it tries to parse it into
self.tree

### Функции DAV response

```bash
expand_simple_props(props=[], multi_value_props=[], xpath=None)
```
The find_objects_and_props() will stop at the xml element below the prop tag. This method will expand
those props into text.

Executes find_objects_and_props if not run already, then modifies and returns self.objects
```bash
find_objects_and_props()
```
Check the response from the server, check that it is on an expected format, find hrefs and props from it and
check statuses delivered.

The parsed data will be put into self.objects, a dict {href: {proptag: prop_element}}. Further parsing of
the prop_element has to be done by the caller.

self.sync_token will be populated if found, self.objects will be populated.
```bash
validate_status(status)
```
status is a string like “HTTP/1.1 404 Not Found”. 200, 207 and 404 are considered good statuses. The
SOGo caldav server even returns “201 created” when doing a sync-report, to indicate that a resource was
created after the last sync-token. This makes sense to me, but I’ve only seen it from SOGo, and it’s not in
accordance with the examples in rfc6578.

## Класс Objects
A “DAV object” is anything we get from the caldav server or push into the caldav server, notably principal, calendars
and calendar events.

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
This method will produce a caldav search query as an etree object.

It is primarily to be used from the search method. See the documentation for the search method for more
information

```bash
freebusy_request(start, end)
```
Search the calendar, but return only the free/busy information.

• start = datetime.today().

• end = same as above.

```bash
get_supported_components()
```
returns a list of component types supported by the calendar, in string format (typically [‘VJOURNAL’,
‘VTODO’, ‘VEVENT’])

```bash
objects(sync_token=None, load_objects=False)
```
Do a sync-collection report, ref RFC 6578 and https://github.com/python-caldav/caldav/issues/87

This method will return all objects in the calendar if no sync_token is passed (the method should then be
referred to as “objects”), or if the sync_token is unknown to the server. If a sync-token known by the server
is passed, it will return objects that are added, deleted or modified since last time the sync-token was set.

If load_objects is set to True, the objects will be loaded - otherwise empty CalendarObjectResource objects
will be returned.

This method will return a SynchronizableCalendarObjectCollection object, which is an iterable.

```bash
objects_by_sync_token(sync_token=None, load_objects=False)
```
То же, что и objects
```bash
save()
```
The save method for a calendar is only used to create it, for now. We know we have to create it when we
don’t have a url.

```bash
save_todo(ical=None, no_overwrite=False, no_create=False, **ical_data)
```
Add a new task to the calendar, with the given ical.

• ical - ical object (text)

```bash
save_with_invites(ical, attendees, **attendeeoptions)
```
sends a schedule request to the server. Equivalent with save_event, save_todo, etc, but the attendees will
be added to the ical object before sending it to the server.

```bash
search(xml=None, comp_class=None, todo=None, include_completed=False, 
sort_keys=(), split_expanded=True, **kwargs)
```
Creates an XML query, does a REPORT request towards the server and returns objects found, eventually
sorting them before delivery.

This method contains some special logics to ensure that it can consistently return a list of pending tasks on
any server implementation. In the future it may also include workarounds and client side filtering to make
sure other search results are consistent on different server implementations.

Parameters supported:

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
fetches a list of todo events

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
For the current (event/todo/journal), add an attendee.

The attendee can be any of the following: * A principal * An email address prepended with “mailto:” * An
email address without the “mailto:”-prefix * A two-item tuple containing a common name and an email
address * (not supported, but planned: an ical text line starting with the word “ATTENDEE”)

Any number of attendee parameters can be given, those will be used as defaults unless
no_default_parameters is set to True:

partstat=NEEDS-ACTION cutype=UNKNOWN (unless a principal object is given) rsvp=TRUE
role=REQ-PARTICIPANT schedule-agent is not set

```bash
add_organizer()
```
goes via self.client, finds the principal, figures out the right attendee-format and adds an organizer line to
the event

```bash
copy(keep_uid=False, new_parent=None)
```
Events, todos etc can be copied within the same calendar, to another calendar or even to another caldav
server

```bash
data
```
vCal representation of the object as normal string

```bash
expand_rrule(start, end)
```
This method will transform the calendar content of the event and expand the calendar data from a “master
copy” with RRULE set and into a “recurrence set” with RECURRENCE-ID set and no RRULE set. The
main usage is for client-side expansion in case the calendar server does not support server-side expansion.
It should be safe to save back to the server, the server should recognize it as recurrences and should not
edit the “master copy”. If doing a self.load, the calendar content will be replaced with the “master copy”.
However, as of 2022-10 there is no test code verifying this.

• event – Event

• start – datetime.datetime

• end – datetime.datetime

```bash
get_duration()
```
According to the RFC, either DURATION or DUE should be set for a task, but never both - implicitly meaning that DURATION is the difference between DTSTART and DUE (personally I believe that’s
stupid. If a task takes five minutes to complete - say, fill in some simple form that should be delivered before midnight at new years eve, then it feels natural for me to define “duration” as five minutes, DTSTART
to “some days before new years eve” and DUE to 20xx-01-01 00:00:00 - but I digress.

This method will return DURATION if set, otherwise the difference between DUE and DTSTART (if both
of them are set).

TODO: should be fixed for Event class as well (only difference is that DTEND is used rather than DUE)
and possibly also for Journal.

WARNING: this method is likely to be deprecated and moved to the icalendar library. If you decide to use
it, please put caldav<2.0 in the requirements.

```bash
icalendar_component
```
icalendar component - should not be used with recurrence sets

```bash
icalendar_instance
```
icalendar instance of the object

```bash
instance
```
vobject instance of the object

```bash
load(only_if_unloaded=False)
```
(Re)load the object from the caldav server.

```bash
save(no_overwrite=False, no_create=False, obj_type=None, 
increase_seqno=True, if_schedule_tag_match=False)
```
Save the object, can be used for creation and update.

no_overwrite and no_create will check if the object exists. Those two are mutually exclusive. Some servers
don’t support searching for an object uid without explicitly specifying what kind of object it should be,
hence obj_type can be passed. obj_type is only used in conjunction with no_overwrite and no_create.

```bash
set_relation(other, reltype=None, set_reverse=True)
```
Sets a relation between this object and another object (given by uid or object).

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
The calendar method will return a calendar object. If it gets a cal_id but no name, it will not initiate any
communication with the server

• name: return the calendar with this display name

• cal_id: return the calendar with this calendar id or URL

```bash
calendars()
```
List all calendar collections in this set.

```bash
make_calendar(name=None, cal_id=None, supported_calendar_component_set=None)
```
Utility method for creating a new calendar.

• name: the display name of the new calendar

• cal_id: the uuid of the new calendar

• supported_calendar_component_set: what kind of objects (EVENT, VTODO, VFREEBUSY,
VJOURNAL) the calendar should handle. Should be set to [‘VTODO’] when creating a task
list in Zimbra - in most other cases the default will be OK.


## Класс DAVObject

```bash
class caldav.objects.DAVObject(client=None, url=None, parent=None, 
name=None, id=None, props=None, **extra)
```
Base class for all DAV objects. Can be instantiated by a client and an absolute or relative URL, or from the
parent object.

### Функции DAVObject

```bash
children(type=None)
```
List children, using a propfind (resourcetype) on the parent object, at depth = 1.

TODO: This is old code, it’s querying for DisplayName and ResourceTypes prop and returning a tuple of
those. Those two are relatively arbitrary. I think it’s mostly only calendars having DisplayName, but it
may make sense to ask for the children of a calendar also as an alternative way to get all events? It should
be redone into a more generic method, and it should probably return a dict rather than a tuple. We should
also look over to see if there is any code duplication.

```bash
delete()
```
Delete the object.

```bash
get_display_name()
```
Get calendar display name

```bash
get_properties(props=None, depth=0, parse_response_xml=True, parse_props=True)
```
Get properties (PROPFIND) for this object.

With parse_response_xml and parse_props set to True a best-attempt will be done on decoding the
XML we get from the server - but this works only for properties that don’t have complex types. With
parse_response_xml set to False, a DAVResponse object will be returned, and it’s up to the caller to decode. With parse_props set to false but parse_response_xml set to true, xml elements will be returned
rather than values.

• props = [dav.ResourceType(), dav.DisplayName(), . . . ]

```bash
save()
```
Save the object. This is an abstract method, that all classes derived from DAVObject implement.

```bash
set_properties(props=None)
```
Set properties (PROPPATCH) for this object.

• props = [dav.DisplayName(‘name’), . . . ]


## Класс Free Busy

```bash
class caldav.objects.FreeBusy(parent, data, url=None, id=None)
```
The FreeBusy object is used to represent a freebusy response from the server. __init__ is overridden, as a
FreeBusy response has no URL or ID. The inheritated methods .save and .load is moot and will probably throw
errors (perhaps the class hierarchy should be rethought, to prevent the FreeBusy from inheritating moot methods)

Update: With RFC6638 a freebusy object can have an URL and an ID.


## Класс Principal

```bash
class caldav.objects.Principal(client=None, url=None)
```
This class represents a DAV Principal. It doesn’t do much, except keep track of the URLs for the calendarhome-set, etc.

A principal MUST have a non-empty DAV:displayname property (defined in Section 13.2 of [RFC2518]), and a
DAV:resourcetype property (defined in Section 13.9 of [RFC2518]). Additionally, a principal MUST report the
DAV:principal XML element in the value of the DAV:resourcetype property.

(TODO: the resourcetype is actually never checked, and the DisplayName is not stored anywhere)

### Функции Principal

```bash
calendar(name=None, cal_id=None, cal_url=None)
```
The calendar method will return a calendar object. It will not initiate any communication with the server.

```bash
calendar_user_address_set()
```
defined in RFC6638

```bash
calendars()
```
Return the principials calendars

```bash
get_vcal_address()
```
Returns the principal, as an icalendar.vCalAddress object

```bash
make_calendar(name=None, cal_id=None, supported_calendar_component_set=None)
```
Convenience method, bypasses the self.calendar_home_set object. See CalendarSet.make_calendar for
details.


## Класс Todo

```bash
class caldav.objects.Todo(client=None, url=None, data=None, parent=None, 
id=None, props=None)
```
The Todo object is used to represent a todo item (VTODO). A Todo-object can be completed. Extra logic for
different ways to complete one recurrence of a recurrent todo. Extra logic to handle due vs duration.

### Функции Todo

```bash
complete(completion_timestamp=None, handle_rrule=False, rrule_mode=’safe’)
```
Marks the task as completed.

• completion_timestamp - datetime object. Defaults to datetime.now().

• handle_rrule - if set to True, the library will try to be smart if the task is recurring. The default is
False, for backward compatibility. I may consider making this one mandatory.

• rrule_mode - The RFC leaves a lot of room for intepretation on how to handle recurring tasks,
and what works on one server may break at another. The following modes are accepted:

– this_and_future

– safe

```bash
get_due()
```
A VTODO may have due or duration set. Return or calculate due.

```bash
set_due(due, move_dtstart=False, check_dependent=False)
```
The RFC specifies that a VTODO cannot have both due and duration, so when setting due, the duration
field must be evicted

check_dependent=True will raise some error if there exists a parent calendar component (through
RELATED-TO), and the parents due or dtend is before the new dtend).

```bash
set_duration(duration, movable_attr=’DTSTART’)
```
If DTSTART and DUE/DTEND is already set, one of them should be moved. Which one? I believe that
for EVENTS, the DTSTART should remain constant and DTEND should be moved, but for a task, I think
the due date may be a hard deadline, hence by default we’ll move DTSTART.

```bash
uncomplete()
```
Undo completion - marks a completed task as not completed


## Класс Synchronizable Calendar Object Collection

```bash
class caldav.objects.SynchronizableCalendarObjectCollection(calendar, 
objects, sync_token)
```
This class may hold a cached snapshot of a calendar, and changes in the calendar can easily be copied over
through the sync method.

To create a SynchronizableCalendarObjectCollection object, use calendar.objects(load_objects=True)

### Функции Synchronizable Calendar Object Collection

```bash
objects_by_url()
```
returns a dict of the contents of the SynchronizableCalendarObjectCollection, URLs -> objects

```bash
sync()
```
This method will contact the caldav server, request all changes from it, and sync up the collection

