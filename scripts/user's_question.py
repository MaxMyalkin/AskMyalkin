import sys
import MySQLdb as mdb
db = mdb.connect('localhost', 'ask-user', '19251925', 'ask_db',init_command='SET NAMES UTF8')
cursor = db.cursor()
cursor.execute('select ask_question.id , ask_question.date , ask_question.rating , ask_question.title , auth_user.username from ask_question inner join auth_user on ask_question.author_id = auth_user.id where auth_user.id = 1 order by ask_question.date desc' )
top = cursor.fetchall()
print(" question of the user with id = 1 by date ")
for x in top:
    print (' id = {2} , rating = {1} , question = {3} , date = {0} , username = {4}'.format(x[1],x[2],x[0],x[3],x[4])) 
db.close()
