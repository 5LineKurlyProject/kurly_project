from django.core.management.base import BaseCommand
import sqlite3
import pandas as pd
import os


class Command(BaseCommand):
    help = "Import CSV data into SQLite database"

    def handle(self, *args, **options):
        # SQLite 데이터베이스 경로
        database_path = os.path.join(os.getcwd(), "db.sqlite3")
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # 테이블 생성
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            image_url TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductCategories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Products (id),
            FOREIGN KEY (category_id) REFERENCES Categories (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            review TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Products (id)
        )
        ''')

        conn.commit()

        # CSV 파일 경로
        csv_file_path = os.path.join(os.getcwd(), "data", "kurly_test_5.csv")
        data = pd.read_csv(csv_file_path)

        # 데이터 import
        category_mapping = {}
        category_name = '럭셔리뷰티'
        for index, row in data.iterrows():
            product_name = row['상품 이름']
            review = row['리뷰']
            image_url = row['이미지 url']
            # category_name = row['카테고리명']

            # Check if category exists
            if category_name not in category_mapping:
                cursor.execute('INSERT INTO Categories (category_name) VALUES (?)', (category_name,))
                conn.commit()
                category_id = cursor.lastrowid
                category_mapping[category_name] = category_id
            else:
                category_id = category_mapping[category_name]

            # Insert product
            cursor.execute('INSERT INTO Products (product_name, image_url) VALUES (?, ?)',
                           (product_name, image_url))
            conn.commit()

            # Map product to category
            product_id = cursor.lastrowid
            cursor.execute('INSERT INTO ProductCategories (product_id, category_id) VALUES (?, ?)',
                           (product_id, category_id))
            conn.commit()

            # Insert reviews
            cursor.execute('INSERT INTO Reviews (product_id, review) VALUES (?, ?)',
                           (product_id, review))
            conn.commit()

        conn.close()
        self.stdout.write(self.style.SUCCESS("CSV data imported successfully!"))
