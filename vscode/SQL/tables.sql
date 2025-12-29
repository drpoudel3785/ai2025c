use ai2025c;

CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    role VARCHAR(5) DEFAULT 'guest',
    status TINYINT(1) DEFAULT 0
);

select * from users;
desc users;


CREATE TABLE user_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    fullname VARCHAR(255) DEFAULT NULL,
    profile_picture VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_profile_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

select * from user_profile;
desc user_profile;

truncate table user_profile;