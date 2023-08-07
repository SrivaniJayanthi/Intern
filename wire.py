import requests
from bs4 import BeautifulSoup
import pymysql

def scrape_and_store_to_mysql(url, database_name, table_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    release_data = []
    for release in soup.select('tr'):
        columns = release.find_all('td')
        if len(columns) >= 3:
            version = columns[1].get_text().strip()
            last_modified = columns[2].get_text().strip()
            release_data.append((version, last_modified))

    if not release_data:
        print("No release data to scrape.")
        return

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Srivani@2003',
        database=database_name
    )

    cursor = conn.cursor()
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (Version VARCHAR(100), LastModified VARCHAR(50))"
    cursor.execute(create_table_query)
    conn.commit()

    insert_query = f"INSERT INTO {table_name} (Version, LastModified) VALUES (%s, %s)"
    cursor.executemany(insert_query, release_data)
    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    url_to_scrape = "https://2.na.dl.wireshark.org/src/all-versions/?C=M;O=A"

    db_name = "srivani_data"
    table_name = "wireshark_releases"

    scrape_and_store_to_mysql(url_to_scrape, db_name, table_name)