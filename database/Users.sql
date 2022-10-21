-- Sample Data for testing
-- Drop tables if they exist
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_fname VARCHAR(255) NOT NULL,
	user_lname VARCHAR(255) NOT NULL,
	user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
	user_is_admin TINYINT NOT NULL
) ENGINE = InnoDB;

INSERT INTO Users(user_fname, user_lname, user_email, user_password, user_is_admin)
VALUES 
    ("Martha", "Smith", "martha.smith@email.com", SHA1("password1"), 1),
    ("Peter", "Williams", "peter.williams@email.com", SHA1("password2"), 0),
    ("Mark", "Brown", "mark.brown@email.com", SHA1("password3"), 1),
    ("Susan", "Davis", "susan.davis@email.com", SHA1("password4"), 1),
    ("Joe", "Garcia", "joe.garcia@email.com", SHA1("password5"), 0),
    ("Mary", "Jones", "mary.jones@email.com", SHA1("password6"), 0),
    ("David", "Miller", "david.miller@email.com", SHA1("password7"), 1)
;
