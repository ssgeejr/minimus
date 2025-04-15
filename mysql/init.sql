-- Create the database if not already present
CREATE DATABASE IF NOT EXISTS minimus;
USE minimus;

-- Drop the table if it exists (for idempotency/testing)
DROP TABLE IF EXISTS userbase;

-- Create the userbase table
CREATE TABLE userbase (
    userid INT AUTO_INCREMENT PRIMARY KEY,
    real_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(50),
    company_name VARCHAR(255),
    keyhash CHAR(32) NOT NULL,
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS generate_hash;

-- Create the trigger
DELIMITER $$

CREATE TRIGGER generate_hash
BEFORE INSERT ON userbase
FOR EACH ROW
BEGIN
    SET NEW.keyhash = MD5(NOW());
END$$

DELIMITER ;


INSERT INTO userbase (real_name, email, phone_number, company_name)
VALUES (
    'Spongebob Squarepants',
    'spongebob@bikinibottom.com',
    '123-456-7890',
    'Krusty Krab'
);