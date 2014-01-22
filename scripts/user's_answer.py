import sys
import MySQLdb as mdb
db = mdb.connect('localhost', 'ask-user', '19251925', 'ask_db',init_command='SET NAMES UTF8')
cursor = db.cursor()
cursor.execute('select ask_answer.id,ask_answer.date,ask_answer.rating, ask_answer.body , auth_user.username from ask_answer inner join auth_user on ask_answer.author_id = auth_user.id where auth_user.id = 1 order by ask_answer.date desc' )
top = cursor.fetchall()
print(' answers of user with id = 1')
for x in top:
    print ('id = {0} , rating = {1} ,answer = {3}, date = {2} , username = {4}'.format(x[0],x[2],x[1],x[3],x[4])) 
db.close()
