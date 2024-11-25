import sqlite3
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame as PySparkDF


class properties_of:
    def __init__(self, name, db=":memory:"):
        """
        Inicijuoja objektą su SQLite, Pandas DataFrame arba PySpark DataFrame pagrindu.

        :param name: Objekto pavadinimas (naudojamas lentelių pavadinimams kurti).
        :param db:
            - ":memory:" arba str: SQLite failo kelias arba atmintyje laikoma duomenų bazė.
            - sqlite3.Connection: Egzistuojantis SQLite ryšys.
            - pandas.DataFrame: Tuščias arba užpildytas Pandas DataFrame.
            - pyspark.sql.DataFrame: Tuščias arba užpildytas PySpark DataFrame.
        """
        self.name = name

        if isinstance(db, pd.DataFrame):
            # Naudojamas Pandas DataFrame
            self.db_type = "dataframe"
            self.df_property = db if not db.empty else pd.DataFrame(columns=["object_id", "property_id", "value"])
            self.df_property_type = pd.DataFrame(columns=["property_id", "description"])
        elif isinstance(db, PySparkDF):
            # Naudojamas PySpark DataFrame
            self.db_type = "pyspark"
            self.spark = SparkSession.builder.getOrCreate()
            self.df_property = db if db else self.spark.createDataFrame([], schema="object_id STRING, property_id STRING, value STRING")
            self.df_property_type = self.spark.createDataFrame([], schema="property_id STRING, description STRING")
        elif isinstance(db, sqlite3.Connection):
            # Naudojamas esamas SQLite ryšys
            self.db_type = "sqlite"
            self.conn = db
            self.cursor = self.conn.cursor()
            self._create_tables()
        else:
            # Naudojamas SQLite failas arba ":memory:"
            self.db_type = "sqlite"
            self.conn = sqlite3.connect(db)
            self.cursor = self.conn.cursor()
            self._create_tables()

    def _create_tables(self):
        """Sukuriamos reikalingos lentelės SQLite duomenų bazėje."""
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.name}_property (
                object_id TEXT,
                property_id TEXT,
                value TEXT,
                PRIMARY KEY (object_id, property_id)
            )
        """)
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.name}_property_type (
                property_id TEXT PRIMARY KEY,
                description TEXT
            )
        """)
        self.conn.commit()

    def add_property_type(self, property_id, description):
        """Pridedamas savybės tipas."""
        if self.db_type == "dataframe":
            if property_id not in self.df_property_type["property_id"].values:
                self.df_property_type = pd.concat([
                    self.df_property_type,
                    pd.DataFrame({"property_id": [property_id], "description": [description]})
                ], ignore_index=True)
        elif self.db_type == "pyspark":
            if not self.df_property_type.filter(self.df_property_type.property_id == property_id).count():
                new_row = self.spark.createDataFrame([(property_id, description)], schema="property_id STRING, description STRING")
                self.df_property_type = self.df_property_type.union(new_row)
        else:
            self.cursor.execute(f"""
                INSERT OR IGNORE INTO {self.name}_property_type (property_id, description)
                VALUES (?, ?)
            """, (property_id, description))
            self.conn.commit()

    def add_property(self, object_id, property_id, value, check_property_type=False):
        """Pridedama savybė konkrečiam objektui."""
        if self.db_type == "dataframe":
            if check_property_type and property_id not in self.df_property_type["property_id"].values:
                raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            self.df_property = pd.concat([
                self.df_property,
                pd.DataFrame({"object_id": [object_id], "property_id": [property_id], "value": [value]})
            ], ignore_index=True).drop_duplicates(subset=["object_id", "property_id"])
        elif self.db_type == "pyspark":
            if check_property_type and not self.df_property_type.filter(self.df_property_type.property_id == property_id).count():
                raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            new_row = self.spark.createDataFrame([(object_id, property_id, value)], schema="object_id STRING, property_id STRING, value STRING")
            self.df_property = self.df_property.union(new_row)
        else:
            if check_property_type:
                self.cursor.execute(f"""
                    SELECT 1 FROM {self.name}_property_type WHERE property_id = ?
                """, (property_id,))
                if not self.cursor.fetchone():
                    raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            self.cursor.execute(f"""
                INSERT OR REPLACE INTO {self.name}_property (object_id, property_id, value)
                VALUES (?, ?, ?)
            """, (object_id, property_id, value))
            self.conn.commit()

    def close(self):
        """Uždaromas ryšys su duomenų baze, jei naudojama SQLite."""
        if self.db_type == "sqlite":
            self.conn.close()


def main():
    # SQLite testavimas
    print("SQLite Test")
    sqlite_test = properties_of("testas", db=":memory:")
    sqlite_test.add_property_type("name", "Vardas")
    sqlite_test.add_property("1", "name", "John")
    sqlite_test.close()

    # Pandas DF testavimas
    print("\nPandas Test")
    pandas_test = properties_of("testas", db=pd.DataFrame())
    pandas_test.add_property_type("name", "Vardas")
    pandas_test.add_property("1", "name", "Jane")
    print(pandas_test.df_property)

    # PySpark DF testavimas
    print("\nPySpark Test")
    spark = SparkSession.builder.appName("Test").getOrCreate()
    pyspark_test = properties_of("testas", db=spark.createDataFrame([], "object_id STRING, property_id STRING, value STRING"))
    pyspark_test.add_property_type("name", "Vardas")
    pyspark_test.add_property("1", "name", "Doe")
    pyspark_test.df_property.show()

if __name__ == "__main__":
    main()
