CREATE DATABASE api_app;

USE api_app;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT,
    description TEXT DEFAULT NULL
);

CREATE TABLE product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES products (id)
);