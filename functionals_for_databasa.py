import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()


def add_movie_to_db(user_id, name, year=None, genre=None):
    insert_query = f"INSERT INTO Movies (UserId, name, year_of_release, GENRE) VALUES (?, ?, ?, ?)"
    record_to_insert = user_id, name, year, genre
    cursor.execute(insert_query, record_to_insert)
    conn.commit()
    cursor.execute("SELECT max(id) FROM Movies")
    id_movie = cursor.fetchall()
    conn.commit()
    return id_movie[0][0]

def sort_movie(genre, user_id):
    cursor.execute("SELECT name FROM Movies WHERE GENRE = ? AND UserId = ?", (genre, user_id))
    res = cursor.fetchall()
    conn.commit()
    return res


def get_genre_in_db(user_id):
    cursor.execute("SELECT DISTINCT GENRE FROM Movies WHERE UserId = ? AND (GENRE NOT NULL)", (user_id, ))
    res = cursor.fetchall()
    conn.commit()
    return res


def add_like_to_db(move_id, val):
    cursor.execute("INSERT INTO Likes (MovieId, level_likes) VALUES (?, ?)", (move_id, val))
    conn.commit()
    return True


def get_list_of_5_movies(user_id):
    cursor.execute("SELECT name FROM Movies WHERE UserId = ? ORDER BY id DESC LIMIT 5 ", (user_id, ))
    res = cursor.fetchall()
    conn.commit()
    return res


def get_list_of_favorite_5_movies(user_id, way):
    cursor.execute("""SELECT m.name FROM Movies AS m
                   JOIN Likes AS l 
                   ON m.id = l.MovieId
                   WHERE m.UserId = ? AND  l.level_likes = ?
                   ORDER BY m.id DESC LIMIT 5 """, (user_id, way))
    res = cursor.fetchall()
    conn.commit()
    return res


def check_add_word(word):
    cursor.execute("SELECT id FROM Keywords WHERE words = ?", (word, ))
    id_keywords = cursor.fetchall()
    if not id_keywords:
        cursor.execute(""" INSERT INTO Keywords (words) VALUES (?) """, (word,))
        conn.commit()
        cursor.execute("SELECT max(id) FROM Keywords")
        id_keywords = cursor.fetchall()
    conn.commit()
    return id_keywords[0][0]


def add_to_movies_keywords(id_movie, id_keywords):
    cursor.execute("""INSERT INTO Movies_Keywords (id_movie, id_keyword) VALUES (?, ?) """,  (id_movie, id_keywords))
    conn.commit()
    return True


def get_movie_by_keywords(word):
    cursor.execute(""" SELECT m.name FROM Movies AS m 
                       JOIN Movies_Keywords AS mk
                       ON m.id = mk.id_movie
                       JOIN Keywords AS k
                       ON mk.id_keyword = k.id
                       WHERE k.words = ?    
    """, (word, ))
    res = cursor.fetchall()
    return res
