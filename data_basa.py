import psycopg2
from faker import Faker
import random
import datetime

fake = Faker()

def create_connection():
    return psycopg2.connect(
        dbname='your_database',
        user='your_username',
        password='your_password',
        host='your_host',
        port='your_port'
    )

def load_authors(cursor, num_authors=100):
    authors = [(fake.name(),) for _ in range(num_authors)]
    cursor.executemany("INSERT INTO Authors (name) VALUES (%s)", authors)

def load_books(cursor, num_books=1000):
    cursor.execute("SELECT author_id FROM Authors")
    author_ids = [row[0] for row in cursor.fetchall()]
    books = [(fake.sentence(nb_words=4), random.choice(author_ids), fake.date_between(start_date='-10y', end_date='today')) for _ in range(num_books)]
    cursor.executemany("INSERT INTO Books (title, author_id, published_date) VALUES (%s, %s, %s)", books)

def load_members(cursor, num_members=500):
    members = [(fake.name(), fake.date_between(start_date='-5y', end_date='today')) for _ in range(num_members)]
    cursor.executemany("INSERT INTO Members (name, join_date) VALUES (%s, %s)", members)

def load_borrowing_records(cursor, num_records=5000):
    cursor.execute("SELECT book_id FROM Books")
    book_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT member_id FROM Members")
    member_ids = [row[0] for row in cursor.fetchall()]
    records = [(random.choice(book_ids), random.choice(member_ids), fake.date_between(start_date='-2y', end_date='today'), None if random.random() < 0.5 else fake.date_between(start_date='today', end_date='today')) for _ in range(num_records)]
    cursor.executemany("INSERT INTO BorrowingRecords (book_id, member_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)", records)

def main():
    connection = create_connection()
    cursor = connection.cursor()
    load_authors(cursor)
    load_books(cursor)
    load_members(cursor)
    load_borrowing_records(cursor)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()



oxirgi 6 oyda eng kop olingan kitob:
SELECT b.title AS book_title, COUNT(br.book_id) AS num_borrows
FROM Books b
INNER JOIN BorrowingRecords br ON b.book_id = br.book_id
WHERE br.borrow_date >= CURRENT_DATE - INTERVAL '6 month'
GROUP BY b.title
ORDER BY num_borrows DESC;

Eng kop kitob olgan azolar:\
SELECT m.name AS member_name, COUNT(br.member_id) AS num_borrows
FROM Members m
INNER JOIN BorrowingRecords br ON m.member_id = br.member_id
GROUP BY m.name
ORDER BY num_borrows DESC;

Kitoblar uchun ortacha qarz olish muddati:
SELECT AVG(EXTRACT(EPOCH FROM (CASE WHEN return_date IS NULL THEN CURRENT_DATE ELSE return_date END - borrow_date))) AS avg_duration_days
FROM BorrowingRecords;

