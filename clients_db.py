import psycopg2

pass_db = ''

def create_db(conn): # Функция, создающая структуру БД (таблицы).
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
            DROP TABLE phones;
            DROP TABLE clients;
        """)

        # создание таблиц
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                sur_name VARCHAR(50),
                email VARCHAR(100)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                phone_number VARCHAR(25) PRIMARY KEY,
                client_id integer NOT NULL REFERENCES clients(id) ON DELETE CASCADE
            );
        """)

        conn.commit()  # фиксируем в БД

def add_phone(conn, client_id, phones):
    # Функция, позволяющая добавить телефон для существующего клиента.
    with conn.cursor() as cur:
        for phone in phones:
            cur.execute("""
                INSERT INTO phones(phone_number, client_id)
                VALUES (%s, %s)
            """, (phone, client_id))

        conn.commit()

        cur.execute("""
            SELECT * FROM phones
        """)
        print('Таблица phones:', cur.fetchall())

def add_client(conn, first_name, sur_name, email, phones=None):
    # Функция, позволяющая добавить нового клиента.
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(first_name, sur_name, email)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (first_name, sur_name, email))
        current_id = cur.fetchone()[0]
        print(current_id)

        conn.commit()

        cur.execute("""
            SELECT * FROM clients
        """)
        print('Таблица clients:', cur.fetchall())

        if phones is not None:
            add_phone(conn, current_id, phones)

def change_client(conn, client_id, first_name=None, sur_name=None, email=None):
    # Функция, позволяющая изменить данные о клиенте.
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                UPDATE clients SET first_name = %s WHERE id = %s
            """, (first_name, client_id))
        if sur_name is not None:
            cur.execute("""
                UPDATE clients SET sur_name = %s WHERE id = %s
            """, (sur_name, client_id))
        if email is not None:
            cur.execute("""
                UPDATE clients SET email = %s WHERE id = %s
            """, (email, client_id))

        conn.commit()

        cur.execute("""
            SELECT * FROM clients
        """)
        print('Таблица clients:', cur.fetchall())

def delete_phone(conn, phone):
    # Функция, позволяющая удалить телефон для существующего клиента.
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE phone_number like %s
        """, ('%'+phone+'%',))

        conn.commit()

        cur.execute("""
            SELECT * FROM phones
        """)
        print('Таблица phones:', cur.fetchall())

def delete_client(conn, client_id):
    # Функция, позволяющая удалить существующего клиента.
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients WHERE id = %s
        """, (client_id,))

        cur.execute("""
            SELECT * FROM phones
        """)
        print('Таблица phones после удаления:', cur.fetchall())

        cur.execute("""
            SELECT * FROM clients
        """)
        print('Таблица clients после удаления:', cur.fetchall())

with psycopg2.connect(database='clients_db', user='postgres', password=pass_db) as conn:
    create_db(conn)
    add_client(conn, 'Dmitrii', 'Selikhov', 'mail1@mail.ru', ['79261234567', '79035001122'])
    add_client(conn, 'Ivan', 'Matveev', 'Ivan1@mail.ru', ['79267774567'])
    add_client(conn, 'Lebron', 'James', 'Lebron@gmail.com', ['71012121234567'])
    add_phone(conn, 2, ['+79825002030'])
    change_client(conn, 2, first_name='Sergey')
    delete_phone(conn, '9035001122')
    delete_client(conn, 1)
conn.close()

print('Finish')
