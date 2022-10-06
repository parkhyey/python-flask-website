-- Sample Data for testing
-- Drop tables if they exist
DROP TABLE IF EXISTS Profiles;

CREATE TABLE Profiles(
    profile_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    profile_name VARCHAR(255) NOT NULL,
	profile_type VARCHAR(255) NOT NULL
) ENGINE = InnoDB;

INSERT INTO Profiles(profile_name, profile_type) 
VALUES 
    ("Layla", "cat"),
    ("March", "dog"),
    ("Ram", "other")
;