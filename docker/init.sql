CREATE DATABASE IF NOT EXISTS dwh_mart;
USE dwh_mart;

CREATE TABLE dim_customers (
    customer_key INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);

CREATE TABLE dim_products (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_date DATE NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    quantity INT NOT NULL,
    gross_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL,
    is_returned TINYINT(1) DEFAULT 0,
    FOREIGN KEY (customer_key) REFERENCES dim_customers(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_products(product_key)
);

INSERT INTO dim_customers VALUES
(1, 'SIA Alfa', 'Enterprise', 'Latvia'),
(2, 'UAB Beta', 'SMB', 'Lithuania'),
(3, 'OU Gamma', 'Enterprise', 'Estonia');

INSERT INTO dim_products VALUES
(101, 'Cloud DWH Licence', 'Software'),
(102, 'ETL Connector Pack', 'Software'),
(103, 'Architecture Audit', 'Consulting');

INSERT INTO fact_sales (sale_date, customer_key, product_key, quantity, gross_amount, discount_amount, is_returned) VALUES
('2026-10-01', 1, 101, 2, 2000.00, 200.00, 0),
('2026-10-05', 2, 102, 5, 1500.00, 0.00, 0),
('2026-10-10', 1, 103, 1, 3000.00, 300.00, 1),
('2026-11-02', 3, 101, 3, 3000.00, 150.00, 0),
('2026-11-15', 2, 103, 1, 3000.00, 0.00, 0);

-- Principle of Least Privilege: DB lietotājs ar tikai SELECT tiesībām
CREATE USER 'ai_reader'@'%' IDENTIFIED BY 'readonly_pass_123';
GRANT SELECT ON dwh_mart.* TO 'ai_reader'@'%';
FLUSH PRIVILEGES;
