import random
import time
from typing import List, Union

class properties_of:
    def __init__(self, name: str, engine: str = "pandas"):
        """
        Inicializuojama klasė. Palaikomi du varikliai: 'pandas' ir 'pyspark'.

        :param name: Objektų grupės pavadinimas.
        :param engine: Variklis ('pandas' arba 'pyspark').
        """
        self.name = name
        self.engine = engine

        if engine == "pandas":
            import pandas as pd
            self.pd = pd
            self.df_property = pd.DataFrame(columns=["id", "property_id", "value"])
            self.df_property_type = pd.DataFrame(columns=["property_id", "description"])
        elif engine == "pyspark":
            from pyspark.sql import SparkSession
            self.spark = SparkSession.builder.master("local").appName("PropertiesDB").getOrCreate()
            self.df_property = self.spark.createDataFrame([], schema="id STRING, property_id STRING, value STRING")
            self.df_property_type = self.spark.createDataFrame([], schema="property_id STRING, description STRING")
        else:
            raise ValueError("Nepalaikomas variklis: pasirinkite 'pandas' arba 'pyspark'.")

    def add_property_type(self, property_id: str, description: str) -> None:
        """
        Pridedamas naujas savybės tipas į tipų lentelę.

        :param property_id: Savybės ID.
        :param description: Savybės aprašymas.
        """
        if self.engine == "pandas":
            self.df_property_type = self.pd.concat([
                self.df_property_type,
                self.pd.DataFrame({"property_id": [property_id], "description": [description]})
            ], ignore_index=True).drop_duplicates(subset=["property_id"])
        elif self.engine == "pyspark":
            new_row = self.spark.createDataFrame([(property_id, description)], schema="property_id STRING, description STRING")
            self.df_property_type = self.df_property_type.union(new_row)

    def add_property(self, id: str, property_id: str, value: str, check_property_type: bool = False) -> None:
        """
        Pridedama savybė konkrečiam objektui.

        :param id: Objekto ID.
        :param property_id: Savybės ID.
        :param value: Savybės reikšmė.
        :param check_property_type: Tikrinti, ar savybės tipas egzistuoja.
        """
        if self.engine == "pandas":
            if check_property_type and property_id not in self.df_property_type["property_id"].values:
                raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            self.df_property = self.pd.concat([
                self.df_property,
                self.pd.DataFrame({"id": [id], "property_id": [property_id], "value": [value]})
            ], ignore_index=True).drop_duplicates(subset=["id", "property_id"])
        elif self.engine == "pyspark":
            if check_property_type:
                existing = self.df_property_type.filter(f"property_id = '{property_id}'").count() > 0
                if not existing:
                    raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")
            new_row = self.spark.createDataFrame([(id, property_id, value)], schema="id STRING, property_id STRING, value STRING")
            self.df_property = self.df_property.union(new_row)

    def import_from_wide(self, filepath: str, file_format: str, id_column: str = "id") -> None:
        """
        Importuoja duomenis iš plačios lentelės.

        :param filepath: Failo kelias.
        :param file_format: Failo formatas: 'csv', 'parquet', 'feather'.
        :param id_column: Objekto ID stulpelio pavadinimas.
        """
        start_time = time.time()
        if self.engine == "pandas":
            if file_format == "csv":
                wide_df = self.pd.read_csv(filepath)
            elif file_format == "parquet":
                wide_df = self.pd.read_parquet(filepath)
            elif file_format == "feather":
                wide_df = self.pd.read_feather(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su Pandas.")
            narrow_df = wide_df.melt(id_vars=id_column, var_name="property_id", value_name="value")
            self.df_property = self.pd.concat([self.df_property, narrow_df], ignore_index=True).drop_duplicates()
            rows = len(narrow_df)
        elif self.engine == "pyspark":
            if file_format in ["csv", "parquet"]:
                wide_df = self.spark.read.format(file_format).load(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su PySpark.")
            narrow_df = wide_df.selectExpr(f"{id_column} AS id", "stack(*) AS (property_id, value)")
            self.df_property = self.df_property.union(narrow_df)
            rows = narrow_df.count()
        print(f"Importuota {rows} eilučių iš {filepath}. Trukmė: {time.time() - start_time:.2f}s")

    def export_to_wide(self, filepath: str, file_format: str, id_column: str = "id") -> None:
        """
        Eksportuoja duomenis į plačią lentelę.

        :param filepath: Failo kelias.
        :param file_format: Failo formatas: 'csv', 'parquet', 'feather'.
        :param id_column: Objekto ID stulpelio pavadinimas.
        """
        start_time = time.time()
        if self.engine == "pandas":
            wide_df = self.df_property.pivot(index=id_column, columns="property_id", values="value").reset_index()
            if file_format == "csv":
                wide_df.to_csv(filepath, index=False)
            elif file_format == "parquet":
                wide_df.to_parquet(filepath, index=False)
            elif file_format == "feather":
                wide_df.to_feather(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su Pandas")
            rows = len(wide_df)
        elif self.engine == "pyspark":
            raise NotImplementedError("PySpark nepalaiko plačių lentelių eksporto.")
        print(f"Eksportuota {rows} eilučių į {filepath}. Trukmė: {time.time() - start_time:.2f}s")

    def import_from_narrow(self, filepath: str, file_format: str) -> None:
        """
        Importuoja duomenis iš siauros lentelės.

        :param filepath: Failo kelias.
        :param file_format: Failo formatas: 'csv', 'parquet', 'feather'.
        """
        start_time = time.time()
        if self.engine == "pandas":
            if file_format == "csv":
                new_data = self.pd.read_csv(filepath)
            elif file_format == "parquet":
                new_data = self.pd.read_parquet(filepath)
            elif file_format == "feather":
                new_data = self.pd.read_feather(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su Pandas")
            self.df_property = self.pd.concat([self.df_property, new_data], ignore_index=True).drop_duplicates()
            rows = len(new_data)
        elif self.engine == "pyspark":
            if file_format in ["csv", "parquet"]:
                new_data = self.spark.read.format(file_format).load(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su PySpark.")
            self.df_property = self.df_property.union(new_data)
            rows = new_data.count()
        print(f"Importuota {rows} eilučių iš {filepath}. Trukmė: {time.time() - start_time:.2f}s")

    def export_to_narrow(self, filepath: str, file_format: str) -> None:
        """
        Eksportuoja duomenis į siaurą lentelę.

        :param filepath: Failo kelias.
        :param file_format: Failo formatas: 'csv', 'parquet', 'feather'.
        """
        start_time = time.time()
        if self.engine == "pandas":
            if file_format == "csv":
                self.df_property.to_csv(filepath, index=False)
            elif file_format == "parquet":
                self.df_property.to_parquet(filepath, index=False)
            elif file_format == "feather":
                self.df_property.to_feather(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su Pandas.")
            rows = len(self.df_property)
        elif self.engine == "pyspark":
            if file_format in ["csv", "parquet"]:
                self.df_property.write.mode("overwrite").format(file_format).save(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su PySpark.")
            rows = self.df_property.count()
        print(f"Eksportuota {rows} eilučių į {filepath}. Trukmė: {time.time() - start_time:.2f}s")

    def import_from_file(self, filepath: str, file_format: str) -> None:
        """
        Importuoja duomenis iš failo.

        :param filepath: Failo kelias.
        :param file_format: Failo formatas: 'csv', 'parquet', 'feather', 'sqlite'.
        """
        start_time = time.time()
        if self.engine == "pandas":
            if file_format == "csv":
                self.df_property = self.pd.read_csv(filepath)
            elif file_format == "parquet":
                self.df_property = self.pd.read_parquet(filepath)
            elif file_format == "feather":
                self.df_property = self.pd.read_feather(filepath)
            elif file_format == "sqlite":
                import sqlite3
                with sqlite3.connect(filepath) as conn:
                    self.df_property = self.pd.read_sql(f"SELECT * FROM {self.name}_property", conn)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su Pandas.")
            rows = len(self.df_property)
        elif self.engine == "pyspark":
            if file_format in ["csv", "parquet"]:
                self.df_property = self.spark.read.format(file_format).load(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su PySpark.")
            rows = self.df_property.count()
        print(f"Importuota {rows} eilučių iš {filepath}. Trukmė: {time.time() - start_time:.2f}s")

    def export_to_file(self, filepath: str, file_format: str) -> None:
        """
        Eksportuoja duomenis į failą.

        :param filepath: Failo kelias.
        :param file_format: Failo formatas: 'csv', 'parquet', 'feather', 'sqlite'.
        """
        start_time = time.time()
        if self.engine == "pandas":
            if file_format == "csv":
                self.df_property.to_csv(filepath, index=False)
            elif file_format == "parquet":
                self.df_property.to_parquet(filepath, index=False)
            elif file_format == "feather":
                self.df_property.to_feather(filepath)
            elif file_format == "sqlite":
                import sqlite3
                with sqlite3.connect(filepath) as conn:
                    self.df_property.to_sql(f"{self.name}_property", conn, if_exists="replace", index=False)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su Pandas.")
            rows = len(self.df_property)
        elif self.engine == "pyspark":
            if file_format in ["csv", "parquet"]:
                self.df_property.write.mode("overwrite").format(file_format).save(filepath)
            else:
                raise ValueError(f"Failo formatas '{file_format}' nepalaikomas su PySpark.")
            rows = self.df_property.count()
        print(f"Eksportuota {rows} eilučių į {filepath}. Trukmė: {time.time()-start_time:.2f}s")

    def close(self) -> None:
        """Uždaroma PySpark sesija, jei naudojama."""
        if self.engine == "pyspark":
            self.spark.stop()

################################################################################### 

def main() -> None:
    import string
    import os

    # NATO fonetinės abėcėlės sąrašas
    nato_phonetic_alphabet = [
        "Alpha", "Bravo", "Charlie", "Delta", "Echo", 
        "Foxtrot", "Golf", "Hotel", "India", "Juliett", 
        "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", 
        "Quebec", "Romeo", "Sierra", "Tango", "Uniform", 
        "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"
    ]

    print("\nTestuojame Pandas variklį")
    pandas_obj = properties_of("pandas_test_objects", engine="pandas")

    # Sukuriamas savybių DF
    for phonetic in nato_phonetic_alphabet:
        pandas_obj.add_property_type(property_id=phonetic.lower(), description=f"Savybė {phonetic}")

    num_objects = 2_000
    print(f'Generuojami {num_objects} objektų su atsitiktinėmis savybėmis')
    for i in range(1, num_objects + 1):
        object_id = f"obj_{i}"
        for _ in range(3):  # Trijų savybių priskyrimas
            property_id = random.choice(nato_phonetic_alphabet).lower()
            value = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            pandas_obj.add_property(object_id, property_id, value)

    pandas_formats = ["csv", "parquet", "feather"]
    for fmt in pandas_formats:
        print(f'\n{fmt}')
        wide_filepath = f"pandas_test_wide.{fmt}"
        narrow_filepath = f"pandas_test_narrow.{fmt}"

        # print(f'Eksportuojame {wide_filepath}')
        pandas_obj.export_to_wide(wide_filepath, file_format=fmt)
        # print(f'Eksportuojame {narrow_filepath}')
        pandas_obj.export_to_narrow(narrow_filepath, file_format=fmt)

        # print(f'Importuojame {wide_filepath}')
        pandas_obj.import_from_wide(wide_filepath, file_format=fmt)
        # print(f'Importuojame {narrow_filepath}')
        pandas_obj.import_from_narrow(narrow_filepath, file_format=fmt)

    pandas_obj.close()

    print("\nTestuojame PySpark variklį (tik su narrow lentelėmis)")
    num_objects = 10
    print(f'Generuojami {num_objects} objektų su atsitiktinėmis savybėmis')
    pyspark_obj = properties_of("pyspark_test_objects", engine="pyspark")

    # Įrašomos savybės
    for phonetic in nato_phonetic_alphabet:
        pyspark_obj.add_property_type(property_id=phonetic.lower(), description=f"Savybė {phonetic}")

    for i in range(1, num_objects + 1):
        object_id = f"obj_{i}"
        for _ in range(3):  # Trijų savybių priskyrimas
            property_id = random.choice(nato_phonetic_alphabet).lower()
            value = ''.join(random.choices(string.ascii_letters+string.digits+string.punctuation,k=10))
            pyspark_obj.add_property(object_id, property_id, value)

    pyspark_formats = ["csv", "parquet"]
    for fmt in pyspark_formats:
        print(f'\n{fmt}')
        narrow_filepath = f"pyspark_test_narrow.{fmt}"

        # print(f'Eksportuojame {narrow_filepath}')
        pyspark_obj.export_to_narrow(narrow_filepath, file_format=fmt)

        # print(f'Importuojame {narrow_filepath}')
        pyspark_obj.import_from_narrow(narrow_filepath, file_format=fmt)

    pyspark_obj.close()

if __name__ == "__main__":
    main()