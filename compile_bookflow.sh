
#takes cmd line args (week_whatevs.txt, filthy.csv, cleaned.csv, <this weeks table>)

python text_remover.py $1 $2
python data_cleaner.py $2 $3
python generate_sql.py $3 $4
sqlite3 Keith_Books.db < books_populate.sql


