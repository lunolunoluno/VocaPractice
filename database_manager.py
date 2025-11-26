import sqlite3

from utils import get_all_languages

database_path = "./database.db"
database_sql_path = "./database.sql"


def create_database():
    with sqlite3.connect(database_path) as conn:
        # Create database
        cursor = conn.cursor()

        with open(database_sql_path, 'r') as sql_file:
            sql = sql_file.read()

        cursor.executescript(sql)

        conn.commit()

        # Add languages to the database
        for language_code, language in get_all_languages():
            cursor.execute(
                "INSERT OR IGNORE INTO language (language_code, language) VALUES (?, ?)",
                (language_code, language)
            )
        conn.commit()
    

