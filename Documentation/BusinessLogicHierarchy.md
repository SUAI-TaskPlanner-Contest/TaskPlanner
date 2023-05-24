### **Описание созданных сущностей**
```
├── Entities
    ├── Task
    ├── Server
    ├── Label
    ├── Size
    ├── Priority
    ├── Type
    ├── Status
    
```

<details>
    <summary>
        <code> Task.py </code>
    </summary>
  
<br> Класс-сущность Task. Поля класса:

|     имя     | тип  |                         описание                          |
|:-----------:|:----:|:---------------------------------------------------------:|
|     id      | int  |              уникальный идентификатор задачи              |
|  server_id  | int  |             уникальный идентификатор сервера              |
|  parent_id  | int  |             идентификатор родительской задачи             |
|   dtstamp   | datetime |                   дата создания задачи                    |
|   dtstart   | datetime |                    дата начала задачи                     |
|     due     | datetime |                   дата окончания задачи                   |
|   summary   | text |                    наименование задачи                    |
| tech_status | int  | технический статус задачи (создана, удалена, изменена...) |
| sync_time | datetime |                      дата последней синхронизации           |
| last_mod | datetime |                      дата последнего изменения           |
| description | text |                      описание задачи                      |


</details>

<details>
    <summary>
        <code> Server.py </code>
    </summary>

| имя | тип  |             описание             |
|:---:|:----:|:--------------------------------:|
| id  | int  | уникальный идентификатор сервера |
| user_email  | text |        email пользователя        |
| user_password  | text | пароль пользователя от аккаунта  |
| server_uri  | text |         ссылка на сервер         |
| server_name   | text |         название сервера         |
| calendar_name    | text |        название календаря        |

</details>

<details>
    <summary>
        <code> Label.py </code>
    </summary>

|     имя     | тип |                  описание                  |
|:-----------:|:---:|:------------------------------------------:|
|     id      |int|   уникальный идентификатор уровня задачи   |
|   task_id   |int|      уникальный идентификатор задачи       |
| priority_id |int| уникальный идентификатор приоритета задачи |
|   size_id   |int|  уникальный идентификатор размера задачи   |
|   type_id   |int|    уникальный идентификатор типа задачи    |
|  status_id  |int|  уникальный идентификатор статуса задачи   |


</details>

<details>
    <summary>
        <code> Priority.py </code>
    </summary>

|     имя     | тип  |                  описание                  |
|:-----------:|:----:|:------------------------------------------:|
|     id      | int  | уникальный идентификатор приоритета задачи |
|   server_id   | int  |      уникальный идентификатор сервера      |
| name  | text |         название приоритета задачи         |

</details>

<details>
    <summary>
        <code> Size.py </code>
    </summary>

|     имя     | тип  |               описание                |
|:-----------:|:----:|:-------------------------------------:|
|     id      | int  | уникальный идентификатор типа размера |
|   server_id   | int  |   уникальный идентификатор сервера    |
| name  | text |     название типа размера задачи      |

</details>

<details>
    <summary>
        <code> Status.py </code>
    </summary>

|     имя     | тип  |                описание                 |
|:-----------:|:----:|:---------------------------------------:|
|     id      | int  | уникальный идентификатор статуса задачи |
|   server_id   | int  |    уникальный идентификатор сервера     |
| name  | text |         название статуса задачи         |

</details>

<details>
    <summary>
        <code> Type.py </code>
    </summary>

|     имя     | тип  |               описание               |
|:-----------:|:----:|:------------------------------------:|
|     id      | int  | уникальный идентификатор типа задачи |
|   server_id   | int  |   уникальный идентификатор сервера   |
| name  | text |         название типа задачи         |

</details>

<!--- Потенциально список можно расширить такими сущностями, как -->
    
<br>

### **Описание сервисов**

В проекте можно выделить следующие группы сервисов:

```
├── Services
    ├── TaskService
    ├── CalDavService
    ├── ServerService
```

<details>
    <summary>
        <code> TaskService.py </code>
    </summary>
<br>TaskService - скрывает в себе работу с локальной базой данных, а также валидацией данных.
Пример создания объекта TaskService:

```
    repo = TaskRepository[Server](session) # session - объект SqlAlchemy, используемый для взаимодействия с базой данных через сессию базы данных.
    task_service = TaskService(repo)
```
<br>
<br>
<details>
        <summary>
            <code> add </code>
        </summary>

<br>**Описание:**
<br> Метод производит валидацию данных, переводит время в формат utc и добавляет задачу в репозиторий.

**Входные параметры:**
- `item: Task` 

**Выходной параметр:** 
- `None`
<br>
<br>
</details>

<details>
        <summary>
            <code> add_all </code>
         </summary>

<br>**Описание:**
<br> Метод производит валидацию данных, переводит время в формат utc и добавляет список задач в репозиторий.

**Входные параметры:**
- `items: list[Task]`

**Выходной параметр:**    
- `None`

**Выбрасываемые исключения:**
- `Invalid('Невозможно добавить задачи')`
<br>
<br>
</details>

