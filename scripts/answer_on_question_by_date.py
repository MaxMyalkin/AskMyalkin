import sys
import MySQLdb as mdb
db = mdb.connect('localhost', 'ask-user', '19251925', 'ask_db',init_command='SET NAMES UTF8')
cursor = db.cursor()
cursor.execute('select ask_answer.id , ask_answer.body,ask_answer.date,ask_answer.rating, ask_question.title from ask_answer inner join ask_question on ask_answer.question_id = ask_question.id where ask_question.id = 1 order by ask_answer.date desc' )
top = cursor.fetchall()
print('Answer on question with id = 1 by date')
for x in top:
    print ('id = {0} , date = {1} , rating = {2}, question = {3} answer = {4}'.format(x[0],x[2],x[3],x[4],x[1]))
db.close()
