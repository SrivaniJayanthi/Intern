import requests
from bs4 import BeautifulSoup
import mysql.connector

def scrape_data():
    url = "https://www.php.net/releases/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    releases = []
    for h2_tag in soup.find_all("h2"):
        model = h2_tag.text.strip()
        release_date = h2_tag.find_next("ul").find("li").text.strip()
        patch = h2_tag.find_next("ul").find_next("ul").find("a")["href"].strip()
        releases.append((model, release_date, patch))

    return releases

def create_table(table_name, cursor):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        model VARCHAR(255),
        release_date TEXT,
        patch VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)

def insert_data(table_name, data, cursor):
    insert_query = f"""
    INSERT INTO {table_name} (model, release_date, patch)
    VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_query, data)

def main():
    table_name = input("Enter the table name: ")
    data = scrape_data()
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Srivani@2003",
            database="srivani_data"
        )
        cursor = connection.cursor()
        create_table(table_name, cursor)
        insert_data(table_name, data, cursor)
        connection.commit()
        connection.close()
        print("Data scraped and stored successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
