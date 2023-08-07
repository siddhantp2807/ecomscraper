from scrapy.commands import ScrapyCommand
import mysql.connector

class Command(ScrapyCommand):

    # command = "initdb"
    requires_project = True
    default_settings = { 'LOG_ENABLED': True }
        
    def run(self, args, opts):
        # Your initialization code here
        items_config = self.settings.getdict("ITEMS_CONFIG")
        links_config = self.settings.getdict("LINKS_CONFIG")

        db_config = {
            'host': items_config["host"],
            'user': items_config["user"],
            'password': items_config["password"]
        }

        try :
            connection = mysql.connector.connect(**db_config)
            print("Connected to MySQL server")
            print("Initializing database...")

            items_db = items_config['database']
            links_db = links_config['database']

            cursor = connection.cursor()
            
            items_query = "CREATE DATABASE IF NOT EXISTS {}".format(items_db)
            links_query = "CREATE DATABASE IF NOT EXISTS {}".format(links_db)
            cursor.execute(items_query)
            cursor.execute(links_query)
            connection.commit()

            print(f"Databases {items_db} and {links_db} created!")

            connection.database = items_db

            cursor.execute("""

            CREATE TABLE IF NOT EXISTS item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                itemName VARCHAR(500),
                itemLink VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            connection.commit()
            
            cursor.execute("""
            
            CREATE TABLE IF NOT EXISTS detail (
                id INT AUTO_INCREMENT PRIMARY KEY,
                availability BOOLEAN,
                price DECIMAL(10, 2),
                rating DECIMAL(3, 1),
                noOfRatings INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                item_id INT,
                FOREIGN KEY (item_id) REFERENCES item(id)
            );
            """)
            connection.commit()

            connection.database = links_db

            cursor.execute("""

            CREATE TABLE IF NOT EXISTS links (
                id INT AUTO_INCREMENT PRIMARY KEY,
                link VARCHAR(500),
                site VARCHAR(20)
            );               
            """)
            connection.commit()

        except mysql.connector.Error as err:
            print("Error: ", err)
        # ... Run your database initialization script ...

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print("MySQL connection closed")