import sqlite3
import sys
import nepali_datetime


def connect_db():
    conn = sqlite3.connect("birthday.db")
    cursor = conn.cursor()
    return conn, cursor


def create_table(conn, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Reminder ("
        "Id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "Name TEXT NOT NULL,"
        "Birthday TEXT NOT NULL,"
        "Days_Remaining TEXT,"
        "Last_Notified_Year INTEGER)"
    )
    conn.commit()


def read_lines():
    print("Paste your entire birthday list, then press Ctrl+D when done:")
    raw_text = sys.stdin.read()
    return raw_text


def add_to_db(conn, cursor):
    lines = read_lines().splitlines()
    for line in lines:
        if line.strip() == "":
            continue

        name, month, day = line.split(",")
        name = name.strip()
        month = int(month.strip())
        day = int(day.strip())

        today = nepali_datetime.date.today()
        birthday_date = nepali_datetime.date(today.year, month, day)
        difference = birthday_date - today

        if difference.days < 0:
            birthday_date = nepali_datetime.date(today.year + 1, month, day)
            difference = birthday_date - today

        birthday_str = birthday_date.strftime("%d %B")
        days_remaining_str = f"~{difference.days} days"

        cursor.execute(
            "INSERT INTO Reminder (Name, Birthday, Days_Remaining, Last_Notified_Year) "
            "VALUES (?, ?, ?, NULL)",
            (name, birthday_str, days_remaining_str),
        )
    conn.commit()
    print(f"Added {len([l for l in lines if l.strip()])} people.")