import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request


CARI_BUKU = (
    """SELECT "Book_ID", "Book_Title", "Book_Publish_Year", "Book_Price", "Original_Language_ID", "Language_ID", "ID_Publisher" FROM public."Book";"""
    )

Buat_Table = (
    """CREATE TABLE public."Bebas"("Reviews") integer NOT NULL, PRIMARY KEY ("Reviews"));
    ALTER TABLE IF EXISTS public."Bebas"OWNER to postgres;"""
)

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")

connection = psycopg2.connect(url)

@app.get("/")
def home():
    return "Hello World"

@app.route('/api/get_book', method = ['POST'])
def get_book():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CARI_BUKU)
            book = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            book_list = [dict(zip(columns, book)) for book in book]
    return jsonify(book_list)

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

@app.route('/api/insert_customer', method= ['POST'])
def insert_customer():
    data = request.get_json()
