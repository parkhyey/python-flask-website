-- Sample Data for testing
-- Drop tables if they exist
DROP TABLE IF EXISTS Profiles;

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