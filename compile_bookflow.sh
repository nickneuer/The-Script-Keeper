python data_cleaner.py $1 $2
python generate_sql.py $2
sqlite3 Keith_Books.db < books_populate.sql


