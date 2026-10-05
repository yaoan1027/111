-- 建立資料庫與銷售記錄資料表
CREATE DATABASE IF NOT EXISTS `sales_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `sales_db`;

DROP TABLE IF EXISTS `sales_records`;

CREATE TABLE `sales_records` (
    `sale_id` INT NOT NULL,
    `sale_date` DATE NOT NULL,
    `product_id` INT NOT NULL,
    `product_name` VARCHAR(50) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `channel` VARCHAR(50) NOT NULL,
    `unit_price` INT NOT NULL,
    `quantity` INT NOT NULL,
    `returned_quantity` INT NOT NULL,
    PRIMARY KEY (`sale_id`),
    INDEX `idx_date` (`sale_date`),
    INDEX `idx_product` (`product_id`),
    INDEX `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 建立方便查詢淨額的 VIEW
CREATE OR REPLACE VIEW `v_sales_summary` AS
SELECT 
    sale_id,
    sale_date,
    product_id,
    product_name,
    category,
    channel,
    unit_price,
    quantity,
    returned_quantity,
    (quantity - returned_quantity) AS net_quantity,
    (unit_price * (quantity - returned_quantity)) AS net_revenue
FROM sales_records;
