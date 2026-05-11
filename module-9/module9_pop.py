"""
Willson Financial – Milestone 2
Gold Team: Kobe Alexander, Samuel Dirr, Sebastian Siqueiros, Zachary White
Professor Sue Sampson

Script 2: insert_records.py
Populates all 7 tables with 6 sample records each.
Run create_tables.py FIRST before running this script.
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


def connect_to_database():
    """Connect to the willson_financial database."""
    try:
        db = mysql.connector.connect(**config)
        if db.is_connected():
            print("\n  Database user {} connected to MySQL on host {} with database {}".format(
                config["user"], config["host"], config["database"]
            ))
            return db
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist.")
        else:
            print(err)
        return None


def insert_employees(cursor):
    """Insert 6 employee records."""
    employees = [
        (1, "Jake",    "Willson",  "Co-Founder / Advisor", "Full-Time", "jake.willson@willsonfinancial.com",    "505-555-0101"),
        (2, "Ned",     "Willson",  "Co-Founder / Advisor", "Full-Time", "ned.willson@willsonfinancial.com",     "505-555-0102"),
        (3, "Phoenix", "Two Star", "Office Administrator", "Full-Time", "phoenix.twostar@willsonfinancial.com", "505-555-0103"),
        (4, "June",    "Santos",   "Compliance Manager",   "Part-Time", "june.santos@willsonfinancial.com",     "505-555-0104"),
        (5, "Maria",   "Reyes",    "Client Support",       "Full-Time", "maria.reyes@willsonfinancial.com",     "505-555-0105"),
        (6, "Tom",     "Harker",   "Financial Analyst",    "Full-Time", "tom.harker@willsonfinancial.com",      "505-555-0106"),
    ]
    sql = """
        INSERT INTO EMPLOYEE (employee_id, first_name, last_name, role, employment_type, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, employees)
    print("  Inserted 6 records into EMPLOYEE.")


def insert_advisors(cursor):
    """Insert 6 advisor records."""
    advisors = [
        (1, "Jake",   "Willson", "CFA",     "jake.willson@willsonfinancial.com",  "505-555-0101"),
        (2, "Ned",    "Willson", "CFA,MBA", "ned.willson@willsonfinancial.com",   "505-555-0102"),
        (3, "Maria",  "Reyes",   "CFP",     "maria.reyes@willsonfinancial.com",   "505-555-0105"),
        (4, "Tom",    "Harker",  "CFA",     "tom.harker@willsonfinancial.com",    "505-555-0106"),
        (5, "Sarah",  "Ortega",  "CFP",     "sarah.ortega@willsonfinancial.com",  "505-555-0107"),
        (6, "Daniel", "Cruz",    "MBA",     "daniel.cruz@willsonfinancial.com",   "505-555-0108"),
    ]
    sql = """
        INSERT INTO ADVISOR (advisor_id, first_name, last_name, credentials, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, advisors)
    print("  Inserted 6 records into ADVISOR.")


def insert_clients(cursor):
    """Insert 6 client records — ranchers, farmers, and retirees in New Mexico."""
    clients = [
        (1, "Roy",    "Castillo",  "roy.castillo@email.com",    "505-555-2001", "2024-01-15", 1),
        (2, "Linda",  "Begay",     "linda.begay@email.com",     "505-555-2002", "2024-02-20", 2),
        (3, "Harold", "Thornton",  "harold.thornton@email.com", "505-555-2003", "2024-03-10", 1),
        (4, "Gloria", "Padilla",   "gloria.padilla@email.com",  "505-555-2004", "2024-04-05", 2),
        (5, "Eugene", "Trujillo",  "eugene.trujillo@email.com", "505-555-2005", "2024-05-18", 1),
        (6, "Martha", "Sandoval",  "martha.sandoval@email.com", "505-555-2006", "2024-06-22", 2),
    ]
    sql = """
        INSERT INTO CLIENT (client_id, first_name, last_name, email, phone, enrollment_date, advisor_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, clients)
    print("  Inserted 6 records into CLIENT.")


