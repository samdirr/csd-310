"""
Willson Financial – Milestone 3
Gold Team: Kobe Alexander, Samuel Dirr, Sebastian Siqueiros, Zachary White
Professor Sue Sampson

Script: supplemental_insert.py
Adds high-volume transactions for THREE clients so Report 3 returns
multiple results — clients with more than 10 transactions in a single month.

Client 1 (Roy Castillo,     account_id 1) — 11 transactions in Feb 2025
Client 3 (Harold Thornton,  account_id 3) — 11 transactions in Feb 2025
Client 4 (Gloria Padilla,   account_id 4) — 12 transactions in Feb 2025

Safe to run multiple times as this code skips any records that already exist.
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

extra_transactions = [

    # ── Client 3: Harold Thornton (account_id 3) — 11 transactions Feb 2025 ──
    (7,  3, "2025-02-02", "Deposit",    1800.00, "Paycheck deposit"),
    (8,  3, "2025-02-04", "Withdrawal",  120.45, "Grocery purchase"),
    (9,  3, "2025-02-07", "Withdrawal",   55.00, "Gas station purchase"),
    (10, 3, "2025-02-10", "Deposit",     250.00, "Transfer from external account"),
    (11, 3, "2025-02-13", "Withdrawal",   89.99, "Internet bill payment"),
    (12, 3, "2025-02-16", "Withdrawal",   45.75, "Restaurant purchase"),
    (13, 3, "2025-02-19", "Deposit",     600.00, "Freelance payment"),
    (14, 3, "2025-02-22", "Withdrawal",  135.20, "Utility bill payment"),
    (15, 3, "2025-02-25", "Withdrawal",   75.00, "Subscription payments"),
    (16, 3, "2025-02-27", "Deposit",     400.00, "Savings transfer"),
    (17, 3, "2025-02-28", "Deposit",     225.00, "Ranch income deposit"),

    # ── Client 4: Gloria Padilla (account_id 4) — 12 transactions Feb 2025 ──
    (18, 4, "2025-02-01", "Deposit",    3500.00, "Monthly retirement contribution"),
    (19, 4, "2025-02-03", "Withdrawal",  210.00, "Property tax installment"),
    (20, 4, "2025-02-05", "Deposit",     875.00, "Rental income deposit"),
    (21, 4, "2025-02-08", "Withdrawal",  320.00, "Home insurance payment"),
    (22, 4, "2025-02-10", "Deposit",     450.00, "Livestock sale proceeds"),
    (23, 4, "2025-02-12", "Withdrawal",  185.00, "Vehicle maintenance"),
    (24, 4, "2025-02-14", "Deposit",     600.00, "Dividend reinvestment"),
    (25, 4, "2025-02-17", "Withdrawal",   95.50, "Medical copay"),
    (26, 4, "2025-02-19", "Deposit",    1200.00, "Farm equipment lease payment in"),
    (27, 4, "2025-02-21", "Withdrawal",  430.00, "Feed and supply purchase"),
    (28, 4, "2025-02-24", "Deposit",     275.00, "Interest earned"),
    (29, 4, "2025-02-26", "Withdrawal",  150.00, "Irrigation system repair"),

    # ── Client 1: Roy Castillo (account_id 1) — 11 transactions Feb 2025 ────
    (30, 1, "2025-02-02", "Deposit",    2200.00, "Ranch sale deposit"),
    (31, 1, "2025-02-04", "Withdrawal",  375.00, "Feed store purchase"),
    (32, 1, "2025-02-06", "Deposit",     500.00, "Government subsidy deposit"),
    (33, 1, "2025-02-09", "Withdrawal",  220.00, "Veterinary services"),
    (34, 1, "2025-02-11", "Deposit",     650.00, "Equipment rental income"),
    (35, 1, "2025-02-13", "Withdrawal",  140.00, "Fuel purchase"),
    (36, 1, "2025-02-15", "Deposit",     800.00, "Cattle sale proceeds"),
    (37, 1, "2025-02-18", "Withdrawal",  310.00, "Property maintenance"),
    (38, 1, "2025-02-20", "Deposit",     425.00, "Water rights payment in"),
    (39, 1, "2025-02-23", "Withdrawal",   95.00, "Subscription and permits"),
    (40, 1, "2025-02-27", "Deposit",     550.00, "Monthly savings transfer"),
]

sql = """
    INSERT INTO `TRANSACTION`
        (transaction_id, account_id, transaction_date, transaction_type, amount, description)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

db = None
cursor = None

try:
    db = mysql.connector.connect(**config)

    print("\n  Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]
    ))

    cursor = db.cursor()

    inserted = 0
    skipped  = 0

    for record in extra_transactions:
        try:
            cursor.execute(sql, record)
            db.commit()
            inserted += 1
        except mysql.connector.Error as err:
            if err.errno == 1062:
                # Duplicate primary key — record already exists, skip it
                print(f"  Skipping transaction_id {record[0]} — already exists.")
                skipped += 1
            else:
                # Any other error should still raise
                raise

    print(f"\n  Done.")
    print(f"  Inserted : {inserted} new transaction(s)")
    print(f"  Skipped  : {skipped} duplicate(s) already in database")
    print(f"\n  Report 3 will return:")
    print("    - Roy Castillo    (account 1) — 11 transactions in Feb 2025")
    print("    - Harold Thornton (account 3) — 11 transactions in Feb 2025")
    print("    - Gloria Padilla  (account 4) — 12 transactions in Feb 2025")

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
