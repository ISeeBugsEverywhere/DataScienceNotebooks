import pandas as pd
import sqlite3
import inspect
from typing import Union

def df_to_sqlite(df: pd.DataFrame, db: Union[str, sqlite3.Connection], table_name: str = None) -> None:
    """
    Įrašo Pandas DataFrame į nurodytą SQLite3 duomenų bazę.

    Args:
        df (pd.DataFrame): Duomenys, kurie bus įrašyti į DB.
        db (Union[str, sqlite3.Connection]): Kelias į SQLite DB failą arba jau egzistuojantis ryšys.
        table_name (str, optional): Lentelės pavadinimas. Jei nenurodytas, bandoma naudoti kintamojo pavadinimą.

    Raises:
        ValueError: Jei lentelės pavadinimo nepavyksta nustatyti automatiškai.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Pateiktas objektas nėra DataFrame.")

    # Nustatome lentelės pavadinimą, jei jis nenurodytas
    if table_name is None:
        # Bandome atspėti kintamojo pavadinimą
        frame = inspect.currentframe().f_back
        table_name = next(
            (name for name, val in frame.f_globals.items() if val is df),
            None
        )
        if table_name is None:
            raise ValueError("Nepavyko nustatyti lentelės pavadinimo. Prašome jį nurodyti rankiniu būdu.")

    # Atidarome DB ryšį, jei reikia
    connection_provided = isinstance(db, sqlite3.Connection)
    connection = db if connection_provided else sqlite3.connect(db)

    try:
        # Įrašome duomenis į DB
        df.to_sql(table_name, connection, if_exists='replace', index=False)
        print(f"Lentelė '{table_name}' sėkmingai įrašyta į DB.")
    except Exception as e:
        print(f"Klaida įrašant lentelę '{table_name}': {e}")
        raise
    finally:
        # Uždaryti ryšį, jei jį atidarėme funkcijoje
        if not connection_provided:
            connection.close()

def sqlite_to_df(db: Union[str, sqlite3.Connection], table_name: str) -> pd.DataFrame:
    """
    Nuskaito lentelę iš SQLite DB ir grąžina ją kaip Pandas DataFrame.

    Args:
        db (Union[str, sqlite3.Connection]): Kelias į SQLite DB failą arba jau egzistuojantis ryšys.
        table_name (str): Lentelės pavadinimas, kurią reikia nuskaityti.

    Returns:
        pd.DataFrame: Nuskaityti duomenys kaip DataFrame.

    Raises:
        ValueError: Jei lentelės pavadinimas nepateiktas.
        Exception: Jei nuskaitymas nepavyko.
    """
    if not table_name:
        raise ValueError("Reikia nurodyti lentelės pavadinimą.")

    # Atidarome DB ryšį, jei reikia
    connection_provided = isinstance(db, sqlite3.Connection)
    connection = db if connection_provided else sqlite3.connect(db)

    try:
        # Skaitome lentelę į DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
        print(f"Lentelė '{table_name}' sėkmingai nuskaityta iš DB.")
        return df
    except Exception as e:
        print(f"Klaida skaitant lentelę '{table_name}': {e}")
        raise
    finally:
        # Uždaryti ryšį, jei jį atidarėme funkcijoje
        if not connection_provided:
            connection.close()

if __name__ == "__main__":
    # Sukuriame pavyzdinį DataFrame
    df_example = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["A", "B", "C"]
    })

    # Įrašome į SQLite DB
    db_path = "example.db"
    df_to_sqlite(df_example, db_path)

    # Nuskaitome lentelę atgal į DataFrame
    df_restored = sqlite_to_df(db_path, "df_example")
    print(df_restored)