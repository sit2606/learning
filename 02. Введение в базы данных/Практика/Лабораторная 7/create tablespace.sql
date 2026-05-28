CREATE TABLESPACE myts1 LOCATION 'D:/pg_ts1';
CREATE TABLESPACE myts2 LOCATION 'D:/pg_ts2';


CREATE DATABASE mydb
    OWNER postgres
    ENCODING 'UTF8'
    LC_COLLATE 'Russian_Russia.1251'
    LC_CTYPE 'Russian_Russia.1251'
    TABLESPACE myts1
    CONNECTION LIMIT 10
    IS_TEMPLATE false;
	
\c mydb


CREATE TABLE table1 (id INT PRIMARY KEY, data TEXT) TABLESPACE myts1;
CREATE TABLE table2 (id INT PRIMARY KEY, info TEXT) TABLESPACE pg_default;
ALTER TABLE table1 SET TABLESPACE pg_default;

SELECT 
    schemaname, 
    tablename, 
    tablespace
FROM pg_tables
WHERE tablename IN ('table1', 'table2')
ORDER BY tablename;