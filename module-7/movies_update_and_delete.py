"""
Sam Dirr
Module 7 Assignment - Movies Update and Delete
"""

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}


def show_films(cursor, title):
    cursor.execute("""
        SELECT
            film_name AS Name,
            film_director AS Director,
            genre_name AS Genre,
            studio_name AS Studio
        FROM film
            INNER JOIN genre
                ON film.genre_id = genre.genre_id
            INNER JOIN studio
                ON film.studio_id = studio.studio_id
    """)

    films = cursor.fetchall()

    print("\n-- {} --".format(title))

    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name: {}\nStudio Name: {}\n".format(
            film[0], film[1], film[2], film[3]
        ))


db = None
cursor = None

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    show_films(cursor, "DISPLAYING FILMS")

    cursor.execute("""
        INSERT INTO film (
            film_name,
            film_releaseDate,
            film_runtime,
            film_director,
            studio_id,
            genre_id
        )
        VALUES (
            'Halloween',
            2018,
            106,
            'David Gordon Green',
            (SELECT studio_id FROM studio WHERE studio_name = 'Blumhouse Productions'),
            (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
        )
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    cursor.execute("""
        UPDATE film
        SET genre_id = (
            SELECT genre_id
            FROM genre
            WHERE genre_name = 'Horror'
        )
        WHERE film_name = 'Alien'
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    cursor.execute("""
        DELETE FROM film
        WHERE film_name = 'Gladiator'
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password is invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")
    else:
        print(err)

finally:
    if cursor is not None:
        cursor.close()

    if db is not None and db.is_connected():
        db.close()
