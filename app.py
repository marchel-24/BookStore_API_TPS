import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from data.Book import Book
from data.Wishlist import Wishlist


load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")

connection = psycopg2.connect(url)

# @app.route('/api/get_book', methods=['GET'])
# def get_book():
#     table_name = request.args.get('table_name')
#     if not table_name:
#         return jsonify({'error': 'Table name is required'}), 400

#     query = f"SELECT * FROM public.{table_name};"
#     try:
#         with connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query)
#                 rows = cursor.fetchall()
#                 columns = [desc[0] for desc in cursor.description]
#                 book_list = [dict(zip(columns, row)) for row in rows]
#         return jsonify(book_list)
#     except Exception as e:
#         return jsonify({'status': 'fail', 'error': str(e)})
    
    
@app.route('/api/create_table', methods=['POST'])
def create_table():
    data = request.json
    table_name = data.get('table_name')
    columns = data.get('columns')
    relations = data.get('relations', [])

    if not table_name or not columns:
        return jsonify({'error': 'Table name and columns are required'}), 400

    # Construct the column definitions
    column_definitions = []
    for column in columns:
        name = column.get('name')
        data_type = column.get('data_type')
        if not name or not data_type:
            return jsonify({'error': 'Each column must have a name and data_type'}), 400
        column_definitions.append(f"{name} {data_type}")

    # Construct the foreign key constraints
    for relation in relations:
        fk_column = relation.get('fk_column')
        ref_table = relation.get('ref_table')
        ref_column = relation.get('ref_column')
        if not fk_column or not ref_table or not ref_column:
            return jsonify({'error': 'Each relation must have fk_column, ref_table, and ref_column'}), 400
        column_definitions.append(f"FOREIGN KEY ({fk_column}) REFERENCES {ref_table} ({ref_column})")

    column_definitions_str = ", ".join(column_definitions)
    query = f"CREATE TABLE {table_name} ({column_definitions_str});"

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        return jsonify({'status': 'success', 'query': query})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})


@app.route('/api/get_book', methods=['GET'])
def get_book():
    data = request.get_json()
    table_name = data.get('table_name') if data else None
    if not table_name:
        return jsonify({'error': 'Table name is required'}), 400

    query = f'SELECT * FROM public."{table_name}";'
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                book_list = [dict(zip(columns, row)) for row in rows]
        return jsonify(book_list)
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})
    

@app.route('/api/get_book_profile', methods=['GET'])
def get_book_profile():
    data = request.get_json()
    return Book.get_book_profile(data, connection)

@app.route('/api/insert_book', methods=['POST'])
def insert_book():
    data = request.get_json()
    return Book.insert_book(data, connection)
    
@app.route('/api/delete_book', methods=['DELETE'])
def delete_book():
    data = request.get_json()
    return Book.delete_book(data, connection)

@app.route('/api/change_book_profile', methods = ['PUT'])
def change_book_profile():
    data = request.get_json()
    return Book.update_book(data, connection)

@app.route('/api/insert_wishlist', methods = ['POST'])
def insert_wishlist():
    data = request.get_json()
    return Wishlist.make_wishlist(data, connection)
    
@app.route('/api/delete_wishlist', methods = ['DELETE'])
def delete_wishlist():
    data = request.get_json()
    return Wishlist.delete_wishlist(data, connection)

@app.route('/api/update_wishlist', methods = ['PUT'])
def update_wishlist():
    data = request.get_json()
    return Wishlist.update_wishlist(data, connection)
            