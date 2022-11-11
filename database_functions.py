import sqlite3
import csv
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
import math

def send_to_database(table, widget):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    many = []
    i = 0

    while True:
        if not widget.item(i, 0):
            break
        else:
            i += 1

    for index in range(i):
        D0 = widget.item(index, 0).text()
        D1 = widget.item(index, 1).text()
        D2 = widget.item(index, 2).text()
        D3 = int(widget.item(index, 3).text())
        D4 = widget.item(index, 4).text()

        if widget.item(index, 5).text() != '' and widget.item(index, 5).text() != " ":
            D5 = float(widget.item(index, 5).text())
        else:
            D5 = " "

        if widget.item(index, 6).text() != '' and widget.item(index, 6).text() != " ":
            D6 = float(widget.item(index, 6).text())
        else:
            D6 = " "

        D7 = float(widget.item(index, 7).text())
        many.append((D0, D1, D2, D3, D4, D5, D6, D7))


    c.executemany(f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?)", many)

    conn.commit()
    conn.close()

def clear_table(table):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute(f"DELETE from {table}")

    conn.commit()
    conn.close()

def extract_data(filepath):
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        next(csv_reader)

        for line in csv_reader:
            many = [
                (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
            ]
            c.executemany(f"INSERT INTO statement VALUES (?, ?, ?, ?, ?, ?, ?, ?)", many)

        conn.commit()
        conn.close()

def insert_data(table, widget):
    i = 0
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table}")
    for item in c.fetchall():
        widget.setItem(i, 0, QTableWidgetItem(str(item[0])))
        widget.setItem(i, 1, QTableWidgetItem(str(item[1])))
        widget.setItem(i, 2, QTableWidgetItem(str(item[2])))
        widget.setItem(i, 3, QTableWidgetItem(str(item[3])))
        widget.setItem(i, 4, QTableWidgetItem(str(item[4])))
        widget.setItem(i, 5, QTableWidgetItem(str(item[5])))
        widget.setItem(i, 6, QTableWidgetItem(str(item[6])))
        widget.setItem(i, 7, QTableWidgetItem(str(item[7])))
        i += 1

    conn.commit()
    conn.close()

def save_total(table):
    addCredit = []
    addDebit = []
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table}")
    statements = c.fetchall()

    for item in statements:
        if item[6] != '':
            addCredit.append(item[6])

    for item in statements:
        if item[5] != '':
            addDebit.append(item[5])

    totalCredit = str(round(math.fsum(addCredit), 2))
    totalDebit = str(round(math.fsum(addDebit), 2))

    conn.commit()
    conn.close()
    return totalCredit, totalDebit

def merge_values(table, data, widget):

    # Create two empty arrays and connect to Sqlite3 database
    addCredit = []
    addDebit = []
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Find all results in Sqlite3 database that have the string in the reference
    c.execute(f"SELECT * FROM {table} WHERE description LIKE '%{data}%' ")
    statements = c.fetchall()
    length = len(statements)
    # Save top-most result in multiple new variables
    new_row_date = statements[0][0]
    new_row_type = statements[0][1]
    new_row_sort = statements[0][2]
    new_row_account = statements[0][3]
    new_row_reference = statements[0][4]
    new_row_balance = statements[0][7]

    for item in statements:
        if item[6] != '' and item[6] != " ":
            addCredit.append(item[6])

    for item in statements:
        if item[5] != '' and item[5] != " ":
            addDebit.append(item[5])

    totalCredit = str(round(math.fsum(addCredit), 2))
    totalDebit = str(round(math.fsum(addDebit), 2))

    # Reset Table
    widget.setRowCount(0)
    widget.setRowCount(1000)

    # Delete found rows from Sqlite3 database
    c.execute(f"DELETE from {table} WHERE description LIKE '%{data}%'")
    c.execute(f"SELECT * from {table}")

    # Setting the iterator to 1, which will leave the top row of the table empty later
    i = 1

    # List out everything
    c.execute(f"SELECT * FROM {table}")

    # Fill out the top row with the new row data
    widget.setItem(0, 0, QTableWidgetItem(str(new_row_date)))
    widget.setItem(0, 1, QTableWidgetItem(str(new_row_type)))
    widget.setItem(0, 2, QTableWidgetItem(str(new_row_sort)))
    widget.setItem(0, 3, QTableWidgetItem(str(new_row_account)))
    widget.setItem(0, 4, QTableWidgetItem(str(new_row_reference)))

    if totalDebit:
        widget.setItem(0, 5, QTableWidgetItem(str(totalDebit)))

    if totalCredit:
        widget.setItem(0, 6, QTableWidgetItem(str(totalCredit)))

    widget.setItem(0, 7, QTableWidgetItem(str(new_row_balance)))

    # Fill in the rest of the table with everything in the Sqlite3 database
    for item in c.fetchall():
        widget.setItem(i, 0, QTableWidgetItem(str(item[0])))
        widget.setItem(i, 1, QTableWidgetItem(str(item[1])))
        widget.setItem(i, 2, QTableWidgetItem(str(item[2])))
        widget.setItem(i, 3, QTableWidgetItem(str(item[3])))
        widget.setItem(i, 4, QTableWidgetItem(str(item[4])))
        widget.setItem(i, 5, QTableWidgetItem(str(item[5])))
        widget.setItem(i, 6, QTableWidgetItem(str(item[6])))
        widget.setItem(i, 7, QTableWidgetItem(str(item[7])))
        i += 1

    conn.commit()
    conn.close()