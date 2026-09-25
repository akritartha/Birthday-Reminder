# Birthday-Reminder

A SQLite + Discord webhook birthday reminder, using the Bikram Sambat (BS) calendar via `nepali_datetime`.

## How it works

- `db.py` — shared database connection, table setup, and the "add people" logic
- `add_person.py` — run manually whenever you want to add people (accepts a pasted list)
- `check_birthdays.py` — run automatically (via cron) once a day; checks who's coming up and pings Discord

## Setup

1. Clone the repo and move into it:
   ```
   git clone https://github.com/<your-username>/Birthday-Reminder.git
   cd Birthday-Reminder
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install requests nepali_datetime
   ```

4. Create a Discord webhook:
   - In your Discord server: **Server Settings → Integrations → Webhooks → New Webhook**
   - Name it, point it at your target channel, click **Copy Webhook URL**

5. Set the webhook URL as an environment variable:
   ```
   export DISCORD_WEBHOOK_URL="paste your webhook url here"
   ```
   (Add this line to your `~/.bashrc` if you want it to persist across terminal sessions — never commit it to a file in the repo.)

## Adding people

Run:
```
python3 add_person.py
```

This creates the database/table if they don't exist yet, then prompts you to paste your list. Format, one person per line:
```
Ram Shrestha, 3, 14
Sita Gurung, 7, 2
```
(`Name, Month, Day` — month/day in the Bikram Sambat calendar, no leading zeros needed)

Press **Ctrl+D** on an empty line when you're done pasting to submit the batch.

## Checking birthdays manually (test run)

```
python3 check_birthdays.py
```

If anyone's birthday is within 7 days, you'll see a message land in your Discord channel. If nothing's due, you can temporarily add a person with today's date to force a test message.

## Automating it with cron

Run `crontab -e` and add a line like:
```
0 8 * * * cd /full/path/to/Birthday-Reminder && /full/path/to/.venv/bin/python check_birthdays.py >> cron.log 2>&1
```

This runs the check every day at 8:00 AM and logs output to `cron.log` so you can confirm it actually ran.

To test quickly instead of waiting until tomorrow, temporarily set the cron time to a couple of minutes from now, wait, then check `cron.log` and Discord.

## Notes

- Birthdays are stored in BS (Bikram Sambat) format, e.g. `"14 Chaitra"`.
- Each person is only notified once per year for a given birthday (tracked via `Last_Notified_Year`), so you won't get repeat pings every day during the reminder window.
- `birthday.db` is intentionally excluded from git via `.gitignore` — your data stays local.
