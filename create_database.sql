CREATE TABLE Users (
    id INTEGER PRIMARY KEY
);

CREATE TABLE Movies (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    year_of_release INTEGER,
    GENRE VARCHAR(50),
    UserId INT,
    FOREIGN KEY (UserId) REFERENCES Users(id)
);