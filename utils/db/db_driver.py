import logging


# Checks for existing user table in db, if not there, create one
def init_user_table(con, cur):
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
    if cur.fetchone()[0] == 1:
        logging.info("SQLITE3: Existing users table found")
    else:
        logging.info("SQLITE3: No existing users table found, creating...")
        cur.execute(''' CREATE TABLE users (discord_user, plex_email, server) ''')
        con.commit()
        logging.info("SQLITE3: Users table created!")


# Add user to table
def add_user(con, cur, discord_user, plex_email, server):
    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (discord_user, plex_email, server))
    con.commit()


# Fetch users from table
def get_users(cur):
    rows = []
    for row in cur.execute("SELECT * FROM users"):
        rows.append(row)
    return rows


# Search DB for user
def search_user(cur, discord_user):
    cur.execute("SELECT count(*) FROM users WHERE discord_user=:user", {"user": discord_user})
    if cur.fetchone()[0] >= 1:
        return True
    else:
        return False
