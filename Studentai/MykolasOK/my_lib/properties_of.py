import sqlite3
import pandas as pd
# from pyspark.sql import SparkSession
from typing import Union, Optional

class properties_of:
    def __init__(self, name: str, engine: str = "sqlite_memory", db_path: Optional[str] = None):
        """
        Inicijuoja objektą su pasirenkamu duomenų bazės "varikliu".

        :param name: Objekto pavadinimas (naudojamas lentelių pavadinimams kurti).
        :param engine: 
            - "sqlite_memory": SQLite laikoma atmintyje.
            - "sqlite_file": SQLite laikoma faile, reikia nurodyti `db_path`.
            - "pandas": Pandas DataFrame kaip duomenų bazė.
            - "pyspark": PySpark DataFrame kaip duomenų bazė.
        :param db_path: Naudojamas tik jei `engine="sqlite_file"`, nurodo SQLite failo kelią.
        """
        self.name = name
        self.engine = engine

        if engine == "sqlite_memory":
            self.conn = sqlite3.connect(":memory:")
            self.cursor = self.conn.cursor()
            self._create_tables()
        elif engine == "sqlite_file":
            if not db_path:
                raise ValueError("Jei pasirenkama 'sqlite_file', turi būti nurodytas 'db_path'.")
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self._create_tables()
        elif engine == "pandas":
            self.df_property = pd.DataFrame(columns=["object_id", "property_id", "value"])
            self.df_property_type = pd.DataFrame(columns=["property_id", "description"])
        elif engine == "pyspark":
            self.spark = SparkSession.builder.master("local").appName("PropertiesDB").getOrCreate()
            self.df_property = self.spark.createDataFrame([], schema="object_id STRING, property_id STRING, value STRING")
            self.df_property_type = self.spark.createDataFrame([], schema="property_id STRING, description STRING")
        else:
            raise ValueError("Nepalaikomas duomenų bazės variklis: pasirinkite 'sqlite_memory', 'sqlite_file', 'pandas' arba 'pyspark'.")

    def _create_tables(self) -> None:
        """Sukuriamos lentelės SQLite duomenų bazėje."""
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

    def add_property_type(self, property_id: str, description: str) -> None:
        """Pridedamas savybės tipas."""
        if self.engine == "pandas":
            if property_id not in self.df_property_type["property_id"].values:
                self.df_property_type = pd.concat([
                    self.df_property_type,
                    pd.DataFrame({"property_id": [property_id], "description": [description]})
                ], ignore_index=True)
        elif self.engine == "pyspark":
            existing = self.df_property_type.filter(f"property_id = '{property_id}'").count() > 0
            if not existing:
                new_row = self.spark.createDataFrame([(property_id, description)], schema="property_id STRING, description STRING")
                self.df_property_type = self.df_property_type.union(new_row)
        else:
            self.cursor.execute(f"""
                INSERT OR IGNORE INTO {self.name}_property_type (property_id, description)
                VALUES (?, ?)
            """, (property_id, description))
            self.conn.commit()

    def add_property(self, object_id: str, property_id: str, value: str, check_property_type: bool = False) -> None:
        """Pridedama savybė konkrečiam objektui."""
        if self.engine == "pandas":
            if check_property_type and property_id not in self.df_property_type["property_id"].values:
                raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            self.df_property = pd.concat([
                self.df_property,
                pd.DataFrame({"object_id": [object_id], "property_id": [property_id], "value": [value]})
            ], ignore_index=True).drop_duplicates(subset=["object_id", "property_id"])
        elif self.engine == "pyspark":
            if check_property_type:
                existing = self.df_property_type.filter(f"property_id = '{property_id}'").count() > 0
                if not existing:
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

    def get_properties(self) -> Union[pd.DataFrame, None]:
        """Grąžinami tik objekto savybių duomenys."""
        if self.engine == "pandas":
            return self.df_property
        elif self.engine == "pyspark":
            return self.df_property.toPandas()
        else:
            self.cursor.execute(f"SELECT * FROM {self.name}_property")
            rows = self.cursor.fetchall()
            return pd.DataFrame(rows, columns=["object_id", "property_id", "value"])

    def get_everything(self) -> Union[pd.DataFrame, None]:
        """Grąžinamos visos savybės su jų aprašymais."""
        if self.engine == "pandas":
            return self.df_property.merge(self.df_property_type, on="property_id", how="left")
        elif self.engine == "pyspark":
            return self.df_property.join(self.df_property_type, "property_id", "left").toPandas()
        else:
            self.cursor.execute(f"""
                SELECT p.object_id, p.property_id, pt.description, p.value
                FROM {self.name}_property p
                LEFT JOIN {self.name}_property_type pt
                ON p.property_id = pt.property_id
            """)
            rows = self.cursor.fetchall()
            return pd.DataFrame(rows, columns=["object_id", "property_id", "description", "value"])

    def close(self) -> None:
        """Uždaromas SQLite ryšys arba PySpark sesija."""
        if self.engine.startswith("sqlite"):
            self.conn.close()
        elif self.engine == "pyspark":
            self.spark.stop()


def main():
    # Demonstracija SQLite atmintyje
    obj_memory = properties_of("knyga", engine="sqlite_memory")
    obj_memory.add_property_type("title", "Pavadinimas")
    obj_memory.add_property_type("metai", "Išleidimo metai")
    obj_memory.add_property("aaa", "title", "Lapė Snapė")
    obj_memory.add_property("bbb", "title", "Mėnuo Juodaragis")
    obj_memory.add_property("ccc", "title", "Meškiukas")
    print(obj_memory.get_properties())
    print()
    print(obj_memory.get_everything())
    print()
    obj_memory.close()

    # Pandas DF demonstracija
    obj_pandas = properties_of("knyga", engine="pandas")
    obj_pandas.add_property_type("title", "Pavadinimas")
    obj_pandas.add_property_type("metai", "Išleidimo metai")
    obj_pandas.add_property("111-222-333", "title", "Panda Bamba")
    obj_pandas.add_property("222-333-111", "title", "Mėnuo Beragis")
    obj_pandas.add_property("333-111-222", "title", "Kurmis")
    obj_pandas.add_property("111-222-333", "metai", "1900")
    obj_pandas.add_property("222-333-111", "metai", "1999")
    obj_pandas.add_property("333-111-222", "metai", "2020")
    print(obj_pandas.get_properties())
    print()
    print(obj_pandas.get_everything())
    print()

    # PySpark DF demonstracija
    # obj_pyspark = properties_of("knyga", engine="pyspark")
    # obj_pyspark.add_property_type("title", "Pavadinimas")
    # obj_pyspark.add_property("111-222-333-PySp", "title", "Lapė Snapė")
    # obj_pyspark.df_property.show()


if __name__ == "__main__":
    main()