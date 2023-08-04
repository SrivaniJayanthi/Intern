import time
import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup

def create_table(table_name, column_headers, connection):
    with connection.cursor() as cursor:
        column_defs = ', '.join([f'`{header}` VARCHAR(255)' for header in column_headers])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {column_defs})"
        cursor.execute(sql)

def store_data_in_mysql(data, table_name, connection):
    with connection.cursor() as cursor:
        for item in data:
            values = [item.get(header.lower(), '') for header in column_headers]
            
            placeholders = ', '.join(['%s'] * len(column_headers))
            sql = f"INSERT INTO {table_name} ({', '.join(column_headers)}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(values))
        
    connection.commit()


if __name__ == "__main__":
    url = "https://www.catalog.update.microsoft.com/Search.aspx?q=windows%2010"

    column_headers = ['Title', 'Products', 'Classification', 'Last Updated', 'Version', 'Size', 'Download']

    table_name = input("Enter the table name: ").strip()

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Srivani@2003',
        database='srivani_data'
    )

    try:
        create_table(table_name, column_headers, connection)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        driver = webdriver.Chrome(options=options) 

        driver.get(url)

        time.sleep(5)

        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')
        items = soup.find_all('div', class_='item-container')

        # Extract and STORE
        data_to_store = []
        for item in items:
            data = {}
            for header in column_headers:
                data[header.lower()] = item.find('div', class_=header.lower()).text.strip()
            data_to_store.append(data)

        print("Extracted Data:")
        for item in data_to_store:
            print(item)

        # Store data
        store_data_in_mysql(data_to_store, table_name, connection)
        print("Data stored successfully in the database!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()
