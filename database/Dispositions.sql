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