def insert_accounts(cursor):
    """Insert 6 account records."""
    accounts = [
        (1, 1, "Individual Brokerage",  45000.00,  "USD", "2024-01-20"),
        (2, 2, "IRA",                   82500.50,  "USD", "2024-02-25"),
        (3, 3, "Individual Brokerage",  15000.75,  "USD", "2024-03-15"),
        (4, 4, "Retirement",           132000.00,  "USD", "2024-04-10"),
        (5, 5, "Individual Brokerage",   9200.25,  "USD", "2024-05-22"),
        (6, 6, "IRA",                   67450.80,  "USD", "2024-06-30"),
    ]
    sql = """
        INSERT INTO ACCOUNT (account_id, client_id, account_type, balance, currency, open_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, accounts)
    print("  Inserted 6 records into ACCOUNT.")


def insert_transactions(cursor):
    """Insert 6 transaction records."""
    transactions = [
        (1, 1, "2024-02-01", "Deposit",    5000.00, "Initial portfolio deposit"),
        (2, 2, "2024-03-05", "Deposit",    1200.00, "Monthly IRA contribution"),
        (3, 3, "2024-04-12", "Withdrawal",  750.00, "Partial withdrawal"),
        (4, 4, "2024-05-03", "Deposit",    2000.00, "Retirement contribution"),
        (5, 5, "2024-06-14", "Deposit",    3500.00, "Ranch sale proceeds deposit"),
        (6, 6, "2024-07-01", "Deposit",     950.00, "Monthly savings transfer"),
    ]
    sql = """
        INSERT INTO `TRANSACTION` (transaction_id, account_id, transaction_date, transaction_type, amount, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, transactions)
    print("  Inserted 6 records into TRANSACTION.")


def insert_appointments(cursor):
    """Insert 6 appointment records."""
    appointments = [
        (1, 1, 1, "2024-02-10", "09:00:00", "Initial financial planning meeting"),
        (2, 2, 2, "2024-03-12", "10:30:00", "IRA contribution review"),
        (3, 3, 1, "2024-04-18", "13:00:00", "Portfolio strategy discussion"),
        (4, 4, 2, "2024-05-20", "14:15:00", "Retirement income planning"),
        (5, 5, 1, "2024-06-25", "11:00:00", "New account setup and review"),
        (6, 6, 2, "2024-07-08", "15:30:00", "Annual portfolio review"),
    ]
    sql = """
        INSERT INTO APPOINTMENT (appointment_id, client_id, advisor_id, appt_date, appt_time, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, appointments)
    print("  Inserted 6 records into APPOINTMENT.")


def insert_compliance_records(cursor):
    """Insert 6 compliance records."""
    compliance_records = [
        (1, "2024-02-15", "Account Review",       "Passed",          "June Santos"),
        (2, "2024-03-20", "Risk Assessment",       "Passed",          "June Santos"),
        (3, "2024-04-22", "Transaction Audit",     "Needs Follow-Up", "June Santos"),
        (4, "2024-05-30", "Policy Review",         "Passed",          "June Santos"),
        (5, "2024-06-18", "Client Documentation",  "Passed",          "June Santos"),
        (6, "2024-07-12", "SEC Compliance Review", "Passed",          "June Santos"),
    ]
    sql = """
        INSERT INTO COMPLIANCE_RECORD (compliance_id, review_date, review_type, outcome, reviewed_by)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, compliance_records)
    print("  Inserted 6 records into COMPLIANCE_RECORD.")


def main():
    db = connect_to_database()
    if db is None:
        print("  Database connection failed. Make sure create_tables.py was run first.")
        return

    try:
        cursor = db.cursor()

        print("\n  Inserting records...")
        insert_employees(cursor)
        insert_advisors(cursor)
        insert_clients(cursor)
        insert_accounts(cursor)
        insert_transactions(cursor)
        insert_appointments(cursor)
        insert_compliance_records(cursor)

        db.commit()
        print("\n  All records inserted successfully.")

    except mysql.connector.Error as err:
        db.rollback()
        print(f"  Error inserting records: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            print("  Database connection closed.")

    input("\n  Press any key to continue...")


if __name__ == "__main__":
    main()