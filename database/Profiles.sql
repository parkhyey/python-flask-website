-- Sample Data for testing
-- Drop tables if they exist
DROP TABLE IF EXISTS Profiles;

CREATE TABLE Profiles(
    profile_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    profile_name VARCHAR(255) NOT NULL,
	profile_type VARCHAR(255) NOT NULL,
	profile_breed VARCHAR(255) NOT NULL,
	profile_disposition VARCHAR(255) NOT NULL,
	profile_availability VARCHAR(255) NOT NULL,
	profile_news VARCHAR(255) NOT NULL,
	profile_description VARCHAR(255) NOT NULL
) ENGINE = InnoDB;

INSERT INTO Profiles(profile_name, profile_type, profile_breed, profile_disposition, profile_availability, profile_news, profile_description) 
VALUES 
    ("Layla", "Cat", "Siamese", "Good with other animals", "Available", "Newly added!", "Small size, long tail, white with brown paws"),
    ("March", "Dog", "Golden Retriever", "Good with children", "Available", "Newly added!", "Large size, light golden fur"),
    ("Ram", "Other", "N/A", "Good with children", "Available", "Newly added!", "Small size, black goat"),
	("Luna", "Cat", "Himalayan", "Good with children", "Pending", "Newly added!", "Small size, long tail, orange with black spots"),
	("Hammie", "Other", "Hamster", "Good with children", "Available", "Newly added!", "Small size, long haired, brown fur"),
	("Buster", "Dog", "German Shepherd", "Good with other animals", "Not available", "Newly added!", "Big size, tan fur"),
	("Benji", "Dog", "Pomeranian", "Good with other animals", "Available", "Newly added!", "Small size, black and white fur")
;