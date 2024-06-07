import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request


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
    

@app.route('/api/insert_book', methods=['POST'])
def insert_book():
    data = request.get_json()
    book_id = data.get('Book_ID')
    book_title = data.get('Book_Title')
    book_price = data.get('Book_Price')
    book_publish_year = data.get('Book_Publish_Year')
    publisher = data.get('ID_Publisher')
    language = data.get('Language_ID')
    ori_lang = data.get('Original_Language_ID')
    author = data.get('Author')

    if not book_id or not book_title:
        return jsonify({'error': 'Book_ID and Book_Title are required'}), 400

    try:
        with connection:
            with connection.cursor() as cursor:
                # Check if Book_ID or Book_Title already exists
                cursor.execute('SELECT 1 FROM public."Book" WHERE "Book_ID" = %s OR "Book_Title" = %s', (book_id, book_title))
                existing_book = cursor.fetchone()
                if existing_book:
                    return jsonify({'status': 'fail', 'error': 'Book_ID or Book_Title already exists'}), 400
                
                # Check if the author exists
                cursor.execute('SELECT 1 FROM public."Author" WHERE "Author_Name" = %s', (author,))
                existing_name = cursor.fetchone()
                if not existing_name:
                    return jsonify({'status': 'fail', 'error': 'Author name is not defined'}), 400
                
                # Insert the new book
                query = f'INSERT INTO public."Book" ("Book_ID", "Book_Title", "Book_Price", "Book_Publish_Year", "ID_Publisher", "Language_ID", "Original_Language_ID") VALUES (%s, %s, %s, %s, %s, %s, %s)'
                values = (book_id, book_title, book_price, book_publish_year, publisher, language, ori_lang)
                cursor.execute(query, values)
                
                # Get the author ID
                cursor.execute('SELECT "Author_ID" FROM public."Author" WHERE "Author_Name" = %s', (author,))
                author_id = cursor.fetchone()[0]
                
                # Insert into Book_Author
                query_author_book = f'INSERT INTO public."Book_Author" ("Book_Book_ID", "Author_Author_ID") VALUES (%s, %s)'
                cursor.execute(query_author_book, (book_id, author_id))
                
                connection.commit()
        return jsonify({'status': 'success', 'query': query})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)})
    
@app.route('/api/delete_book', methods=['DELETE'])
def delete_book():
    data = request.get_json()
    book_title = data.get('Book_Title')

    if not book_title:
        return jsonify({'error': 'Book_Title is required'}), 400

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT "Book_ID" FROM public."Book" WHERE "Book_Title" = %s', (book_title,))
                book_id_row = cursor.fetchone()
                if not book_id_row:
                    return jsonify({'status': 'fail', 'error': 'Book title not found'}), 404
                
                book_id = book_id_row[0]
                
                query_author = 'DELETE FROM public."Book_Author" WHERE "Book_Book_ID" = %s'
                query_book = 'DELETE FROM public."Book" WHERE "Book_ID" = %s'

                cursor.execute(query_author, (book_id,))
                cursor.execute(query_book, (book_id,))
                
                connection.commit()

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 500

# @app.route('/api/membuat_wishlist', methods = ['POST'])
# def make_wishlist():
#     data = request.get_json()
#     nama_customer =
            