"""
Willson Financial – Milestone 2
Gold Team: Kobe Alexander, Samuel Dirr, Sebastian Siqueiros, Zachary White
Professor Sue Sampson

Script 3: display_tables.py
Displays all records from each table in the willson_financial database.
Run create_tables.py and insert_records.py FIRST before running this script.
"""

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values
import os

# Load .env file from the same folder as this script
base_dir = os.path.dirname(os.path.abspath(__file__))
secrets = dotenv_values(os.path.join(base_dir, ".env"))

# Database config
config = {
    "user":              secrets["USER"],
    "password":          secrets["PASSWORD"],
    "host":              secrets["HOST"],
    "database":          secrets["DATABASE"],
    "raise_on_warnings": secrets["RAISE_ON_WARNINGS"].lower() == "true"
}

tables = [
    "EMPLOYEE",
    "ADVISOR",
    "CLIENT",
    "ACCOUNT",
    "`TRANSACTION`",
    "APPOINTMENT",
    "COMPLIANCE_RECORD"
]

try:
    db = mysql.connector.connect(**config)

    print("\n  Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]
    ))

    cursor = db.cursor()

    for table in tables:
        print("\n  ========================================")
        print(f"  TABLE: {table}")
        print("  ========================================")
        cursor.execute(f"SELECT * FROM {table}")
        results = cursor.fetchall()
        for row in results:
            formatted = tuple(str(v) for v in row)
            print(" ", formatted)

    print("\n  All tables displayed successfully.")
    input("\n  Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist.")
    else:
        print(err)

finally:
    if db.is_connected():
        cursor.close()
        db.close()
        print("  Database connection closed.")
