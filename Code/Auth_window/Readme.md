# Изменения вносятся в class AuthWindowHandler(QObject))
## Пример реализации нажатия на "Продолжить локально"
```
@pyqtSlot()
    def localareaClicked(self):
        print("Local area clicked")
```
![image](https://github.com/SUAI-TaskPlanner-Contest/TaskPlanner/assets/78814540/f0561ffd-87da-42d3-aa21-3344e36ea8b8)

## Пример реализации нажатия на "Войти"
```
@pyqtSlot(str, str, str, str)
def loginClicked(self, login, password, calendarAddress, serverLink):
    print("Login:", login)
    print("Password:", password)
    print("Calendar Address:", calendarAddress)
    print("Server Link:", serverLink)
```
![image](https://github.com/SUAI-TaskPlanner-Contest/TaskPlanner/assets/78814540/4584aa61-eedd-407e-8ca6-46033cd6d9c5)
# Изменения вносятся в if __name__ == "__main__":
## Пример обновления текста ошибки
```
AuthWindowHandler.errorText = "Новый текст ошибки"
```