<details>
        <summary>
            <code> edit </code>
         </summary>

<br>**Описание:**
<br> Метод производит валадацию данных и изменяет задачу в репозитории.

**Входные параметры:**
- `item: Task`

**Выходной параметр:**    
- `None`
<br>
<br>
</details>
<details>
        <summary>
            <code> delete </code>
         </summary>

<br>**Описание:**
<br> Метод производит валидацию данных и удаляет задачу в репозитории.

**Входные параметры:**
- `item: Task`

**Выходной параметр:**    
- `None`
<br>
<br>
</details>
<details>
        <summary>
            <code> delete_by_id </code>
         </summary>

<br>**Описание:**
<br> Метод удаляет задачу в репозитории по id.

**Входные параметры:**
- `item_id: int`

**Выходной параметр:**    
- `None`

**Выбрасываемые исключения:**
- `Invalid('Невозможно удалить задачу')`
<br>
<br>
</details>
<details>
        <summary>
            <code> get_all </code>
         </summary>

<br>**Описание:**
<br> Метод переводит время в локальный формат и возвращает список всех задач.

**Входной параметр:**    
- `None`

**Выходной параметр:**    
- ` tasks: list[Task]`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_by_id </code>
         </summary>

<br>**Описание:**
<br> Метод переводит время в локальный формат и возвращает задачу по id.

**Входные параметры:**
- `item_id: int`

**Выходной параметр:**    
- `item: Task`

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть задачу')`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_many_by_ids </code>
         </summary>

<br>**Описание:**
<br> Метод переводит время в локальный формат и возвращает список задач, id которых входят в переданный список ids.

**Входные параметры:**
- `ids: list[int]`

**Выходной параметр:**    
- `tasks: list[Task] `

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть задачи')`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_all_by_server_id </code>
         </summary>

<br>**Описание:**
<br> Метод переводит время в локальный формат и возвращает все задачи с сервера по его id.

**Входные параметры:**
- `server_id: int`

**Выходной параметр:**    
- `tasks: list[Task] `

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть задачи')`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_children_by_parent_id </code>
         </summary>

<br>**Описание:**
<br> Метод переводит время в локальный формат и возвращает все подзадачи по родительскому id.

**Входные параметры:**
- `parent_id: int`

**Выходной параметр:**    
- `tasks: list[Task] `

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть задачи')`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_task_children_by_id </code>
         </summary>

<br>**Описание:**
<br> Метод переводит время в локальный формат и возвращает все подзадачи по id.

**Входные параметры:**
- `task_id: int`

**Выходной параметр:**    
- `tasks: list[Task]`

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть задачи')`
<br>
<br>
</details>

</details>

<details>
    <summary>
        <code> CalDavService.py </code>
    </summary>

<br>CalDavService - скрывает в себе работу с удаленным сервером по протоколу CalDAV.
<br>CalDavService автоматически создает календарь с таким же именем, если он не существует на сервере.
<details>
        <summary>
            <code> get_all_tasks </code>
         </summary>

<br>**Описание:**
<br> Метод возвращает все задачи календаря на сервере.

**Входные параметры:**
- `None`

**Выходной параметр:**    
- `tasks: list[Task]`
<br>
<br>
</details>
<details>
        <summary>
            <code> publish_task </code>
         </summary>

<br>**Описание:**
<br> Метод публикует переданную в него задачу и обновляет связанные с временем публикации параметры.

**Входные параметры:**
- `tasks: Task`

**Выходной параметр:**    
- `None` - если публикация успешна
- `existing_task: Task, task: Task` - если возник конфликт между версиями публикующейся задачи

**Выбрасываемые исключения:**
- `Publish exception: Unauthorized`
- `Update exception`
<br>
<br>
</details>

<details>
        <summary>
            <code> delete_task_by_int_id </code>
         </summary>

<br>**Описание:**
<br> Метод удаляет задачу по её id.

**Входные параметры:**
- `uid: int`

**Выходной параметр:**    
- `result: Bool` - если задача удалена True, иначе - False

**Выбрасываемые исключения:**
- `Delete exception: Unauthorized`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_task_by_id </code>
         </summary>
        
<br>**Описание:**
<br> Метод возвращает задачу по её id.

**Входные параметры:**
- `uid: int`

**Выходной параметр:**    
- `task: Task`

**Выбрасываемые ошибки:**
- `NotFoundError`
<br>
<br>
</details>


</details>

<details>
    <summary>
        <code> ServerService.py </code>
    </summary>
<br>ServerService - скрывает в себе работу с серверами в базе данных.
Пример создания объекта ServerService:

```
    repo = ServerRepository[Server](session) # session - объект SqlAlchemy, используемый для взаимодействия с базой данных через сессию базы данных.
    server_service = ServerService(repo, pincode) # pincode - заданная пользователем строка для шифрования данных.
```
<br>
<br>
<details>
        <summary>
            <code> add </code>
         </summary>
        
