#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

# Establish the connection to the database
db = get_db()
cursor = db.cursor()

# Execute a simple query
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])

# Close cursor and connection
cursor.close()
db.close()
