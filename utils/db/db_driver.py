import logging


# Checks for existing user table in db, if not there, create one
def init_user_table(con, cur, plex_connections):
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users_v2' ''')
    if cur.fetchone()[0] == 1:
        logging.info("SQLITE3: Existing users table found")
    else:
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
        if cur.fetchone()[0] == 1:
            logging.info("SQLITE3: Existing v1 users table found, converting to v2")
            convert_v1_v2(con, cur, plex_connections)
        else:
            logging.info("SQLITE3: No existing users table found, creating...")
            cur.execute(''' CREATE TABLE users_v2 (discord_user, user_plex_email, server_account, server_friendly_name, server_id, overseer_account_id) ''')
            con.commit()
            logging.info("SQLITE3: Users table created!")


# Add user to table
def add_user(con, cur, discord_user, user_plex_email, server_account, server_friendly_name, server_id, overseer_account_id):
    cur.execute("INSERT INTO users_v2 VALUES (?, ?, ?, ?, ?, ?)", (discord_user, user_plex_email, server_account, server_friendly_name, server_id, overseer_account_id))
    con.commit()


# Fetch users from table
def get_users(cur):
    rows = []
    for row in cur.execute("SELECT * FROM users_v2"):
        rows.append(row)
    return rows


# Check DB if user exists
def check_user(cur, discord_user):
    cur.execute("SELECT count(*) FROM users_v2 WHERE discord_user=:user", {"user": discord_user})
    if cur.fetchone()[0] >= 1:
        return True
    else:
        return False


# Check DB if user exists
def check_user_email(cur, user_email):
    cur.execute("SELECT count(*) FROM users_v2 WHERE user_plex_email=:email", {"email": user_email})
    if cur.fetchone()[0] >= 1:
        return True
    else:
        return False


# Grab user info from DB given email
def grab_user(cur, user_email):
    cur.execute("SELECT * FROM users_v2 WHERE user_plex_email=:email", {"email": user_email})
    return cur.fetchone()


def delete_user(cur, con, user_email):
    cur.execute("DELETE FROM users_v2 WHERE user_plex_email=:email", {"email": user_email})
    con.commit()


# Convert a V1 table to a V2 table
def convert_v1_v2(con, cur, plex_connections):
    cur.execute(''' CREATE TABLE users_v2 (discord_user, user_plex_email, server_account, server_friendly_name, server_id, overseer_account_id) ''')
    rows = []
    for row in cur.execute("SELECT * FROM users"):
        rows.append(row)
    for row in rows:
        for plex_server_account in plex_connections:
            for server in plex_server_account['servers']:
                if server.friendlyName == row[2]:
                    server_id = server.machineIdentifier
                    server_account = plex_server_account['account'].email
        cur.execute("INSERT INTO users_v2 VALUES (?, ?, ?, ?, ?, ?)", (row[0], row[1], server_account, row[2], server_id, "None"))
        logging.info(f"SQLITE3: Record: ({row[0]}, {row[1]}, {server_account}, {row[2]}, {server_id}, None) transferred to v2 table")
    logging.info(f"SQLITE3: v2 table complete!")
    cur.execute("DROP TABLE users")
    logging.info(f"SQLITE3: v1 table deleted!")
    con.commit()