<br>**Описание:**
<br> Метод производит валидацию полученных данных, шифрует их и добавляет полученный сервер в БД.

**Входные параметры:**
- `item: Server`

**Выходной параметр:**    
- `None`
<br>
<br>
</details>
<details>
        <summary>
            <code> add_all </code>
         </summary>

<br>**Описание:**
<br> Метод производит валидацию полученных данных, шифрует их и добавляет полученный список серверов в БД.

**Входные параметры:**
- `items:  list[Server]`

**Выходной параметр:**    
- `None`

**Выбрасываемые исключения:**
- `Invalid('Невозможно добавить серверы')`
<br>
<br>
</details>
<details>
        <summary>
            <code> edit </code>
         </summary>
        
<br>**Описание:**
<br> Метод производит валидацию полученных данных, шифрует их и обновляет полученный сервер в БД.

**Входные параметры:**
- `item:  Server`

**Выходной параметр:**    
- `None`
<br>
<br>
</details>
<details>
        <summary>
            <code> delete </code>
         </summary>

<br>**Описание:**
<br> Метод производит валидацию полученных данных, шифрует их и удаляет сервер из БД.

**Входные параметры:**
- `item:  Server`

**Выходной параметр:**    
- `None`
<br>
<br>
</details>
<details>
        <summary>
            <code> delete_by_id </code>
         </summary>

<br>**Описание:**
<br> Метод удаляет сервер из БД по id.

**Входные параметры:**
- `item_id:  int`

**Выходной параметр:**    
- `None`

**Выбрасываемые исключения:**
- `Invalid('Невозможно удалить сервер')`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_all </code>
         </summary>

<br>**Описание:**
<br> Метод дешифрует данные и возвращает список серверов.

**Входные параметры:**
- `None`

**Выходной параметр:**    
- `items_decrypt: list[Server]`

<br>
<br>
</details>

<details>
        <summary>
            <code> get_by_id </code>
         </summary>

<br>**Описание:**
<br> Метод дешифрует данные и возвращает указанный по id сервер.

**Входные параметры:**
- `item_id: int`

**Выходной параметр:**    
- `item: Server`

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть сервер')`
<br>
<br>
</details>

<details>
        <summary>
            <code> get_many_by_ids </code>
         </summary>

<br>**Описание:**
<br> Метод дешифрует данные и возвращает список серверов по их ids.

**Входные параметры:**
- `objects_ids: list[Server]`

**Выходной параметр:**    
- `servers: list[Server]`

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть серверы')`
<br>
<br>
</details>
<details>
        <summary>
            <code> get_count </code>
         </summary>
        
<br>**Описание:**
<br> Метод дешифрует данные и возвращает число записей, соответствующих переданному email.

**Входные параметры:**
- `email: str`

**Выходной параметр:**    
- `count: int`

**Выбрасываемые исключения:**
- `Invalid('Невозможно открыть сервера')`
<br>
<br>
</details>
<details>
        <summary>
            <code> get_tasks </code>
         </summary>
        
<br>**Описание:**
<br> Метод возвращает список задач по id сервера, на котором они хранятся.

**Входные параметры:**
- `server_id: int`

**Выходной параметр:**    
- `tasks: list[Task] `

**Выбрасываемые исключения:**
- `Invalid("Невозможно открыть задачи").`
<br>
<br>
</details>
<details>
        <summary>
            <code> get_statuses </code>
         </summary>
        
<br>**Описание:**
<br> Метод возвращает список статусов, которые соответствуют определенному серверу.

**Входные параметры:**
- `server_id: int`

**Выходной параметр:**    
- `statuses: list[Status]`

**Выбрасываемые исключения:**
- `Invalid("Невозможно открыть список статусов")`
<br>
<br>
</details>
<details>
        <summary>
            <code>  get_sizes </code>
         </summary>
        
<br>**Описание:**
<br> Метод возвращает список размеров, которые соответствуют определенному серверу. 

**Входные параметры:**
- `server_id: int`

**Выходной параметр:**    
- `sizes: list[Size]`

**Выбрасываемые исключения:**
- `Invalid("Невозможно открыть список размеров")`
<br>
<br>
</details>
<details>
        <summary>
            <code>   get_priorities </code>
         </summary>

<br>**Описание:**
<br> Метод возвращает список приоритетов, которые соответствуют определенному серверу.

**Входные параметры:**
- `server_id: int`

**Выходной параметр:**    
- `priorities: list[Priority]`

**Выбрасываемые исключения:**
- `Invalid("Невозможно открыть список приоритетов")`
<br>
<br>
</details>
<details>
        <summary>
            <code>  get_types </code>
         </summary>
        
<br>**Описание:**
<br> Метод возвращает список типов задач, которые соответствуют определенному серверу.

**Входные параметры:**
- `server_id: int`

**Выходной параметр:**    
- `types: list[Type]`

**Выбрасываемые исключения:**
- `Invalid("Невозможно открыть список типов")`
<br>
<br>
</details>
</details>
<br>