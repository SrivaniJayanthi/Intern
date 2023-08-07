import requests
from bs4 import BeautifulSoup
import mysql.connector

def scrape_and_store_to_mysql(url, database_name, table_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    release_data = []
    for release in soup.select('tr'):
        columns = release.find_all('td')
        if len(columns) >= 6:
            version = columns[0].get_text().strip()
            model = columns[1].get_text().strip()
            date = columns[2].get_text().strip()
            patch_link = columns[5].find('a')['href'] if columns[6].find('a') and columns[6].find('a')['href'].startswith(('http://', 'https://')) else None
            release_data.append((version, model, date, patch_link))

    if not release_data:
        print("No release data to scrape.")
        return

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Srivani@2003',
        database=database_name
    )

    cursor = conn.cursor()

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, version VARCHAR(50), model VARCHAR(50), release_date DATE, patch VARCHAR(255))"
    cursor.execute(create_table_query)
    conn.commit()

    insert_query = f"INSERT INTO {table_name} (version, model, release_date, patch) VALUES (%s, %s, %s, %s)"
    cursor.executemany(insert_query, release_data)
    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    url_to_scrape = "https://www.kernel.org/"
    db_name = "srivani_data"
    table_name = "kernel_release_two"
    scrape_and_store_to_mysql(url_to_scrape, db_name, table_name)
