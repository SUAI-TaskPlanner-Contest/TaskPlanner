# Инструкция по развертыванию Nextcloud
## 1. Рекомендации и требования для корректной работы Nextcloud
Подробнее с ними можно ознакомиться по ссылке:
https://portal.nextcloud.com/categories/Scalability/Deployment-recommendations
### 1.1 Рекомендации по выбору операционной системы, СУБД и веб-сервера.

![image](https://user-images.githubusercontent.com/78814540/230606501-6a30be6f-75fd-46c9-b9b3-500635ca3788.png)

Ссылка для скачивания образа Ubuntu 22.04.2 LTS (Jammy Jellyfish): https://releases.ubuntu.com/jammy/
### 1.2. Рекомендации для корректной работы Nextcloud
Nextcloud требуется минимум 128 МБ ОЗУ на процесс, разработчики рекомендуют минимум 512 МБ ОЗУ на процесс.
Для нормальной работы Nextcloud требуется 64-битный процессор, ОС и PHP.

**Настройка виртуальной машины (минимальные требования)**

При выключенной машине зайти в:
- Настроить -> Дисплей -> Видеопамять - 128 мб;
- Настроить -> Система -> Процессоры - 4.

## 2. Шаги по развертыванию Nextcloud
Следующие шаги были осуществлены на ОС Ubuntu 23.04 (Lunar Lobster) в VirtualBox

Ссылка для скачивания образа: https://cdimage.ubuntu.com/daily-live/current/

![image](https://user-images.githubusercontent.com/78814540/230652975-766f47c5-fc57-415e-b4fe-64d5886aa7b9.png)

### 2.1 Обновите систему
❗Выполнение всех команд осуществляется через терминал Ubuntu❗

Перед началом установки обновите систему до последней версии:
```
sudo apt update && sudo apt upgrade -y
```

### 2.2 Установите LAMP
Nextcloud требует работающую LAMP-среду, которая включает в себя Apache, MySQL и PHP (Потребуется около 274Мб). Для установки LAMP на Ubuntu 23.04 выполните следующую команду (выполнение команды может занять длительное время на ВМ, которой выделено мало ресурсов):
```
sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql php-gd php-curl php-zip php-mbstring php-intl php-xml php-json
```
После установки LAMP проверьте, что Apache и MySQL запущены:
```
sudo systemctl status apache2
```
```
sudo systemctl status mysql
```
![image](https://user-images.githubusercontent.com/78814540/230653378-9ad37b67-c1a8-4fd2-8d6f-23bb9fe6e99c.png)
![image](https://user-images.githubusercontent.com/78814540/230653442-59c7cbfd-f7ca-4246-a94a-6ac703180d5f.png)

В случае, если Apache и MySQL не запустились автоматически, можно использовать команды:
- Для Apache:
```
sudo systemctl enable apache2
```
- Для MySQL:
```
sudo systemctl enable mysql
```
Эти команды добавят необходимые ссылки в системные директории, чтобы сервисы Apache2 и MySQL автоматически запускались при загрузке системы.
После выполнения команды enable, вы можете использовать команду systemctl status, чтобы убедиться, что сервисы Apache2 и MySQL теперь имеют статус enabled.

### 2.3 Создайте базу данных MySQL для Nextcloud
Запустите командную строку MySQL в режиме администратора (root) с запросом пароля:
```
sudo mysql -u root -p
```
Введите пароль root для MySQL и выполните следующие команды:

1. Следующая команда создает новую базу данных с названием "nextcloud":
```
CREATE DATABASE nextcloud;
```
2. Следующая команда создает нового пользователя базы данных "admin" с паролем "admin". '@localhost' указывает, что пользователь сможет подключаться только с того же компьютера (localhost), где база данных запущена:
```
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
```
3. Следующая команда предоставляет пользователю "admin" все права на все таблицы в базе данных "nextcloud". '.*' указывает, что должны быть предоставлены все права на все таблицы базы данных "nextcloud":
```
GRANT ALL PRIVILEGES ON nextcloud.* TO 'admin'@'localhost';
```
4. Следующая команда перезагружает привилегии базы данных MySQL, чтобы изменения, внесенные в предыдущие команды, вступили в силу:
```
FLUSH PRIVILEGES;
```
5. Следующая команда завершает сеанс работы в командной строке MySQL и выходит из нее.
```
EXIT;
```
❗❗❗**Следующую команду не нужно использовать при развертывании, но она пригодится в будущем**❗❗❗

Для подключения к базе данных MySQL от имени пользователя 'admin', вы можно использовать следующую команду:
```
mysql -u admin -p nextcloud
```
При выполнении этой команды вы будете подключены к базе данных "nextcloud" от имени пользователя "admin". Система запросит вас ввести пароль для пользователя "admin", который вы указали при создании пользователя.

### 2.4 Установите последнюю версию Nextcloud с официального сайта
Загрузите архив с последней версией Nextcloud с помощью программы wget:
```
wget https://download.nextcloud.com/server/releases/latest.tar.bz2
```
Извлеките содержимое архива latest.tar.bz2 в директорию /var/www/html/ с помощью утилиты tar:
```
sudo tar -xjf latest.tar.bz2 -C /var/www/html/
```
Измените владельца и группу для всех файлов и директорий в директории /var/www/html/nextcloud/ на пользователя www-data и группу www-data. Когда команда выполнена, пользователь и группа для всех файлов и поддиректорий в /var/www/html/nextcloud/ будут изменены на www-data:www-data. Это может быть полезно, чтобы обеспечить корректную работу веб-приложений, которые работают с файлами и директориями в этой директории, таких как Nextcloud:
```
sudo chown -R www-data:www-data /var/www/html/nextcloud/
```
### 2.5 Настройте Apache
Создайте файл конфигурации Apache для Nextcloud:
```
sudo nano /etc/apache2/sites-available/nextcloud.conf
```
Добавьте следующий текст:
```
<VirtualHost *:80>
     ServerAdmin admin@example.com
     DocumentRoot /var/www/html/nextcloud/
     ServerName localhost

     <Directory /var/www/html/nextcloud/>
        Options +FollowSymlinks
        AllowOverride All
        Require all granted
          <IfModule mod_dav.c>
            Dav off
          </IfModule>
        SetEnv HOME /var/www/html/nextcloud
        SetEnv HTTP_HOME /var/www/html/nextcloud
     </Directory>

     ErrorLog ${APACHE_LOG_DIR}/error.log
     CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
```
Замените ServerAdmin и ServerName на свой домен. Сохраните и закройте файл.
Активируйте новый виртуальный хост и перезапустите Apache:
```
sudo a2ensite nextcloud.conf
```
```
sudo systemctl reload apache2
```
### 2.6 Завершите установку через веб-интерфейс
Откройте веб-браузер и перейдите на свой домен (например, example.com или localhost).

![image](https://user-images.githubusercontent.com/78814540/230659983-ebf33b4f-3a85-498e-86c9-3c8d24ed9ee8.png)

Порядок действий для завершения установки через веб-интерфейс:
1. Введите домен localhost (Указывался в пункте 2.5 Настройте Apache) в адресную строку браузера и нажмите Enter. Вы увидите страницу приветствия Nextcloud.

2. На странице приветствия нажмите на кнопку "Create an admin account" (Создать учетную запись администратора) для создания административной учетной записи.

3. Введите имя пользователя и пароль для администратора, затем нажмите на кнопку "Create account" (Создать учетную запись).

4. Выберите местоположение хранилища данных.

5. Затем выберите базу данных MySQL и введите параметры подключения к базе данных. Введите имя пользователя, пароль и название базы данных, которую вы создали (пункт 2.3 Создайте базу данных MySQL для Nextcloud).

6. Нажмите на кнопку "Finish setup" (Завершить установку), чтобы завершить установку.

Теперь у вас есть Nextcloud на Ubuntu 23.04!
