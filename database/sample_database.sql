DROP TABLE IF EXISTS Profiles_Dispositions;
DROP TABLE IF EXISTS Dispositions;
DROP TABLE IF EXISTS Profiles;
DROP TABLE IF EXISTS Users;

CREATE TABLE Profiles(
    profile_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    profile_name VARCHAR(255) NOT NULL,
	profile_type VARCHAR(255) NOT NULL,
	profile_breed VARCHAR(255) NOT NULL,
	profile_availability VARCHAR(255) NOT NULL,
	profile_news VARCHAR(255) NOT NULL,
	profile_description VARCHAR(255) NOT NULL,
	profile_image VARCHAR(255) NOT NULL
) ENGINE = InnoDB;

INSERT INTO Profiles(profile_name, profile_type, profile_breed, profile_availability, profile_news, profile_description, profile_image) 
VALUES 
    ("Layla", "Cat", "Siamese", "Available", "She just arrived at the shelter!", "Small size, long tail, white with brown paws", "siamese.jpg"),
    ("March", "Dog", "Golden Retriever", "Available", "Newly Available for adoption!","Large size, light golden fur", "golden.jpg"),
    ("Ram", "Other", "N/A", "Available", "He likes to sleep", "Small size, white goat", "goat.jpg"),
	("Luna", "Cat", "Persian", "Pending", "Just adopted!", "Small size, long tail, orange with black spots", "persian.jpg"),
	("Hammie", "Other", "Hamster", "Available", "He likes to stash food", "Small size, long haired, brown fur", "hamster.jpg"),
	("Buster", "Dog", "German Shepherd", "Not available", "Just adopted!", "Big size, tan fur", "gsd.jpg"),
	("Benji", "Dog", "Pomeranian", "Available", "Still available for adoption! He's a sweetheart", "Small size, black and white fur", "pom.jpg")
;

CREATE TABLE Dispositions (
    disposition_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    disposition_value VARCHAR(255) NOT NULL
) ENGINE = InnoDB;

INSERT INTO Dispositions(disposition_value) 
VALUES
    ("Good with animals"),
    ("Good with children"),
    ("Animal must be leashed at all times")
;

CREATE TABLE Profiles_Dispositions (
    profile_disposition_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    profile_id INT,
    disposition_id INT,
    FOREIGN KEY (profile_id) REFERENCES Profiles(profile_id),
    FOREIGN KEY (disposition_id) REFERENCES Dispositions(disposition_id)
) ENGINE = InnoDB;

INSERT INTO Profiles_Dispositions(profile_id, disposition_id) 
VALUES
    (1,1),
    (2,1),
    (3,1),
    (4,2),
    (4,3),
    (5,3),
    (6,2)
;

CREATE TABLE Users (
    user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_fname VARCHAR(255) NOT NULL,
	user_lname VARCHAR(255) NOT NULL,
	user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
	user_city VARCHAR(255) NOT NULL,
	user_state VARCHAR(255) NOT NULL,
	user_is_admin TINYINT NOT NULL
) ENGINE = InnoDB;

INSERT INTO Users(user_fname, user_lname, user_email, user_password, user_city, user_state, user_is_admin)
VALUES 
    ("Martha", "Smith", "martha.smith@email.com", SHA1("password1"), "Chicago", "Illinois", 1),
    ("Peter", "Williams", "peter.williams@email.com", SHA1("password2"), "San Francisco", "California", 0),
    ("Mark", "Brown", "mark.brown@email.com", SHA1("password3"), "Houston", "Texas", 1),
    ("Susan", "Davis", "susan.davis@email.com", SHA1("password4"), "Seattle", "Washington", 1),
    ("Joe", "Garcia", "joe.garcia@email.com", SHA1("password5"), "Springfield", "Masssachusetts", 0),
    ("Mary", "Jones", "mary.jones@email.com", SHA1("password6"), "Atlanta", "Georgia", 0),
    ("David", "Miller", "david.miller@email.com", SHA1("password7"), "Greenville", "South Carolina", 1)
;