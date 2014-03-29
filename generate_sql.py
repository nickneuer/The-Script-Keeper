import sys 

SQL = """
CREATE TABLE IF NOT EXISTS {1}(author varchar, title varchar, ISBN int, binding varchar, price float, BISAC varchar, publisher varchar, date_pub varchar, TW float, YTD float, RTD float);

.mode csv
.separator ';'
.import {0} {1}
"""

with open("books_populate.sql", "wb") as out:
    out.write(SQL.format(sys.argv[1], sys.argv[2]))
