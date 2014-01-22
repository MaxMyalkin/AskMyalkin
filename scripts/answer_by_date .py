import sys
import MySQLdb as mdb
db = mdb.connect('localhost', 'ask-user', '19251925', 'ask_db',init_command='SET NAMES UTF8')
cursor = db.cursor()
cursor.execute('select id , date, rating, body from ask_answer order by date desc limit 50' )
top = cursor.fetchall()
print('Newest 50 answer')
for x in top:
   print ('id = {0} , date = {1} , rating = {2} , answer = {3}'.format(x[0],x[1],x[2],x[3]))
db.close()
