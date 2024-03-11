import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()


def add_movie_to_db(user_id, name, year=None, genre=None):
    insert_query = f"INSERT INTO Movies (UserId, name, year_of_release, GENRE) VALUES (?, ?, ?, ?)"
    record_to_insert = user_id, name, year, genre
    cursor.execute(insert_query, record_to_insert)
    conn.commit()
    return True

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
