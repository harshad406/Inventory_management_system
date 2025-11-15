CREATE DATABASE inventory_db;
USE inventory_db;

CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2)
);