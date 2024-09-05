CREATE DATABASE flask;
\c flask;
CREATE SCHEMA flask_app;
SET SEARCH_PATH TO flask_app;

CREATE TABLE Users(user_id int PRIMARY KEY not null, user_name varchar, age int, gender char(1)); 

