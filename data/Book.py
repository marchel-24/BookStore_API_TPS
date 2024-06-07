import psycopg2
from flask import jsonify

class Book:
    def __init__(self, book_id, book_name, book_price, book_publish_year, publisher, language, ori_lang):
        self.book_id = book_id
        self.book_name = book_name
        self.book_price = book_price
        self.book_publish_year = book_publish_year
        self.publisher = publisher
        self.language = language
        self.ori_lang = ori_lang

    @staticmethod
    def insert_book(data, connection):
        book = Book(
            book_id=data.get('Book_ID'),
            book_name=data.get('Book_Title'),
            book_price=data.get('Book_Price'),
            book_publish_year=data.get('Book_Publish_Year'),
            publisher=data.get('ID_Publisher'),
            language=data.get('Language_ID'),
            ori_lang=data.get('Original_Language_ID')
        )
        
        author = data.get('Author')

        if not book.book_id or not book.book_name:
            return jsonify({'error': 'Book_ID and Book_Title are required'}), 400

        try:
            with connection:
                with connection.cursor() as cursor:
                    # Check if Book_ID or Book_Title already exists
                    cursor.execute('SELECT 1 FROM public."Book" WHERE "Book_ID" = %s OR "Book_Title" = %s', (book.book_id, book.book_name))
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
                    values = (book.book_id, book.book_name, book.book_price, book.book_publish_year, book.publisher, book.language, book.ori_lang)
                    cursor.execute(query, values)
                    
                    # Get the author ID
                    cursor.execute('SELECT "Author_ID" FROM public."Author" WHERE "Author_Name" = %s', (author,))
                    author_id = cursor.fetchone()[0]
                    
                    # Insert into Book_Author
                    query_author_book = f'INSERT INTO public."Book_Author" ("Book_Book_ID", "Author_Author_ID") VALUES (%s, %s)'
                    cursor.execute(query_author_book, (book.book_id, author_id))
                    
                    connection.commit()
            return jsonify({'status': 'success', 'query': query})
        except Exception as e:
            return jsonify({'status': 'fail', 'error': str(e)})

    @staticmethod
    def delete_book(data, connection):
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

    @staticmethod
    def get_book_profile(data, connection):
        book_title = data.get('Book_Title')
        if not book_title:
            return jsonify({'status': 'fail', 'error': 'Need Book Title'}), 400
        
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT "Book_ID", "Book_Title", "Book_Publish_Year", "Book_Price", "Original_Language_ID", "Language_ID", "ID_Publisher" FROM public."Book" WHERE "Book_Title" = %s', (book_title,))
                    book_row = cursor.fetchone()
                    if not book_row:
                        return jsonify({'status': 'fail', 'error': 'Book not found'}), 404

                    columns = ["Book_ID", "Book_Title", "Book_Publish_Year", "Book_Price", "Original_Language_ID", "Language_ID", "ID_Publisher"]
                    book_profile = dict(zip(columns, book_row))

            return jsonify({'status': 'success', 'book': book_profile})
        except Exception as e:
            return jsonify({'status': 'fail', 'error': str(e)}), 500
