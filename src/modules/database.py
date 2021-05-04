import sqlite3
import os
import io
from datetime import datetime, timezone


from src.modules.config import Config

CONFIG = Config("config.ini")

DEFAULT_PATH = os.path.join(CONFIG.USB_DIR, "database.sqlite3")
DEFAULT_BACKUP_PATH = DEFAULT_PATH + ".sql"

class Database():
    def __init__(self, path = DEFAULT_PATH):
        if (os.path.exists(path)):
            self.con = sqlite3.connect(path)
        else:
            self.con = sqlite3.connect(path)
            self.con.execute("""CREATE TABLE "sites" (
                "id"	INTEGER,
                "name"  INTEGER NOT NULL,
                "latitude"	TEXT NOT NULL,
                "longitude"	TEXT NOT NULL,
                "depth"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )""")

            self.con.execute("""CREATE TABLE "measurements" (
                "id"	INTEGER,
                "site"  INTEGER NOT NULL,
                "sensor"	TEXT NOT NULL,
                "timestamp"	TEXT NOT NULL,
                "type"	TEXT NOT NULL,
                "value"	REAL NOT NULL,
                "unit"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY(site) REFERENCES sites(id)
            )""")

        self.curs = self.con.cursor()

    def backup(self, path:str = DEFAULT_BACKUP_PATH):
        with io.open(path, 'w') as f:
            for linha in self.con.iterdump():
                f.write('%s\n' % linha)
            print('Backup performed successfully.')

    def log_data(self, site_id:int, responses:dict):
        sql_insert = """
                INSERT INTO measurements (
                    site, sensor, timestamp, type, value, unit) 
                VALUES (?, ?, ?, ?, ?, ?);
                """

        
        for sensor in responses: 
            try:
                for measurement in responses[sensor]:
                    # Insert data into database
                    print(measurement)
                    timestamp_iso8601 = datetime.fromtimestamp(measurement["timestamp"], timezone.utc).isoformat('T', 'milliseconds')
                    self.curs.execute(sql_insert, (site_id, sensor, str(timestamp_iso8601),
                        measurement["type"], measurement["value"], measurement["unit"]))
            except:
                print("Skipping Invalid Measurement...")

        self.con.commit()

    def add_site(self, name, latitude, longitude, depth):
        sql_insert = """
            INSERT INTO sites (
                name, latitude, longitude, depth)
            VALUES (?, ?, ?, ?);
            """
        self.curs.execute(sql_insert, (str(name), str(latitude), str(longitude), str(depth)))
        self.con.commit()

    def get_most_recent(self):
        keys = [
            "id",
            "site",
            "sensor",
            "timestamp",
            "type",
            "value",
            "unit"
        ]

        sql_query = f"""
            SELECT DISTINCT id, site, sensor, max(timestamp), type, value, unit 
            FROM measurements 
            GROUP BY type
            ;""" 


        #print(sql_query)
        # query = self.con.execute(sql_query).fetchall()
        # values = list(query.pop(0))
        # response = dict(zip(keys, values))
        # return response
        measurements = []

        query = self.con.execute(sql_query).fetchall()
        values = [list(measurement) for measurement in query]

        for measurement in values:
            measurements.append(dict(zip(keys, measurement)))

        return measurements

    def get_site_list(self):
        keys = [
            "id",
            "name",
            "latitude",
            "longitude",
            "depth"
        ]

        sql_query = """ 
            SELECT *
            FROM sites;
        """
        sites = []

        query = self.con.execute(sql_query).fetchall()
        values = [list(site) for site in query]

        for site in values:
            sites.append(dict(zip(keys, site)))

        return sites


DB = Database()