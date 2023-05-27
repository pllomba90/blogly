DROP DATABASE IF EXISTS blogly_db;

CREATE DATABASE blogly_db;

\c blogly_db

CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    image_url VARCHAR);

INSERT INTO users (first_name, last_name)
VALUES
('Bob', 'Loblaw'),
('Kathy', 'Poland'),
('Hugh', 'Janus');