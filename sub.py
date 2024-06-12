import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('fes_app.db')

# Create a cursor object
cursor = conn.cursor()

# Define table creation statements
mission_table = """
CREATE TABLE IF NOT EXISTS Mission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mission_id TEXT UNIQUE,
    mission_code TEXT,
    img_domain TEXT
);
"""

cipher_table = '''CREATE TABLE IF NOT EXISTS Cipher (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   cipher_id TEXT UNIQUE,
                   mission_id INTEGER,
                   cipher TEXT,
                   point INTEGER,
                   FOREIGN KEY (mission_id) REFERENCES Mission(id)
                   )'''

user_table = """
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE,
    username TEXT,
    password TEXT,
    points INTEGER,
    episode INTEGER
);
"""

logs_table = '''CREATE TABLE IF NOT EXISTS Logs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id TEXT,
                   mission_id TEXT,
                   cipher_id TEXT,
                   success BOOLEAN DEFAULT FALSE,
                   time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES User(id),
                   FOREIGN KEY (mission_id) REFERENCES Mission(id),
                   FOREIGN KEY (cipher_id) REFERENCES Cipher(cipher_id)
                   )'''

#cursor.execute("DROP TABLE Logs")
#conn.commit()



# Execute the table creation statements
#cursor.execute(mission_table)
#cursor.execute(cipher_table)
# cursor.execute(user_table)
#cursor.execute(logs_table)

cipher_data = (6789, 2345, 6789, 1)  # Replace with appropriate values if needed
#cursor.execute('INSERT INTO Cipher (cipher_id, mission_id, cipher, point) VALUES (?, ?, ?, ?)', cipher_data)

mission_data = (2345, 2345, 0)  # Replace with appropriate values if needed
#cursor.execute('INSERT INTO Mission (mission_id, mission_code, img_domain) VALUES (?, ?, ?)', mission_data)

# Save changes and close the connection
conn.commit()
conn.close()

print("Tables created successfully!")
