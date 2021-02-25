from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
import flask
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import json


app = Flask(__name__)
# connection = psycopg2.connect(dbname="pet_hotel_python",
#                             host="127.0.0.1",
#                             port="5432",)
# cursor = connection.cursor()

# try:
#     # Connect to an existing database
#     # connection = psycopg2.connect(user="connordetviler",
#     #                               host="127.0.0.1",
#     #                               port="5432",
#     #                               database="pet_hotel_python")

#     # # Create a cursor to perform database operations
#     # cursor = connection.cursor()
#     # Print PostgreSQL details
#     print("PostgreSQL server information")
#     print(connection.get_dsn_parameters(), "\n")
#     # Executing a SQL query
#     cursor.execute("SELECT version();")
#     # Fetch result
#     record = cursor.fetchone()
#     print("You are connected to - ", record, "\n")

# except (Exception, Error) as error:
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     if (connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World!</h1><p>From Python and Flask!</p>"

@app.route('/api/pets', methods=['GET'])
def api_pets():
    connection = psycopg2.connect(dbname="pet_hotel_python",
                            host="127.0.0.1",
                            port="5432",)

    cursor = connection.cursor()
    postgreSQL_select_Query = 'SELECT "pets".*, "owners".name AS owner FROM pets JOIN "owners" ON "pets".owner_id = "owners".id;'
    cursor.execute(postgreSQL_select_Query)
    # Selecting rows from mobile table using cursor.fetchall
    # pets = cursor.fetchall()
    response = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    # respond, status 200 is added for us
    table = jsonify(response)
    return table
    # return response

@app.route('/api/owners', methods=['GET'])
def api_owners():

    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM owners"
    # execute query
    cursor.execute(postgreSQL_select_Query)
    # Selecting rows from mobile table using cursor.fetchall
    owners = cursor.fetchall()
    # respond, status 200 is added for us
    return jsonify(owners)

@app.route('/api/pets', methods=['POST'])
def api_add():
    # print(request.form)
    name = request.get_json()['name']
    color = request.get_json()['color']
    breed = request.get_json()['breed']
    check_in = request.get_json()['check_in']
    owner_id = request.get_json()['owner_id']
    try:
        print('yay')
        connection = psycopg2.connect(dbname="pet_hotel_python",
                                host="127.0.0.1",
                                port="5432",)
        # Avoid getting arrays of arrays!
        print('yay 2')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        print('yay 3')
        insertQuery = "INSERT INTO pets (name, color, breed, check_in, owner_id) VALUES (%s, %s, %s, %s, %s)"
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, (name, color, breed, check_in, owner_id))
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "Pet inserted")
        # respond nicely
        result = {'status': 'CREATED'}
        return make_response(jsonify(result), 201)
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        if(connection):
            print("Failed to insert pet", error)
            # respond with error
            result = {'status': 'ERROR'}
            return make_response(jsonify(result), 500)
    finally:
        # closing database connection.
        if(connection):
            # clean up our connections
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


app.run()