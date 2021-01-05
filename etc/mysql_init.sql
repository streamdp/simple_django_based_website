CREATE DATABASE IF NOT EXISTS django_db CHARACTER SET utf8;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'django_password';
GRANT ALL PRIVILEGES ON django_db . * TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
