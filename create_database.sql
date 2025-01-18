CREATE TABLE Users (
    id INTEGER PRIMARY KEY
);

CREATE TABLE Movies (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    year_of_release INTEGER,
    GENRE VARCHAR(50),
    UserId INT,
    time_add TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES Users(id)

);

CREATE TABLE Likes (
    id INTEGER PRIMARY KEY,
    level_likes INTEGER,
    MovieId INT,
    FOREIGN KEY (MovieId) REFERENCES Movies(id)

);

CREATE TABLE Keywords (
    id INTEGER PRIMARY KEY,
    [words] VARCHAR(100)
);

CREATE TABLE Movies_Keywords (
    id_movie INT,
    id_keyword INT,
    FOREIGN KEY (id_movie) REFERENCES Movies(id),
    FOREIGN KEY (id_keyword) REFERENCES Keywords(id)
);



