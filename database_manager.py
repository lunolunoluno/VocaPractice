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
    

def insert_or_ignore_language(language_code: str, language: str) -> None:
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO language (language_code, language) VALUES (?, ?)",
            (language_code, language)
        )
        conn.commit()


def create_new_request() -> int:
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO request DEFAULT VALUES")

        request_id = cursor.lastrowid

        conn.commit()
    
    return request_id


def insert_sentence(english: str, translation: str, request_id: int, language_code: str) -> int:
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO sentence (english, translation, fk_request_id, fk_language_code) VALUES (?, ?, ?, ?)",
            (english, translation, request_id, language_code)
        )

        sentence_id = cursor.lastrowid

        conn.commit()
    
    return sentence_id


def link_vocab_to_request(term: str, meaning: str, type_: str, language_code: str, request_id: int) -> int:
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        # Check if term is already saved
        cursor.execute("""
            SELECT term_id 
            FROM vocabulary
            WHERE term = ? AND meaning = ? AND type = ? AND fk_language_code = ?
        """, (term, meaning, type_, language_code))

        row = cursor.fetchone()

        if row is not None:
            # Term already exists
            term_id = row[0]
        else:
            # Insert new term
            cursor.execute("""
                INSERT INTO vocabulary (term, meaning, type, fk_language_code)
                VALUES (?, ?, ?, ?)
            """, (term, meaning, type_, language_code))
            term_id = cursor.lastrowid
        

        cursor.execute("""
            INSERT INTO request_vocabulary (fk_request_id, fk_term_id)
            VALUES (?, ?)
        """, (request_id, term_id))

        conn.commit()
    
    return term_id


def get_sentence(sentence_id: int) -> dict:
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT english, translation, fk_language_code 
            FROM sentence
            WHERE sentence_id = ?
        """, (sentence_id,))

        row = cursor.fetchone()
        if row is not None:
            return {
                "english": row[0],
                "translation": row[1],
                "language_code": row[2]
            }

    return None


def get_request_vocab(request_id: int) -> dict:
    with sqlite3.connect(database_path) as conn:
        vocab = {}

        cursor = conn.cursor()

        cursor.execute("""
            SELECT fk_term_id 
            FROM request_vocabulary
            WHERE fk_request_id = ?
        """, (request_id,))

        for row in cursor.fetchall():
            cursor.execute("""
                SELECT term, meaning 
                FROM vocabulary
                WHERE term_id = ?
            """, (row[0],))

            term = cursor.fetchone()
            if term is not None:
                vocab[term[1]] = term[0] 
        
        return vocab
    return None

