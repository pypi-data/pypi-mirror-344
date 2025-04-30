# syntaxmatrix/db.py
from datetime import datetime
import sqlite3
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "syntaxmatrix.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            name TEXT PRIMARY KEY,
            content TEXT
        )
    """)

    # Create table for pdf_chunks for the admin files
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pdf_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            chunk_index INTEGER,
            chunk_text TEXT,
            processed_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_pages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM pages")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def add_page(name, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pages (name, content) VALUES (?, ?)", (name, content))
    conn.commit()
    conn.close()

def update_page(old_name, new_name, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE pages SET name = ?, content = ? WHERE name = ?", (new_name, content, old_name))
    conn.commit()
    conn.close()

def delete_page(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pages WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# ***************************************
# PDF Chunk Table Functions
# ***************************************
# These functions manage the pdf_chunks table in the database.
def init_pdf_chunks_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pdf_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_pdf_chunk(file_name: str, chunk_index: int, chunk_text: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO pdf_chunks (file_name, chunk_index, chunk_text) VALUES (?, ?, ?)",
        (file_name, chunk_index, chunk_text)
    )
    conn.commit()
    conn.close()

def get_pdf_chunks(file_name: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if file_name:
        cursor.execute(
            "SELECT chunk_index, chunk_text FROM pdf_chunks WHERE file_name = ? ORDER BY chunk_index",
            (file_name,)
        )
    else:
        cursor.execute(
            "SELECT file_name, chunk_index, chunk_text FROM pdf_chunks ORDER BY file_name, chunk_index"
        )
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_pdf_chunk(chunk_id: int, new_chunk_text: str):
    """
    Updates the chunk_text of a PDF chunk record identified by chunk_id.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pdf_chunks
        SET chunk_text = ?
        WHERE id = ?
    """, (new_chunk_text, chunk_id))
    conn.commit()
    conn.close()

def delete_pdf_chunks(file_name):
    """
    Delete all chunks associated with the given PDF file name.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "DELETE FROM pdf_chunks WHERE file_name = ?",
        (file_name,)
    )
    conn.commit()
    conn.close()
