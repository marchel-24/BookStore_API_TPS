import psycopg2
from flask import jsonify

class Wishlist:
    def __init__(self, wishlist_id, customer_id, store_id, book_id, date_make):
        self.wishlist_id = wishlist_id
        self.customer_id = customer_id
        self.store_id = store_id
        self.book_id = book_id
        self.date_make = date_make

    @staticmethod
    def make_wishlist(data, connection):
        wishlist = Wishlist(
            wishlist_id=data.get('wishlist_id'),
            customer_id=data.get('customer_id'),
            store_id=data.get('store_id'),
            book_id=data.get('book_id'),
            date_make=data.get('date_make')
        )

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT 1 FROM public."Whislist" WHERE "Whistlist_ID" = %s', (wishlist.wishlist_id,))
                    existing_wishlist = cursor.fetchone()
                    if existing_wishlist:
                        return jsonify({'status': 'fail', 'error': 'wishlist_id is already used'}), 400

                    cursor.execute('SELECT 1 FROM public."Book" WHERE "Book_ID" = %s', (wishlist.book_id,))
                    existing_book = cursor.fetchone()
                    if not existing_book:
                        return jsonify({'status': 'fail', 'error': 'Book is not defined'})

                    cursor.execute('SELECT 1 FROM public."Store" WHERE "ID_Store" = %s', (wishlist.store_id,))
                    existing_store = cursor.fetchone()
                    if not existing_store:
                        return jsonify({'status': 'fail', 'error': 'Store is not defined'})

                    cursor.execute('SELECT 1 FROM public."Customer" WHERE "ID_Customer" = %s', (wishlist.customer_id,))
                    existing_customer = cursor.fetchone()
                    if not existing_customer:
                        return jsonify({'status': 'fail', 'error': 'Customer is not registered'})

                    query = 'INSERT INTO public."Whislist" ("Whistlist_ID", "ID_Customer", "ID_Store", "ID_Book", "Date_Make") VALUES (%s, %s, %s, %s, %s)'
                    values = (wishlist.wishlist_id, wishlist.customer_id, wishlist.store_id, wishlist.book_id, wishlist.date_make)
                    cursor.execute(query, values)
                    connection.commit()

            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'fail', 'error': str(e)})
        
    @staticmethod
    def delete_wishlist(data, connection):
        wishlist_id = data.get("wishlist_id")

        if not wishlist_id:
            return jsonify({'status': 'fail', 'error': 'Wishlist_ID is required'}), 400
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT 1 FROM public."Whislist" WHERE "Whistlist_ID" = %s', (wishlist_id,))
                    wishlist_id_check = cursor.fetchone()
                    if not wishlist_id_check:
                        return jsonify({'status': 'fail', 'error': 'wishlist_id is not found'})
                    cursor.execute('DELETE FROM public."Whislist" WHERE "Whistlist_ID" = %s', (wishlist_id,))
                    connection.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'fail', 'error': str(e)}), 500
        
    @staticmethod
    def update_wishlist(data, connection):
        wishlist_id = data.get("wishlist_id")

        if not wishlist_id:
            return jsonify({'status': 'fail', 'error': 'Wishlist ID is required'}), 400
        
        update_fields = {}
        if 'ID_Book' in data:
            update_fields['ID_Book'] = data['ID_Book']
        if 'ID_Customer' in data:
            update_fields['ID_Customer'] = data['ID_Customer']
        if 'ID_Store' in data:
            update_fields['ID_Store'] = data['ID_Store']
        if 'date_make' in data:
            update_fields['Date_Make'] = data['date_make']

        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400

        set_clause = ", ".join([f'"{key}" = %s' for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(wishlist_id)

        query = f'UPDATE public."Whislist" SET {set_clause} WHERE "Whistlist_ID" = %s'
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT 1 FROM public."Whislist" WHERE "Whistlist_ID" = %s', (wishlist_id,))
                    wishlist_id_check = cursor.fetchone()
                    if not wishlist_id_check:
                        return jsonify({'status': 'fail', 'error': 'wishlist_id is not found'})
                    
                    cursor.execute(query, values)
                    connection.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'fail', 'error': str(e)})

