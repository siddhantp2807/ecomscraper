# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from scrapy.exceptions import NotConfigured

class EcomscraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveToMySQLPipeline:
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_config=crawler.settings.getdict('ITEMS_CONFIG')
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS item (
            id INT AUTO_INCREMENT PRIMARY KEY,
            itemName VARCHAR(500),
            itemLink VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

        self.cursor.execute("""
                            
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
        self.conn.commit()


    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):

        select_query = """
        SELECT id FROM item WHERE itemName = %s
        """
        self.cursor.execute(select_query, (item['itemName'],))
        existing_item = self.cursor.fetchone()

        if existing_item :
            
            item_id = existing_item[0]
            insert_query_detail = """
            INSERT INTO detail (availability, price, rating, noOfRatings, created_at, item_id)
            VALUES (%s, %s, %s, %s, NOW(), %s)
            """
            price = None if 'price' not in item else item['price']
            detail_data = (item['availability'], price, item['rating'], item['noOfRatings'], item_id)
            self.cursor.execute(insert_query_detail, detail_data)
        
        else :
            
            insert_query = """
            INSERT INTO item (itemName, itemLink, created_at)
            VALUES (%s, %s, NOW())
            """
            item_data = (item['itemName'], item['itemLink'])
            self.cursor.execute(insert_query, item_data)
            self.conn.commit()

            # Get the last inserted ID for the foreign key in the 'detail' table
            item_id = self.cursor.lastrowid

            insert_query_detail = """
            INSERT INTO detail (availability, price, rating, noOfRatings, created_at, item_id)
            VALUES (%s, %s, %s, %s, NOW(), %s)
            """
        
            price = None if 'price' not in item else item['price']
            detail_data = (item['availability'], price, item['rating'], item['noOfRatings'], item_id)
            self.cursor.execute(insert_query_detail, detail_data)
        
        self.conn.commit()

        return item


class MySQLStartUrlsPipeline:
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config

    @classmethod
    def from_crawler(cls, crawler):
        mysql_config = crawler.settings.getdict('LINKS_CONFIG')
        if not mysql_config:
            raise NotConfigured("LINKS_CONFIG not set")
        return cls(mysql_config)

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_spider_input(self, response, spider):
        pass

    def process_item(self, item, spider):
        return item

    def process_spider_exception(self, response, exception, spider):
        pass

    def spider_opened(self, spider):
        query = "SELECT url FROM links"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        spider.start_urls = [row[0] for row in result]
