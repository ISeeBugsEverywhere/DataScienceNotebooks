import random
import time
from typing import List, Union

class properties_of:
    """
    Klasė darbui su objektų savybėmis įvairiuose duomenų varikliuose (v17).

    Parametrai:
        - name (str): Objekto grupės pavadinimas.
        - engine (str): Naudojamas duomenų variklis ("pandas" arba "pyspark").
        - silent (bool): Jei True, nenaudojami išvesties pranešimai.

    Savybės:
        - property_type (DataFrame): Laikomi savybių tipai.
        - property (DataFrame): Laikomos objektų savybės.
        - file_path (str): Paskutiniu metu skaityto ar rašyto failo kelias.
        - file_format (str): Failo formatas (csv, parquet, feather).
        - opened_format (str): Atidarytas lentelės formatas ("wide" arba "narrow").

    Vieši metodai:
        - add_property_type(property_id: str, description: str) -> None
            Prideda naują savybių tipą.
        - add_property(object_id: str, property_id: str, value: Any) -> None
            Prideda arba atnaujina savybę konkrečiam objektui.
        - open_wide(file_path: str, file_format: str) -> None
            Perskaito plačią lentelę iš failo ir išsaugo failo informaciją.
        - open_narrow(file_path: str, file_format: str) -> None
            Perskaito siaurą lentelę iš failo ir išsaugo failo informaciją.
        - write_wide(file_path: str, file_format: str, columns: List[str] = []) -> None
            Išsaugo plačią lentelę į failą.
        - write_narrow(file_path: str, file_format: str, columns: List[str] = []) -> None
            Išsaugo siaurą lentelę į failą.
        - get_wide_df(columns: List[str] = []) -> DataFrame
            Grąžina plačią lentelę. Jei `columns` yra tuščias, grąžina visus stulpelius.
        - save() -> None
            Išsaugo duomenis į anksčiau perskaitytą failą (wide arba narrow).
        - close() -> None
            Uždaro PySpark sesiją ir atlaisvina atmintį (RAM).
    """

    def __init__(self, name: str, engine: str = "pandas", silent: bool = False) -> None:
        from typing import List
        import time

        self.name = name
        self.engine = engine
        self.silent = silent
        self.file_path = None
        self.file_format = None
        self.opened_format = None

        if engine == "pandas":
            import pandas as pd
            self.pd = pd
            self.property_type = pd.DataFrame(columns=["property_id", "description"])
            self.property = pd.DataFrame(columns=["id", "property_id", "value"])
        elif engine == "pyspark":
            from pyspark.sql import SparkSession
            self.spark = SparkSession.builder.appName("Properties").getOrCreate()
            self.property_type = self.spark.createDataFrame([], "property_id STRING, description STRING")
            self.property = self.spark.createDataFrame([], "id STRING, property_id STRING, value STRING")
        else:
            raise ValueError(f"Nežinomas variklis: {engine}")

    def _log(self, message: str) -> None:
        """Išveda pranešimą, jei silent=False."""
        if not self.silent:
            print(message)

    def add_property_type(self, property_id: str, description: str) -> None:
        """Prideda naują savybių tipą."""
        if self.engine == "pandas":
            new_row = self.pd.DataFrame({"property_id": [property_id], "description": [description]})
            self.property_type = self.pd.concat([self.property_type, new_row], ignore_index=True).drop_duplicates()
        elif self.engine == "pyspark":
            new_row = self.spark.createDataFrame([(property_id, description)], schema="property_id STRING, description STRING")
            self.property_type = self.property_type.union(new_row)

    def add_property(self, id: str, property_id: str, value: str) -> None:
        """Prideda arba atnaujina savybę konkrečiam objektui."""
        if self.engine == "pandas":
            condition = (self.property["id"] == id) & (self.property["property_id"] == property_id)
            if condition.any():
                self.property.loc[condition, "value"] = value
            else:
                new_row = self.pd.DataFrame({"id": [id], "property_id": [property_id], "value": [value]})
                self.property = self.pd.concat([self.property, new_row], ignore_index=True).drop_duplicates()
        elif self.engine == "pyspark":
            self.property = (
                self.property.filter(f"id != '{id}' OR property_id != '{property_id}'")
                .union(self.spark.createDataFrame([(id, property_id, value)], schema="id STRING, property_id STRING, value STRING"))
            )

    def open_narrow(self, file_path: str, file_format: str) -> None:
        """Perskaito siaurą lentelę iš failo."""
        start_time = time.time()
        self.file_path = file_path
        self.file_format = file_format
        self.opened_format = "narrow"
        if self.engine == "pandas":
            if file_format == "csv":
                self.property = self.pd.read_csv(file_path)
            elif file_format == "parquet":
                self.property = self.pd.read_parquet(file_path)
            elif file_format == "feather":
                self.property = self.pd.read_feather(file_path)
            else:
                raise ValueError("Nepalaikomas failo formatas.")
        elif self.engine == "pyspark":
            if file_format in ["csv", "parquet"]:
                self.property = self.spark.read.format(file_format).load(file_path)
            else:
                raise ValueError("Nepalaikomas failo formatas.")
        self._log(f"Siauros lentelės duomenys perskaityti per {time.time() - start_time:.2f}s.")

    def open_wide(self, file_path: str, file_format: str) -> None:
        """Perskaito plačią lentelę iš failo ir konvertuoja ją į siaurą."""
        start_time = time.time()
        self.file_path = file_path
        self.file_format = file_format
        self.opened_format = "wide"
        if self.engine == "pandas":
            if file_format == "csv":
                wide_df = self.pd.read_csv(file_path)
            elif file_format == "parquet":
                wide_df = self.pd.read_parquet(file_path)
            elif file_format == "feather":
                wide_df = self.pd.read_feather(file_path)
            else:
                raise ValueError("Nepalaikomas failo formatas.")
            narrow_df = wide_df.melt(id_vars="id", var_name="property_id", value_name="value")
            self.property = self.pd.concat([self.property, narrow_df], ignore_index=True).drop_duplicates()
        self._log(f"Plačios lentelės duomenys perskaityti per {time.time() - start_time:.2f}s.")

    def write_narrow(self, file_path: str, file_format: str, columns: List[str] = []) -> None:
        """Išsaugo siaurą lentelę į failą."""
        start_time = time.time()
        if self.engine == "pandas":
            narrow_df = self.property
            if columns:
                narrow_df = narrow_df[narrow_df["property_id"].isin(columns)]
            if file_format == "csv":
                narrow_df.to_csv(file_path, index=False)
            elif file_format == "parquet":
                narrow_df.to_parquet(file_path, index=False)
            elif file_format == "feather":
                narrow_df.to_feather(file_path)
            else:
                raise ValueError("Nepalaikomas failo formatas.")
        elif self.engine == "pyspark":
            if file_format in ["csv", "parquet"]:
                narrow_df = self.property
                narrow_df.write.mode("overwrite").format(file_format).save(file_path)
            else:
                raise ValueError("Nepalaikomas failo formatas.")
        self._log(f"Siauros lentelės duomenys išsaugoti į {file_path} per {time.time() - start_time:.2f}s.")

    def write_wide(self, file_path: str, file_format: str, columns: List[str] = []) -> None:
        """Išsaugo plačią lentelę į failą."""
        start_time = time.time()
        if self.engine == "pandas":
            wide_df = self.property.pivot(index="id", columns="property_id", values="value").reset_index()
            if columns:
                wide_df = wide_df[["id"] + columns]
            if file_format == "csv":
                wide_df.to_csv(file_path, index=False)
            elif file_format == "parquet":
                wide_df.to_parquet(file_path, index=False)
            elif file_format == "feather":
                wide_df.to_feather(file_path)
            else:
                raise ValueError("Nepalaikomas failo formatas.")
        self._log(f"Plačios lentelės duomenys išsaugoti į {file_path} per {time.time() - start_time:.2f}s.")

    def get_wide_df(self, columns: List[str] = []) -> "pd.DataFrame":
        """Grąžina plačią lentelę."""
        if self.engine == "pandas":
            wide_df = self.property.pivot(index="id", columns="property_id", values="value").reset_index()
            if columns:
                return wide_df[["id"] + columns]
            return wide_df
        else:
            raise NotImplementedError("get_wide_df palaikomas tik Pandas varikliui.")

    def save(self) -> None:
        """Išsaugo duomenis į anksčiau perskaitytą failą (wide arba narrow)."""
        if not self.file_path or not self.file_format or not self.opened_format:
            raise ValueError("Failo kelias, formatas ir formatas (wide/narrow) turi būti nustatyti per open_* metodus.")
        if self.opened_format == "narrow":
            self.write_narrow(self.file_path, self.file_format)
        elif self.opened_format == "wide":
            self.write_wide(self.file_path, self.file_format)
        else:
            raise ValueError("Nepalaikomas išsaugojimo formatas.")

    def close(self) -> None:
        """Uždaro PySpark sesiją ir sunaikina duomenų rėmelius."""
        if self.engine == "pandas":
            self.property = None
            self.property_type = None
        elif self.engine == "pyspark":
            self.spark.stop()
            self.property = None
            self.property_type = None
        self._log("Klasės resursai sėkmingai atlaisvinti.")

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