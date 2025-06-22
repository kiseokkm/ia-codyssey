import csv
import mysql.connector
from datetime import datetime
import os

def read_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = [row for row in reader]
    return rows

def insert_data_to_mysql(data):
    password = os.getenv('MYSQL_PW')

    if password is None:
        print('MYSQL_PW 환경변수가 설정되어 있지 않습니다.')
        return

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='mars'
    )
    cursor = connection.cursor()

    for row in data:
        mars_date = datetime.strptime(row[1], '%Y-%m-%d')
        temp = int(float(row[2]))
        storm = int(row[3])
        cursor.execute(
            'INSERT INTO mars_weather (mars_date, temp, storm) VALUES (%s, %s, %s)',
            (mars_date, temp, storm)
        )

    connection.commit()
    cursor.close()
    connection.close()
    print('데이터 삽입 완료')

if __name__ == '__main__':
    csv_path = 'mars_weathers_data.CSV'
    rows = read_csv_file(csv_path)
    insert_data_to_mysql(rows)
