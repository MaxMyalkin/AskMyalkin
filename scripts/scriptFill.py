import sys
import MySQLdb as mdb
from time import gmtime, strftime
import random
from random import randrange
import string
import datetime


def time_gen():
    result = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    return result
 
def insert_user(cursor, id):
    password = 'password'+(format(id))
    last_login = time_gen()
    is_superuser = random.randint(0, 1)
    username = 'username'+(format(id))
    first_name = 'name'+(format(id))
    last_name = 'surname'+(format(id))
    email = username+'@mail.com'
    is_staff = random.randint(0, 1)
    is_active = random.randint(0, 1)
    date_joined = time_gen()
   # cursor.execute('INSERT INTO auth_user VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
    #               (id, password, last_login, is_superuser, username, first_name, last_name, email,
     #               is_staff, is_active, date_joined))
    cursor.execute('insert into ask_userprofile values (%s , %s , %s)',(id,id,0))
 
def insert_question(cursor, id):
    title = 'title'+(format(id))
    body = 'body'+(format(id))
    author = randrange(1, 10000)
    creation_date = time_gen()
    rating = randrange(-100, 100)
    cursor.execute("INSERT INTO ask_question (id,title,body,author_id,date,rating,counter) VALUES (%s, %s, %s, %s, %s , %s , %s )",(id, title, body, author, creation_date, rating, '0'))
 
 
def insert_answer(cursor, id):
    contents = 'answer'+(format(id))
    question = randrange(1, 100000)
    author = randrange(1, 10000)
    date = time_gen()
    correct = random.randint(0, 1)
    rating = randrange(-100,100)
    cursor.execute("INSERT INTO ask_answer VALUES (%s, %s, %s, %s, %s, %s, %s)",
    (id, contents,  author,question,  date, correct, rating))

def insert_comment_question(cursor,id):
     contents = 'comment on question'+(format(id))
     main = randrange(1,100000)
     author = randrange(1,10000)
     date = time_gen()
     cursor.execute("insert into ask_commentquest VALUES (%s , %s , %s , %s , %s)", (id , contents , author , main , date))

def insert_quest_tag(cursor,id):
     question_id = randrange(1,100000)
     tag_id = randrange(1, 100)
     cursor.execute("insert into ask_question_tags VALUES (%s , %s , %s )", (id , question_id , tag_id ))

def insert_tag(cursor,id):
     text = 'tag' + (format(id))
     cursor.execute("insert into ask_tag VALUES (%s , %s )", (id , text ))

def insert_comment_answer(cursor,id):
     contents = 'comment on asnwer '+(format(id))
     main = randrange(1,100000)
     author = randrange(1,10000)
     date = time_gen()
     cursor.execute("insert into ask_commentans VALUES (%s , %s , %s , %s , %s)", (id , contents , author , main , date))

def insert_likeans(cursor,id):
     main_id = randrange(1,1000000)
     type = randrange(0,1)
     author_id = randrange(1,10000)
     cursor.execute("insert into ask_likeans VALUES (%s , %s, %s, %s )", (id , type , author_id , main_id ))

def insert_likequest(cursor,id):
     main_id = randrange(1,100000)
     type = randrange(0,1)
     author_id = randrange(1,10000)
     cursor.execute("insert into ask_likequest VALUES (%s , %s,  %s,  %s )", (id , type , author_id , main_id ))

con = mdb.connect('localhost', 'ask-user', '19251925', 'ask_db')
 
with con:
    cur = con.cursor()
 
    #for x in xrange(1, 10001):
     #    insert_user(cur, x)

    #for x in xrange(1, 100000):
       # insert_question(cur, x)

    #for x in xrange(1, 1000000):
     #  insert_answer(cur, x)

    #for x in xrange(1, 600000):
     #   insert_comment_answer(cur, x)

    #for x in xrange(1, 400000):
     #   insert_comment_question(cur, x)

    #for x in xrange(1, 100):
     #    insert_tag(cur, x)

    #for x in xrange(1, 200000):
      #   insert_quest_tag(cur, x)

    #for x in xrange(1, 1000000):
       #  insert_likeans(cur, x)

    #for x in xrange(1, 1000000):
     #    insert_likequest(cur, x)