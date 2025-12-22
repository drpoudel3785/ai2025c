CREATE DATABASE ai2025c;

USE ai2025c;

show tables;
CREATE TABLE users(
id INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(50) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL,
email VARCHAR(40) NOT NULL UNIQUE,
role VARCHAR(5) DEFAULT 'guest',
status TINYINT(1) DEFAULT 0
);


CREATE TABLE department (
departmentid INT PRIMARY KEY AUTO_INCREMENT,
departmentname VARCHAR(50) NOT NULL UNIQUE,
hod VARCHAR(50) NOT NULL,
officeroom varchar(50) NOT NULL
);

CREATE TABLE program
(
programid INT PRIMARY KEY AUTO_INCREMENT,
programname VARCHAR(50) NOT NULL UNIQUE,
departmentid INT NOT NULL,
CONSTRAINT fk_departmentid FOREIGN KEY (departmentid) REFERENCES department(departmentid)
);

SELECT * from department;

INSERT INTO department(departmentname, hod, officeroom) VALUES('DS','Dharma Raj Poudel',103);
desc program;

INSERT INTO program(programname, departmentid) VALUES('Game Development',105);


INSERT INTO program(departmentname, hod, officeroom) VALUES('DS','Dharma Raj Poudel',103);

INSERT INTO department(departmentname, hod, officeroom) 
VALUES
('CS','Saroj Sharma',101),
('Computing','Anita Rana',102);



CREATE TABLE student
(
studentid INT PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(50) NOT NULL,
lastname VARCHAR(50) NOT NULL,
dob date NULL,
email VARCHAR(50) NULL UNIQUE,users
phone VARCHAR(10) NOT NULL UNIQUE,
programid INT NOT NULL,
CONSTRAINT fk_programid FOREIGN KEY (programid) REFERENCES program(programid)
);

desc users;

#comments
ALTER TABLE users 
RENAME COLUMN username TO usernames;

#adding the created_at on users table
ALTER TAble users ADD salry double;
ALTER TABLE users RENAME COLUMN salry TO salary;
desc users;
ALTER TABLE users ADD COLUMN deleteme VARCHAR(4) AFTER role;
desc users;
ALTER TABLE users DROP COLUMN deleteme;


SELECT email as Email, role, usernames as UserName from users;

SELECT * from users;

select * from department;
#selecting all departmetn with asc by hod
SELECT * FROM department ORDER by hod ASC;



use ai2025c;
