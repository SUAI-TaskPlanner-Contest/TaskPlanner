# Способы представления иерархичных структур

## Materialazed Path

Допустим, что мы имеем следующую иерархичную структуру:

```
├── Введение
│   ├── Наименование программы
│   ├── Основание для разработки
├── Основание для разработки
│   ├── Основание для проведения разработки
│   ├── ...
|── ...
```

Тогда, в виде таблицы ее можно представить следующим образом:

| id            |     number      |  path         | name          |
|:-------------:|:---------------:|:-------------:|:-------------:|
| 1 | 1 | 1     | Введение |
| 2 | 1 | 1.1   | Наименование программы |
| 3 | 2 | 1.2   | Краткая характеристика области применения |
| 4 | 2 | 2     | Основание для разработки |
| 5 | 1 | 2.1   | Основание для проведения разработки |

### Операции для работы с таблицей
#### 1. Взятие всех потомков
```
SELECT WHERE path LIKE '1.1.%' ORDER BY path
```

#### 2. Добавление
1. В конец

Добавление в конец происходит без совершения дополнительных операций

2. В середину

Необходимо увеличить значения number и path всем задачам, следующим за только что вставленной. Теоретически, добавление в середину нам не должно понадобиться

#### 3. Удаление
1. С конца

Удаление с конца происходит без совершения дополнительных операций

2. Из середины

Аналогичная ситуация, как и в добавлении, но теперь нам необходимо уменьшить number и path всем задачам, следующим за удаленной.

#### 4. Изменение/Поиск

Не вижу возможных проблем из-за иерархичного представления в этих операциях.

### Возможные проблемы

Из обнаруженных мною проблем (вообще-то другими людьми...), при наличии например списка задач с такими path: 1.1, 1.2, 1.10, запрос из раздела "Взятие всех потомков" вернет результат:

> 1.1, 1.10, 1.2

Решением пробемы может быть оценка количества записей, которые может хранить одна таблица задач, и увеличение количества десятков в path, например:

> 1000.1001, 1000.1002, 1000.1010.

### Выводы
Простая структура для понимания, которая позволяет быстро загрузить всех потомков, отобразить их. Все данные хранятся отсортированными. Простые операции для изменения/поиска. Из минусов - необходимо проводить дополнительные операции при удалении/добавлении в середину.
