CREATE TABLE Profiles_Dispositions (
    profile_disposition_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    profile_id INT,
    disposition_id INT,
    FOREIGN KEY (profile_id) REFERENCES Profiles(profile_id),
    FOREIGN KEY (disposition_id) REFERENCES Dispositions(disposition_id)
) ENGINE = InnoDB;

