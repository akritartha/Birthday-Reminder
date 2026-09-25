from db import connect_db, create_table, add_to_db

if __name__ == "__main__":
    conn, cursor = connect_db()
    create_table(conn, cursor)
    add_to_db(conn, cursor)