import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "wardrobe.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            colors TEXT,
            seasons TEXT,
            occasions TEXT,
            brand TEXT,
            notes TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            item_ids TEXT,
            vibe TEXT,
            rating REAL DEFAULT 0,
            folder TEXT DEFAULT 'General',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_item(name, category, colors, seasons, occasions, brand, notes, image_path):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO items (name, category, colors, seasons, occasions, brand, notes, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, category, colors, seasons, occasions, brand, notes, image_path))
    conn.commit()
    item_id = c.lastrowid
    conn.close()
    return item_id


def get_all_items():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_item(item_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_item(item_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def update_item(item_id, name, category, colors, seasons, occasions, brand, notes):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE items SET name=?, category=?, colors=?, seasons=?, occasions=?, brand=?, notes=?
        WHERE id=?
    """, (name, category, colors, seasons, occasions, brand, notes, item_id))
    conn.commit()
    conn.close()


def save_outfit(name, item_ids, vibe, rating, folder, notes):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO outfits (name, item_ids, vibe, rating, folder, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, ",".join(str(i) for i in item_ids), vibe, rating, folder, notes))
    conn.commit()
    outfit_id = c.lastrowid
    conn.close()
    return outfit_id


def get_all_outfits():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM outfits ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_outfit_rating(outfit_id, rating):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE outfits SET rating=? WHERE id=?", (rating, outfit_id))
    conn.commit()
    conn.close()


def delete_outfit(outfit_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM outfits WHERE id=?", (outfit_id,))
    conn.commit()
    conn.close()


def get_folders():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT folder FROM outfits")
    rows = c.fetchall()
    conn.close()
    return [r["folder"] for r in rows]
