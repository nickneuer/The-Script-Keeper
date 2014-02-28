import sys 

SQL = """
DROP TABLE books;

CREATE TABLE books(author varchar, title varchar, ISBN int, binding varchar, price float, BISAC varchar, publisher varchar, date_pub varchar, TW int, YTD int, RTD int);

.mode csv
.separator ';'
.import {0} books
"""

with open("books_populate.sql", "wb") as out:
    out.write(SQL.format(sys.argv[1]))
