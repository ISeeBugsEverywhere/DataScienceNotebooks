import sqlite3
import pandas as pd
from pyspark.sql import SparkSession
from typing import List, Optional, Union
# 2024-12-05 (nauja versija)

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
            self.df_property = pd.DataFrame(columns=["id", "property_id", "value"])
            self.df_property_type = pd.DataFrame(columns=["property_id", "description"])
        elif engine == "pyspark":
            self.spark = SparkSession.builder.master("local").appName("PropertiesDB").getOrCreate()
            self.df_property = self.spark.createDataFrame([], schema="id STRING, property_id STRING, value STRING")
            self.df_property_type = self.spark.createDataFrame([], schema="property_id STRING, description STRING")
        else:
            raise ValueError("Nepalaikomas duomenų bazės variklis: pasirinkite 'sqlite_memory', 'sqlite_file', 'pandas' arba 'pyspark'.")

    def _create_tables(self) -> None:
        """Sukuriamos lentelės SQLite duomenų bazėje."""
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.name}_property (
                id TEXT,
                property_id TEXT,
                value TEXT,
                PRIMARY KEY (id, property_id)
            )
        """)
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.name}_property_type (
                property_id TEXT PRIMARY KEY,
                description TEXT
            )
        """)
        self.conn.commit()

    def add_property(self, id: str, property_id: str, value: str, check_property_type: bool = False) -> None:
        """Pridedama savybė konkrečiam objektui."""
        if self.engine == "pandas":
            if check_property_type and property_id not in self.df_property_type["property_id"].values:
                raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            self.df_property = pd.concat([
                self.df_property,
                pd.DataFrame({"id": [id], "property_id": [property_id], "value": [value]})
            ], ignore_index=True).drop_duplicates(subset=["id", "property_id"])
        elif self.engine == "pyspark":
            if check_property_type:
                existing = self.df_property_type.filter(f"property_id = '{property_id}'").count() > 0
                if not existing:
                    raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            new_row = self.spark.createDataFrame([(id, property_id, value)], schema="id STRING, property_id STRING, value STRING")
            self.df_property = self.df_property.union(new_row)
        else:
            if check_property_type:
                self.cursor.execute(f"""
                    SELECT 1 FROM {self.name}_property_type WHERE property_id = ?
                """, (property_id,))
                if not self.cursor.fetchone():
                    raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            self.cursor.execute(f"""
                INSERT OR REPLACE INTO {self.name}_property (id, property_id, value)
                VALUES (?, ?, ?)
            """, (id, property_id, value))
            self.conn.commit()

    def export_to_narrow(self) -> pd.DataFrame:
        """
        Eksportuoja savybes į siauro formato Pandas DataFrame.

        :return: Pandas DataFrame su stulpeliais ['id', 'property_id', 'value'].
        """
        if self.engine == "pandas":
            return self.df_property.copy()
        elif self.engine == "pyspark":
            return self.df_property.toPandas()
        else:
            self.cursor.execute(f"SELECT * FROM {self.name}_property")
            rows = self.cursor.fetchall()
            return pd.DataFrame(rows, columns=["id", "property_id", "value"])

    def import_from_narrow(self, df: pd.DataFrame) -> None:
        """
        Importuoja siauro formato Pandas DataFrame į duomenų bazę.

        :param df: Pandas DataFrame su stulpeliais ['id', 'property_id', 'value'].
        """
        for _, row in df.iterrows():
            self.add_property(row["id"], row["property_id"], row["value"])

    def export_to_wide(self, properties: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Eksportuoja savybes į platų Pandas DataFrame.

        :param properties: Savybių sąrašas. Jei `None`, grąžina visas savybes.
        :return: Pandas DataFrame su kiekvienai savybei atskiru stulpeliu.
        """
        df_narrow = self.export_to_narrow()
        df = df_narrow.pivot(index="id", columns="property_id", values="value").reset_index()

        if properties:
            all_columns = ["id"] + properties
            df = df.reindex(columns=all_columns, fill_value=None)

        return df

    def import_from_wide(self, df: pd.DataFrame) -> None:
        """
        Importuoja savybes iš plataus Pandas DataFrame.

        :param df: Pandas DataFrame su stulpeliais: `id`, savybės ir jų reikšmės.
        """
        id_col = "id"
        for _, row in df.iterrows():
            for property_id, value in row.drop(labels=[id_col]).items():
                if pd.notna(value):
                    self.add_property(row[id_col], property_id, value)

    def close(self) -> None:
        """Uždaromas SQLite ryšys arba PySpark sesija."""
        if self.engine.startswith("sqlite"):
            self.conn.close()
        elif self.engine == "pyspark":
            self.spark.stop()


def main() -> None:
    # Testavimas
    obj = properties_of("knyga", engine="sqlite_memory")

    # Test import_from_wide
    data = pd.DataFrame({
        "id": ["111-222-333", "222-333-444"],
        "title": ["Lapė Snapė", "Vilkas Pilkas"],
        "author": ["Jojas Papievis", "Antanas Antanaitis"],
        "year": ["2020", "1900"]
    })
    obj.import_from_wide(data)

    # Eksportavimas į siaurą lentelę
    narrow = obj.export_to_narrow()
    print("Siauras formatas:")
    print(narrow)

    # Importavimas iš siauro formato
    obj.import_from_narrow(narrow)

    # Eksportas į platų formatą
    print("Platus formatas:")
    print(obj.export_to_wide())

    obj.close()


if __name__ == "__main__":
    main()
