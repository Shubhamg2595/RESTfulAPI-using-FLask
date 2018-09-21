import sqlite3
from flask_restful import Resource,reqparse

class User:
    def __init__(self,_id,username,password):
        self.id=_id
        self.username=username
        self.password=password
    @classmethod
    def findByUsername(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query="select * from users where username=?"
        resultset=cursor.execute(query,(username,))
        #reason we passed username in '()' with a comma (,) is to tell
        # python that we actually want our result to be a tuple

        #NOW TO FECTH ONLY ONE ROW FROM RESULSET
        row=resultset.fetchone()

        if row: #only works if row got some data
            # user=cls(row[0],row[1],row[2])
            user=cls(*row)
        else:
            user=None
        return user

    @classmethod
    def findByUseId(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from users where id=?"
        resultset = cursor.execute(query, (_id,))
        # reason we passed username in '()' with a comma (,) is to tell
        # python that we actually want our result to be a tuple
        # NOW TO FECTH ONLY ONE ROW FROM RESULSET
        row = resultset.fetchone()
        if row:  # only works if row got some data
            # user=cls(row[0],row[1],row[2])
            user = cls(*row)
        else:
            user = None


    'now make appropriate changes to security class with appropriate methods'



'creating a class to addd new users directly'

'this method will be called,when we POST some data to the user register'
class UserRegistration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="password field cannot be left blank")

    def post(self):
        data=UserRegistration.parser.parse_args()

        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="insert into users values(null,?,?)"

        cursor.execute(query,(data['username'],data['password']))

        connection.commit()
        connection.close()

        return {"message":"user created successfully"}
