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

def find_client(conn, first_name=None, sur_name=None, email=None, phone=None):
    # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    if first_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM clients WHERE first_name like %s
            """, ('%'+first_name+'%', ))
            res = cur.fetchall()
            if len(res) > 0:
                print(f'Результат поиска клиента с именем {first_name}:', res)
                current_id = res[0][0]
                cur.execute("""
                    SELECT phone_number FROM phones WHERE client_id = %s
                """, (current_id, ))
                print('Его телефоны:', cur.fetchall())
            else:
                print(f'Нет такого клиента ({first_name})')

    if sur_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM clients WHERE sur_name like %s
            """, ('%'+sur_name+'%', ))
            res = cur.fetchall()
            if len(res) > 0:
                print(f'Результат поиска клиента с Фамилией {sur_name}:', res)
                current_id = res[0][0]
                cur.execute("""
                    SELECT phone_number FROM phones WHERE client_id = %s
                """, (current_id, ))
                print('Его телефоны:', cur.fetchall())
            else:
                print(f'Нет такого клиента ({sur_name})')

    if email is not None:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM clients WHERE email like %s
            """, (email, ) )
            res = cur.fetchall()
            if len(res) > 0:
                print(f'Результат поиска клиента с почтой {email}:', res)
                current_id = res[0][0]
                cur.execute("""
                    SELECT phone_number FROM phones WHERE client_id = %s
                """, (current_id, ))
                print('Его телефоны:', cur.fetchall())
            else:
                print(f'Нет такого клиента ({email})')

    if phone is not None:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM phones WHERE phone_number like %s
            """, ('%'+phone+'%', ) )
            res = cur.fetchall()
            # print('phone!!!!', res[0][1])
            if len(res) > 0:
                cur.execute("""
                    SELECT * FROM clients WHERE id = %s
                """, (res[0][1],))
                print(f'Телефон {phone} принадлежит клиенту', cur.fetchall())
            else:
                print(f'Нет клиента с номером телефона ({phone})')


with psycopg2.connect(database='clients_db', user='postgres', password=pass_db) as conn:
    create_db(conn)
    add_client(conn, 'Dmitrii', 'Selikhov', 'mail1@mail.ru', ['79261234567', '79035001122'])
    add_client(conn, 'Ivan', 'Matveev', 'Ivan1@mail.ru', ['79267774567'])
    add_client(conn, 'Lebron', 'James', 'Lebron@gmail.com', ['71012121234567'])
    add_phone(conn, 2, ['79825002030'])
    change_client(conn, 2, first_name='Sergey')
    delete_phone(conn, '9035001122')
    delete_client(conn, 1)
    find_client(conn, first_name='Sergey')
    find_client(conn, first_name='Vasya')
    find_client(conn, sur_name='Matveev')
    find_client(conn, email='Lebron@gmail.com')
    find_client(conn, phone='9825002030')
    find_client(conn, phone='9825002031')
conn.close()

print('Finish')
