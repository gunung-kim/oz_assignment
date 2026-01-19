-- 데이터베이스 생성
CREATE DATABASE fishbread_db;
-- users 테이블 생성
USE fishbread_db;
CREATE TABLE users (
user_id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255),
age INT NOT NULL,
email VARCHAR(100),
is_business BOOLEAN DEFAULT False
);
-- orders 테이블 생성
CREATE TABLE orders (
order_id INT PRIMARY KEY AUTO_INCREMENT,
user_id INT,
order_date DATE,
AMOUNT DECIMAL(10,2),
FOREIGN (user_id) REFERENCES users(user_id)
);
-- inventory 테이블 생성
CREATE TABLE inventory(
item_id INT PRIMARY KEY AUTO_INCREMENT,
item_name VARCHAR(255) NOT NULL,
quantity INT NOT NULL
);
-- sales 테이블 생성
CREATE TABLE sales(
sale_id INT PRIMARY KEY AUTO_INCREMENT,
order_id INT,
item_id INT,
quantity_sold INT NOT NULL,
FOREIGN (order_id) REFERENCES orders(id)
FOREIGN (item_id) REFERENCES inventory(id)
);
-- daily_sales 생성
CREATE TABLE daily_sales(
date DATE PRIMARY KEY,
total_sales DECIMAL(10,2) NOT NULL
);