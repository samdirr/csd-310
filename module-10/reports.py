"""
Willson Financial – Milestone 3
Gold Team: Kobe Alexander, Samuel Dirr, Sebastian Siqueiros, Zachary White
Professor Sue Sampson

Script: reports.py
Runs all three business reports against the willson_financial database.
Run supplemental_insert.py FIRST to ensure Report 3 returns results.
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

db = None
cursor = None

try:
    db = mysql.connector.connect(**config)

    print("\n  Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]
    ))

    cursor = db.cursor()

    # ── REPORT 1: Clients added per month ────────────────────────────────────
    print("\n  ===== REPORT 1: CLIENTS ADDED BY MONTH =====\n")

    query1 = """
        SELECT
            DATE_FORMAT(enrollment_date, '%Y-%m') AS month,
            COUNT(client_id)                      AS total_clients
        FROM CLIENT
        GROUP BY month
        ORDER BY month;
    """

    cursor.execute(query1)
    for row in cursor.fetchall():
        print(f"    Month: {row[0]}  |  Clients Added: {row[1]}")

    # ── REPORT 2: Average client assets ──────────────────────────────────────
    print("\n  ===== REPORT 2: AVERAGE CLIENT ASSETS =====\n")

    query2 = """
        SELECT ROUND(AVG(balance), 2) AS avg_assets
        FROM ACCOUNT;
    """

    cursor.execute(query2)
    for row in cursor.fetchall():
        print(f"    Average Assets Across All Clients: ${row[0]:,.2f}")

    # ── REPORT 3: High-transaction clients (more than 10 per month) ──────────
    print("\n  ===== REPORT 3: HIGH TRANSACTION CLIENTS (MORE THAN 10/MONTH) =====\n")

    query3 = """
        SELECT
            c.first_name,
            c.last_name,
            DATE_FORMAT(t.transaction_date, '%Y-%m') AS month,
            COUNT(t.transaction_id)                  AS transaction_total
        FROM CLIENT c
        JOIN ACCOUNT a     ON c.client_id  = a.client_id
        JOIN `TRANSACTION` t ON a.account_id = t.account_id
        GROUP BY c.client_id, month
        HAVING transaction_total > 10
        ORDER BY transaction_total DESC;
    """

    cursor.execute(query3)
    results = cursor.fetchall()

    if results:
        for row in results:
            print(f"    {row[0]} {row[1]}  |  Month: {row[2]}  |  Transactions: {row[3]}")
    else:
        print("    No clients exceeded 10 transactions in a single month.")

    print("\n  All reports complete.")
    input("\n  Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist.")
    else:
        print(err)

finally:
    if db is not None and db.is_connected():
        if cursor is not None:
            cursor.close()
        db.close()
        print("  Database connection closed.")
