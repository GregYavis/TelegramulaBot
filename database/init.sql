CREATE DATABASE IF NOT EXISTS bot_backend;
CREATE DATABASE IF NOT EXISTS bot_finance;
CREATE USER 'bot'@'localhost' IDENTIFIED BY 'Khamul_password';
GRANT ALL PRIVILEGES ON * . * TO 'bot'@'localhost';
FLUSH PRIVILEGES;

USE bot_backend;
CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL,
    balance FLOAT,
    UNIQUE (user_id));

USE bot_backend;
CREATE TABLE IF NOT EXISTS categories (
    category VARCHAR(150),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users (user_id));

USE bot_finance;
CREATE TABLE IF NOT EXISTS expenses (
    category VARCHAR(150),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES bot_backend.users (user_id));