-- Sample Data for testing
-- Drop tables if they exist
DROP TABLE IF EXISTS Profiles_Dispositions;

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
