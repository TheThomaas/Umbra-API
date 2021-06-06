import subprocess
import flask
from flask import request, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import Error
# import json

DATABASE = r"umbra.db"

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

"""
Creates a database connection to the SQLite database specified by db_file
:param db_file: database file
:return: Connection object or None
"""
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

"""
Transforms a cursor into a dict
"""
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/games', methods=['GET'])
def get_all():
    query = "SELECT * FROM games"

    conn = create_connection(DATABASE)

    if conn is not None:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("SELECT * FROM games")

        results = cur.execute(query).fetchall()
        return jsonify(results)
    else:
        return page_not_found(404)

@app.route('/api/v1/games/<int:id>', methods=['GET'])
def get_with_id(id):
    query = "SELECT * FROM games WHERE "
    to_filter = []

    if id:
        query += 'game_id = ' + str(id) + ';'
        to_filter.append(id)
    if not (id):
        return page_not_found(404)
    conn = create_connection(DATABASE)

    if conn is not None:
        conn.row_factory = dict_factory
        cur = conn.cursor()

        results = cur.execute(query).fetchall()
        return jsonify(results)
    else:
        return page_not_found(404)

@app.route('/api/v1/games/<int:id>/open', methods=['GET'])
def open_with_id(id):
    query = "SELECT * FROM games WHERE "
    to_filter = []

    if id:
        query += 'game_id = ' + str(id) + ';'
        to_filter.append(id)
    if not (id):
        return page_not_found(404)
    conn = create_connection(DATABASE)

    if conn is not None:
        conn.row_factory = dict_factory
        cur = conn.cursor()

        results = cur.execute(query).fetchall()
        subprocess.call([results[0]['path']])
        # subprocess.call([results[0]['path'], results[0]['arguments']])
        print("Program Closed")
        return jsonify(results)
    else:
        return page_not_found(404)

@app.route('/api/v1/games/<int:id>/<string:column>', methods=['GET'])
def get_column_with_id(id, column):
    query = "SELECT " + column + " FROM games WHERE "
    to_filter = []

    if id:
        query += 'game_id = ' + str(id) + ';'
        to_filter.append(id)
    if not (id):
        return page_not_found(404)
    conn = create_connection(DATABASE)

    if conn is not None:
        conn.row_factory = dict_factory
        cur = conn.cursor()

        try:
            results = cur.execute(query).fetchall()
            return jsonify(results)
        except Error:
            return page_not_found(404)
    else:
        return page_not_found(404)

@app.route('/api/v1/games/<int:id>/<string:column>', methods=['PUT'])
def update_column(id, column):
    if column != 'favorite':
        data = request.get_json()
        to_filter = []

        if id:
            query += 'game_id = ' + str(id) + ';'
            to_filter.append(id)
        if not (id):
            return page_not_found(404)

        if column != data[column]:
            return page_not_found(404)

        conn = create_connection(DATABASE)

        query = """ UPDATE games
                    SET """ + column + """ = """ + data[column] + """
                    WHERE
                        game_id = """ + str(id) + ";"

        if conn is not None:
            conn.row_factory = dict_factory
            cur = conn.cursor()

            results = cur.execute(query).fetchall()
            cur.execute("COMMIT;")
            return get_column_with_id(id, 'favorite')
        else:
            return page_not_found(404)
    else:
        return toggle_favorite(id)

@app.route('/api/v1/games/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    is_favorite_query = "SELECT favorite FROM games WHERE "
    to_filter = []

    if id:
        is_favorite_query += 'game_id = ' + str(id) + ';'
        to_filter.append(id)
    if not (id):
        return page_not_found(404)
    conn = create_connection(DATABASE)

    if conn is not None:
        conn.row_factory = dict_factory
        cur = conn.cursor()

        try:
            results = cur.execute(is_favorite_query).fetchall()
            result_int = int(results[0]['favorite'])
            is_favorite = str(1 - result_int)
        except Error:
            return page_not_found(404)
    else:
        return page_not_found(404)

    query = """ UPDATE games
                SET favorite = """ + is_favorite + """
                WHERE
                    game_id = """ + str(id) + ";"

    if conn is not None:
        conn.row_factory = dict_factory
        cur = conn.cursor()

        results = cur.execute(query).fetchall()
        cur.execute("COMMIT;")
        return get_column_with_id(id, 'favorite')
    else:
        return page_not_found(404)

app.run()