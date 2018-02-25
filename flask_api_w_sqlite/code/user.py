import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM user WHERE username=?'
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            # Creates User instance from SQL response if found
            user = cls(*row) # Expands row into (row[n], row[n+1], row[n+2], ...)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM user WHERE id=?'
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            # Creates User instance from SQL response if found
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
            type=str,
            required=True,
            help='This must be a valid username.'
        )
        parser.add_argument('password',
            type=str,
            required=True,
            help='This must be a valid password.'
        )
        data = parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO user VALUES (NULL, ?, ?)'
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User "{}" created successfully.'.format(data['username'])}, 201
