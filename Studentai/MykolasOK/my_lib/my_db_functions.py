import pandas as pd
import sqlite3
import inspect

def save_df_to_sqlite(df, db, table_name=None):
    """
    Įrašo Pandas DataFrame į nurodytą SQLite3 duomenų bazę.

    Args:
        df (pd.DataFrame): Duomenys, kurie bus įrašyti į DB.
        db (str arba sqlite3.Connection): Kelias į SQLite DB failą arba jau egzistuojantis ryšys.
        table_name (str, optional): Lentelės pavadinimas. Jei nenurodytas, bandoma naudoti kintamojo pavadinimą.
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
    finally:
        # Uždaryti ryšį, jei jį atidarėme funkcijoje
        if not connection_provided:
            connection.close()

# Naudojimo pavyzdys
if __name__ == "__main__":
    # Sukuriame pavyzdinį DataFrame
    df_example = pd.DataFrame({
        "id": [10, 20, 30],
        "name": ["Aa", "Bb", "Cc"]
    })

    # Įrašome į SQLite DB failą
    save_df_to_sqlite(df_example, "./example.db")
