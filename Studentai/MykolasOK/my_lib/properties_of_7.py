import sqlite3
import pandas as pd
# from pyspark.sql import SparkSession
from typing import List, Optional, Union


class properties_of:
    def __init__(self, name: str, engine: str = "sqlite_memory", db_path: Optional[str] = None):
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
        # elif engine == "pyspark":
        #     self.spark = SparkSession.builder.master("local").appName("PropertiesDB").getOrCreate()
        #     self.df_property = self.spark.createDataFrame([], schema="object_id STRING, property_id STRING, value STRING")
        #     self.df_property_type = self.spark.createDataFrame([], schema="property_id STRING, description STRING")
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

    def add_property(self, object_id: str, property_id: str, value: str, check_property_type: bool = False) -> None:
        """Pridedama savybė konkrečiam objektui."""
        if self.engine == "pandas":
            if check_property_type and property_id not in self.df_property_type["property_id"].values:
                raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            self.df_property = pd.concat([
                self.df_property,
                pd.DataFrame({"object_id": [object_id], "property_id": [property_id], "value": [value]})
            ], ignore_index=True).drop_duplicates(subset=["object_id", "property_id"])
        # elif self.engine == "pyspark":
        #     if check_property_type:
        #         existing = self.df_property_type.filter(f"property_id = '{property_id}'").count() > 0
        #         if not existing:
        #             raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
        #     new_row = self.spark.createDataFrame([(object_id, property_id, value)], schema="object_id STRING, property_id STRING, value STRING")
        #     self.df_property = self.df_property.union(new_row)
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

    def import_from_df(self, df: pd.DataFrame, id: str = "id") -> None:
        """Importuoja savybes iš Pandas DataFrame į duomenų bazę."""
        for _, row in df.iterrows():
            object_id = row[id]
            for property_id, value in row.drop(id).items():
                self.add_property(id, property_id, value)

    def export_to_df(self, properties: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Eksportuoja savybes į Pandas DataFrame.

        :param properties: Savybių sąrašas. Jei `None`, grąžina visas savybes.
        :return: Pandas DataFrame su kiekvienai savybei atskiru stulpeliu.
        """
        if self.engine == "pandas":
            df = self.df_property.pivot(index="id", columns="property_id", values="value").reset_index()
        # elif self.engine == "pyspark":
        #     df = self.df_property.toPandas().pivot(index="id", columns="property_id", values="value").reset_index()
        else:
            self.cursor.execute(f"SELECT * FROM {self.name}_property")
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=["id", "property_id", "value"]).pivot(index="object_id", columns="property_id", values="value").reset_index()

        if properties:
            all_columns = ["id"] + properties
            df = df.reindex(columns=all_columns, fill_value=None)

        return df

    def close(self) -> None:
        """Uždaromas SQLite ryšys arba PySpark sesija."""
        if self.engine.startswith("sqlite"):
            self.conn.close()
        # elif self.engine == "pyspark":
        #     self.spark.stop()


def main() -> None:
    # Testavimas
    obj = properties_of("knyga", engine="sqlite_memory")

    # Test import_from_df
    data = pd.DataFrame({
        "id": ["111-222-333", "222-333-444"],
        "title": ["Lapė Snapė", "Vilkas Pilkas"],
        "author": ["Jojas Papievis", "Antanas Antanaitis"],
        "year": ["2020", "1900"]
    })
    obj.import_from_df(data)

    # Test export_to_df
    print("Eksportuotos savybės:")
    print(obj.export_to_df())

    # Eksportuojame tik konkrečias savybes
    print("Tik 'title' ir 'year':")
    print(obj.export_to_df(properties=["title", "year"]))

    obj.close()


if __name__ == "__main__":
    main()
