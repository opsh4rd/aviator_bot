import psycopg2

# Указывайте ваши данные
conn = psycopg2.connect(
    dbname="...",
    user="...",
    password="...",
    host="..."
)

cursor = conn.cursor()

# Создание таблицы для хранения чисел
cursor.execute('''
    CREATE TABLE IF NOT EXISTS numbers (
        id SERIAL PRIMARY KEY,
        number REAL
    )
''')

conn.commit()


# Вставка числа в таблицу
def insert_number(number):
    cursor.execute('INSERT INTO numbers (number) VALUES (%s)', (number,))
    conn.commit()
