import os
import requests
import nepali_datetime
from db import connect_db

REMIND_WITHIN_DAYS = 7
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")


def month_name_to_number(year):
    """Builds {'Baishakh': 1, 'Jestha': 2, ...} dynamically, so it always
    matches whatever spelling nepali_datetime itself produces."""
    mapping = {}
    for m in range(1, 13):
        d = nepali_datetime.date(year, m, 1)
        mapping[d.strftime("%B")] = m
    return mapping


def send_discord_message(content):
    if not WEBHOOK_URL:
        print("No DISCORD_WEBHOOK_URL set. Message was:", content)
        return False
    resp = requests.post(WEBHOOK_URL, json={"content": content})
    if resp.status_code not in (200, 204):
        print(f"Discord send failed ({resp.status_code}): {resp.text}")
        return False
    return True


def check_and_notify():
    conn, cursor = connect_db()
    today = nepali_datetime.date.today()
    name_to_num = month_name_to_number(today.year)

    rows = cursor.execute(
        "SELECT Id, Name, Birthday, Last_Notified_Year FROM Reminder"
    ).fetchall()

    for person_id, name, birthday_str, last_notified_year in rows:
        day_str, month_name = birthday_str.split(" ", 1)
        day = int(day_str)
        month = name_to_num[month_name]

        occ = nepali_datetime.date(today.year, month, day)
        if (occ - today).days < 0:
            occ = nepali_datetime.date(today.year + 1, month, day)

        days_left = (occ - today).days

        if days_left <= REMIND_WITHIN_DAYS and last_notified_year != occ.year:
            if days_left == 0:
                msg = f"🎂 It's **{name}'s** birthday today!"
            else:
                msg = f"🎉 **{name}'s** birthday is in {days_left} day(s) — {birthday_str}."
            sent = send_discord_message(msg)

            if sent:
                cursor.execute(
                    "UPDATE Reminder SET Last_Notified_Year = ? WHERE Id = ?",
                    (occ.year, person_id),
                )
                conn.commit()

    conn.close()


if __name__ == "__main__":
    check_and_notify()