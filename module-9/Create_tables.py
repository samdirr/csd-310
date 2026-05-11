"""
Willson Financial – Milestone 2
Gold Team: Kobe Alexander, Samuel Dirr, Sebastian Siqueiros, Zachary White
Professor Sue Sampson

Script 1: create_tables.py
Creates the willson_financial database and all 7 tables.
Run this script FIRST before running insert_records.py
"""

import os

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


# Load .env file from the same folder as this script
base_dir = os.path.dirname(os.path.abspath(__file__))
secrets = dotenv_values(os.path.join(base_dir, ".env"))


# Database config
config = {
    "user":              secrets["USER"],
    "password":          secrets["PASSWORD"],
    "host":              secrets["HOST"],
    "database":          secrets["DATABASE"],
    "raise_on_warnings": True
}

CREATE_STATEMENTS = [

    # 1. EMPLOYEE — no dependencies
    """
    CREATE TABLE IF NOT EXISTS EMPLOYEE (
        employee_id     INT           PRIMARY KEY,
        first_name      VARCHAR(50)   NOT NULL,
        last_name       VARCHAR(50)   NOT NULL,
        role            VARCHAR(75)   NOT NULL,
        employment_type VARCHAR(50)   NOT NULL,
        email           VARCHAR(100)  NOT NULL UNIQUE,
        phone           VARCHAR(20)
    )
    """,

    # 2. ADVISOR — no dependencies
    """
    CREATE TABLE IF NOT EXISTS ADVISOR (
        advisor_id  INT           PRIMARY KEY,
        first_name  VARCHAR(50)   NOT NULL,
        last_name   VARCHAR(50)   NOT NULL,
        credentials VARCHAR(50),
        email       VARCHAR(100)  NOT NULL UNIQUE,
        phone       VARCHAR(20)
    )
    """,

    # 3. CLIENT — references ADVISOR
    """
    CREATE TABLE IF NOT EXISTS CLIENT (
        client_id       INT           PRIMARY KEY,
        first_name      VARCHAR(50)   NOT NULL,
        last_name       VARCHAR(50)   NOT NULL,
        email           VARCHAR(100)  NOT NULL UNIQUE,
        phone           VARCHAR(20),
        enrollment_date DATE          NOT NULL,
        advisor_id      INT,
        CONSTRAINT fk_client_advisor
            FOREIGN KEY (advisor_id) REFERENCES ADVISOR(advisor_id)
            ON UPDATE CASCADE ON DELETE SET NULL
    )
    """,

    # 4. ACCOUNT — references CLIENT
    """
    CREATE TABLE IF NOT EXISTS ACCOUNT (
        account_id   INT            PRIMARY KEY,
        client_id    INT            NOT NULL,
        account_type VARCHAR(50)    NOT NULL,
        balance      DECIMAL(12,2)  NOT NULL DEFAULT 0.00,
        currency     CHAR(3)        NOT NULL DEFAULT 'USD',
        open_date    DATE           NOT NULL,
        CONSTRAINT fk_account_client
            FOREIGN KEY (client_id) REFERENCES CLIENT(client_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT chk_account_balance CHECK (balance >= 0)
    )
    """,

    # 5. TRANSACTION — references ACCOUNT
    """
    CREATE TABLE IF NOT EXISTS `TRANSACTION` (
        transaction_id   INT            PRIMARY KEY,
        account_id       INT            NOT NULL,
        transaction_date DATE           NOT NULL,
        transaction_type VARCHAR(50)    NOT NULL,
        amount           DECIMAL(12,2)  NOT NULL,
        description      VARCHAR(255),
        CONSTRAINT fk_transaction_account
            FOREIGN KEY (account_id) REFERENCES ACCOUNT(account_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT chk_transaction_amount CHECK (amount > 0)
    )
    """,

    # 6. APPOINTMENT — references CLIENT and ADVISOR
    """
    CREATE TABLE IF NOT EXISTS APPOINTMENT (
        appointment_id INT          PRIMARY KEY,
        client_id      INT          NOT NULL,
        advisor_id     INT          NOT NULL,
        appt_date      DATE         NOT NULL,
        appt_time      TIME         NOT NULL,
        notes          VARCHAR(255),
        CONSTRAINT fk_appointment_client
            FOREIGN KEY (client_id) REFERENCES CLIENT(client_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT fk_appointment_advisor
            FOREIGN KEY (advisor_id) REFERENCES ADVISOR(advisor_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    # 7. COMPLIANCE_RECORD — no dependencies
    """
    CREATE TABLE IF NOT EXISTS COMPLIANCE_RECORD (
        compliance_id INT          PRIMARY KEY,
        review_date   DATE         NOT NULL,
        review_type   VARCHAR(100) NOT NULL,
        outcome       VARCHAR(100) NOT NULL,
        reviewed_by   VARCHAR(100) NOT NULL
    )
    """,
]


def main():
    try:
        db = mysql.connector.connect(**config)

        print("\n  Database user {} connected to MySQL on host {} with database {}".format(
            config["user"], config["host"], config["database"]
        ))

        cursor = db.cursor()

        for statement in CREATE_STATEMENTS:
            cursor.execute(statement)
            table_name = [w for w in statement.split()
                          if w.upper() not in ("CREATE", "TABLE", "IF", "NOT", "EXISTS", "")][0]
            print(f"  Table {table_name} created successfully.")

        db.commit()
        print("\n  All 7 tables created successfully.")

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


if __name__ == "__main__":
    main()