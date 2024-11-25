import sqlite3
import pandas as pd

# Nornt naudoti šią biblioteką reikią nurodyti:
# import sqlite3
# import pandas as pd
# from lib.properties_of import properties_of

class properties_of:
    def __init__(self, name, db_path=":memory:"):
        self.name = name

        # Patikrina, ar `db_path` yra ryšio objektas
        if isinstance(db_path, sqlite3.Connection):
            self.conn = db_path
            self.external_connection = True  # Nenaikinti ryšio uždarant
        else:
            self.conn = sqlite3.connect(db_path)
            self.external_connection = False  # Sukurtas naujas ryšys

        self.cursor = self.conn.cursor()

        # Lentelių pavadinimai
        self.property_table = f"{self.name}_property"
        self.property_type_table = f"{self.name}_property_type"

        # Sukuria lenteles, jei nėra
        self._create_tables()

    def _create_tables(self):
        """Sukuria reikalingas lenteles."""
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.property_table} (
                object_id TEXT,
                property_id TEXT,
                value TEXT,
                PRIMARY KEY (object_id, property_id)
            )
        """)

        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.property_type_table} (
                property_id TEXT PRIMARY KEY,
                description TEXT
            )
        """)
        self.conn.commit()

    def add_property_type(self, property_id, description):
        """Prideda savybės tipą."""
        self.cursor.execute(f"""
            INSERT OR IGNORE INTO {self.property_type_table} (property_id, description)
            VALUES (?, ?)
        """, (property_id, description))
        self.conn.commit()

    def add_property(self, object_id, property_id, value, check_property_type=False):
        """Prideda savybę konkrečiam objektui."""
        if check_property_type:
            self.cursor.execute(f"""
                SELECT 1 FROM {self.property_type_table} WHERE property_id = ?
            """, (property_id,))
            if not self.cursor.fetchone():
                raise ValueError(f"Savybės ID '{property_id}' nėra savybių tipų lentelėje.")

        self.cursor.execute(f"""
            INSERT OR REPLACE INTO {self.property_table} (object_id, property_id, value)
            VALUES (?, ?, ?)
        """, (object_id, property_id, value))
        self.conn.commit()

    def get_all_properties(self):
        """Gauna visas savybes visiems objektams."""
        self.cursor.execute(f"""
            SELECT p.object_id, pt.property_id, pt.description, p.value
            FROM {self.property_table} p
            JOIN {self.property_type_table} pt
            ON p.property_id = pt.property_id
        """)
        return [
            {"object_id": row[0], "property_id": row[1], "description": row[2], "value": row[3]}
            for row in self.cursor.fetchall()
        ]

    def get_properties_as_dataframe(self, properties):
        """
        Grąžina Pandas DataFrame su nurodytomis savybėmis.

        :param properties: Savybių ID sąrašas.
        :return: Pandas DataFrame su stulpeliais: objekto ID ir nurodytų savybių reikšmėmis.
        """
        # Sukuria dinaminę SQL užklausą
        query = f"""
            SELECT object_id, property_id, value
            FROM {self.property_table}
            WHERE property_id IN ({','.join(['?'] * len(properties))})
        """
        self.cursor.execute(query, properties)
        rows = self.cursor.fetchall()

        # Jei nėra duomenų, grąžina tuščią DataFrame
        if not rows:
            return pd.DataFrame(columns=["object_id"] + properties)

        # Sukuria DataFrame
        df = pd.DataFrame(rows, columns=["object_id", "property_id", "value"])

        # Pivot lentelė, kad savybės taptų stulpeliais
        df = df.pivot(index="object_id", columns="property_id", values="value").reset_index()

        # Užtikrina, kad stulpeliai yra tokie patys kaip nurodyta
        for prop in properties:
            if prop not in df.columns:
                df[prop] = None

        # Sutvarko stulpelių eiliškumą
        df = df[["object_id"] + properties]

        return df

    def close(self):
        """Uždaro ryšį su duomenų baze, jei ji buvo sukurta šioje klasėje."""
        if not self.external_connection:  # Uždaro tik vidinį ryšį
            self.conn.close()

def main():
    # Sukuria bendrą ryšio objektą
    shared_conn = sqlite3.connect(":memory:")

    # Sukuria objektus, naudodami bendrą ryšį
    book = properties_of("knyga", db_path=shared_conn)
    car = properties_of("automobilis", db_path=shared_conn)

    # Prideda duomenų
    book.add_property_type(1, "Pavadinimas")
    book.add_property("111-222-333", 1, "Lapė Snapė")

    car.add_property_type(1, "Energija")
    car.add_property("GGZ123", 1, "dyzelis")

    # Išveda duomenis
    print("Knygos savybės:", book.get_all_properties())
    print("Automobilių savybės:", car.get_all_properties())
    print()

    # Uždaro bendrą ryšį
    shared_conn.close()

    # Sukuria objektą ir pridedame duomenų
    conn = sqlite3.connect(":memory:")
    book = properties_of("knyga", db_path=conn)

    # Prideda savybių tipus
    book.add_property_type("title", "Pavadinimas")
    book.add_property_type("author", "Autorius")
    book.add_property_type("year", "Metai")

    # Prideda savybes objektams
    book.add_property("111-222-333", "title", "Lapė Snapė")
    book.add_property("111-222-333", "author", "Jojas Papievis")
    book.add_property("111-222-333", "year", "2020")

    book.add_property("222-333-444", "title", "Vilkas Pilkas")
    book.add_property("222-333-444", "author", "Antanas Antanaitis")
    book.add_property("222-333-444", "year", "1900")

    # Gauna Pandas DataFrame su nurodytomis savybėmis
    properties_to_fetch = ["title", "author", "year"]
    df = book.get_properties_as_dataframe(properties_to_fetch)
    print(df)

    # Uždaro ryšį
    conn.close()

if __name__ == "__main__":
    main()