# Инструкция по развертыванию NextCloud
## 1. Рекомендации и требования для корректной работы NextCloud
Подробнее с ними можно ознакомиться по ссылке:
https://portal.nextcloud.com/categories/Scalability/Deployment-recommendations
### 1.1 Рекомендации по выбору операционной системы, СУБД и веб-сервера.

![image](https://user-images.githubusercontent.com/78814540/230606501-6a30be6f-75fd-46c9-b9b3-500635ca3788.png)

### 1.2. Архитектура процессора и ОС. Память
Для нормальной работы Nextcloud требуется 64-битный процессор, ОС и PHP.

Nextcloud требуется минимум 128 МБ ОЗУ на процесс, разработчики рекомендуют минимум 512 МБ ОЗУ на процесс.

### 1.3 Требования к базе данных для MySQL/MariaDB
В настоящее время существуют следующие требования, если Nextcloud используется вместе с базой данных MySQL/MariaDB:
* Механизм хранения InnoDB (MyISAM не поддерживается)
* Уровень изоляции транзакций «READ COMMITTED» (см. Уровень изоляции транзакций базы данных «READ COMMITTED»)
* Отключено или BINLOG_FORMAT = ROW настроено ведение двоичного журнала (см.: https://dev.mysql.com/doc/refman/5.7/en/binary-log-formats.html)
* Информацию для поддержки Emoji (UTF8, 4 байта) см. в разделе Включение поддержки MySQL 4 байта.

### 1.4 Рекомендации по выбору ОС клиента
* Windows 10+
* macOS Lion (10.14)+ (только 64-разрядная версия)
* Linux (только 64-разрядная версия) Должен работать в любом дистрибутиве, более новом, чем Ubuntu 18.04, с нашим официальным пакетом AppImage.

### 1.5 Рекомендации по выбору браузера
- Mozilla Firefox
- Google Chrome/Chromium
- Apple Safari

## 2. Шаги по развертыванию NextCloud
Следующие шаги были осуществлены на ОС Ubuntu 23.04 (Lunar Lobster) в VirtualBox

![image](https://user-images.githubusercontent.com/78814540/230652975-766f47c5-fc57-415e-b4fe-64d5886aa7b9.png)

### 2.1 Обновите систему
Перед началом установки обновите систему до последней версии:
> sudo apt update && sudo apt upgrade -y


### 2.2 Установите LAMP
NextCloud требует работающую LAMP-среду, которая включает в себя Apache, MySQL и PHP (Потребуется около 274Мб). Для установки LAMP на Ubuntu 22.10 выполните следующую команду:
> sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql php-gd php-curl php-zip php-mbstring php-intl php-xml php-json

После установки LAMP проверьте, что Apache и MySQL запущены:
> sudo systemctl status apache2

> sudo systemctl status mysql

![image](https://user-images.githubusercontent.com/78814540/230653378-9ad37b67-c1a8-4fd2-8d6f-23bb9fe6e99c.png)
![image](https://user-images.githubusercontent.com/78814540/230653442-59c7cbfd-f7ca-4246-a94a-6ac703180d5f.png)


### 2.3 Создайте базу данных MySQL
Создайте базу данных MySQL для NextCloud:
> sudo mysql -u root -p

Введите пароль root для MySQL и выполните следующие команды:
> CREATE DATABASE nextcloud;
> 
> CREATE USER 'nextclouduser'@'localhost' IDENTIFIED BY 'password';
> 
> GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextclouduser'@'localhost';
> 
> FLUSH PRIVILEGES;
> 
> EXIT;

Вместо 'password' используйте пароль, который вы хотите использовать для пользователя nextclouduser.

### 2.4 Установите NextCloud
Скачайте и установите последнюю версию NextCloud с официального сайта (около 142Мб):
> wget https://download.nextcloud.com/server/releases/latest.tar.bz2
> 
> sudo tar -xjf latest.tar.bz2 -C /var/www/html/
> 
> sudo chown -R www-data:www-data /var/www/html/nextcloud/

### 2.5 Настройте Apache
Создайте файл конфигурации Apache для NextCloud:
> sudo nano /etc/apache2/sites-available/nextcloud.conf

Добавьте следующий текст:

     <VirtualHost *:80>
          ServerAdmin admin@example.com
          DocumentRoot /var/www/html/nextcloud/
          ServerName example.com

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

Я делал для localhost, поэтому nextcloud.conf выглядел следующим образом:

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

Замените ServerAdmin и ServerName на свой домен. Сохраните и закройте файл.
Активируйте новый виртуальный хост и перезапустите Apache:
> sudo a2ensite nextcloud.conf

> sudo systemctl reload apache2

### 2.6 Завершите установку через веб-интерфейс
Откройте веб-браузер и перейдите на свой домен (например, example.com или localhost).

![image](https://user-images.githubusercontent.com/78814540/230659983-ebf33b4f-3a85-498e-86c9-3c8d24ed9ee8.png)

Подробная инструкция для завершения установки через веб-интерфейс:
1. Введите свой домен в адресную строку браузера и нажмите Enter. Вы увидите страницу приветствия NextCloud.

2. На странице приветствия нажмите на кнопку "Create an admin account" (Создать учетную запись администратора) для создания административной учетной записи.

3. Введите имя пользователя и пароль для администратора, затем нажмите на кнопку "Create account" (Создать учетную запись).

4. На следующей странице установки выберите местоположение хранилища данных. Вы можете выбрать локальное хранилище или настроить внешнее хранилище, такое как Amazon S3 или Dropbox.

5. Затем выберите базу данных MySQL и введите параметры подключения к базе данных. Введите имя пользователя, пароль и название базы данных, которую вы создали на шаге 3.

6. Нажмите на кнопку "Finish setup" (Завершить установку), чтобы завершить установку.

7. После завершения установки вы будете перенаправлены на страницу входа. Введите имя пользователя и пароль администратора, чтобы войти в панель управления NextCloud.

Теперь у вас есть NextCloud на Ubuntu 22.04!
