-- Sample Data for testing
-- Drop tables if they exist
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_fname VARCHAR(255) NOT NULL,
	user_lname VARCHAR(255) NOT NULL,
	user_email VARCHAR(255) NOT NULL,
	user_city VARCHAR(255) NOT NULL,
	user_state VARCHAR(255) NOT NULL,
	user_is_admin TINYINT(1) NOT NULL
) ENGINE = InnoDB;

INSERT INTO Users(user_fname, user_lname, user_email, user_city, user_state, user_is_admin)
VALUES 
    ("Martha", "Smith", "martha.smith@email.com", "Chicago", "Illinois", 1),
    ("Peter", "Williams", "peter.williams@email.com", "San Francisco", "California", 0),
    ("Mark", "Brown", "mark.brown@email.com", "Houston", "Texas", 1),
    ("Susan", "Davis", "susan.davis@email.com", "Seattle", "Washington", 1),
    ("Joe", "Garcia", "joe.garcia@email.com", "Springfield", "Masssachusetts", 0),
    ("Mary", "Jones", "mary.jones@email.com", "Atlanta", "Georgia", 0),
    ("David", "Miller", "david.miller@email.com", "Greenville", "South Carolina", 1)
;
