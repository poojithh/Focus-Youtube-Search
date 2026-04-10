import sqlite3

conn = sqlite3.connect("database/user_data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT
)
""")

conn.commit()


def save_search(query):
    cursor.execute(
        "INSERT INTO history(query) VALUES (?)",
        (query,)
    )
    conn.commit()


# TEST (optional)
if __name__ == "__main__":
    save_search("test query")
    print("Database working")

def get_history():
    cursor.execute("SELECT query FROM history ORDER BY id DESC LIMIT 10")
    return cursor.fetchall()
    