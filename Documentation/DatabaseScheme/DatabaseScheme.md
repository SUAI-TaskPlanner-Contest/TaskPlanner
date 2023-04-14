![Схема базы данных](Images/db_scheme.svg)
## Уточнения по таблице Task
Каждая задача должна соответствовать сущности iCalendar (сущность VTODO) и обязательно иметь два атрибута
1. UID - уникальный идентификатор задачи (передается с сервера календарей)
2. dtstamp - дата создания задачи

Помимо обязательных атрибутов есть ряд атрибутов, которое нужны согласно [ТЗ](https://github.com/SUAI-TaskPlanner-Contest/TaskPlanner/blob/15-create-database/Documentation/TechTask.md)
1. dtstart - дата начала задачи
2. due - срок выполнения задачи
3. category - категория задачи
4. summary - наименование задачи
5. status - статус задачи (например требуется какое-то действие)
6. technical_status - технический статус задачи (например, сделана, обновлена и тд)
7. description - описание задачи

Также нужны атрибуты для создания иерархии задачи ([подробнее тут](https://github.com/SUAI-TaskPlanner-Contest/TaskPlanner/blob/15-create-database/Documentation/DatabaseReaserch/Database.md)):
1. number - номер задачи
2. path - путь из номеров задач до текущей

## Хранение даты и времени
Атрибуты dtstamp, dtstart, due имеют формат: YYYY-MM-DDTHH:MM:SS (или YYYY-MM-DDTHH:MM:SSZ, если используется абсолютное время) \
Например, 13:00 09.07.2007 по времени UTC - 20070709T130000Z
