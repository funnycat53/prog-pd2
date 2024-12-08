import sqlite3



conn = sqlite3.connect("dati.db", check_same_thread=False)


# izveido lietotāju tabulu ar vārda, uzvārda, lietotajvārda kolonām
def registretu_lietotaju_tabulas_izv():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE registreti_lietotaji(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL,
        lietotajvards TEXT NOT NULL UNIQUE # neļauj ievadīt lietotājvārdu, kas jau pastāv
        )
        """
    )
    conn.commit()
# pievieno jaunu lietotāju datubāzei
def pievienot_lietotaju(vards, uzvards, lietotajvards):
    cur = conn.cursor()
    # pārbauda vai šāds lietotājvārds jau pastāv
    cur.execute(
        f"""SELECT COUNT(*) FROM registreti_lietotaji WHERE lietotajvards = "{lietotajvards}" """, 
        
    )
    if cur.fetchone()[0] > 0:
        print(f"Lietotājvārds {lietotajvards} jau eksistē!")
        return False
    
    try:
        # pievieno jaunu lietotāju datubāzei
        cur.execute(
            f"""
            INSERT INTO registreti_lietotaji(vards, uzvards, lietotajvards) VALUES ("{vards}", "{uzvards}", "{lietotajvards}")
            """
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Kļūda: Lietotājvārds {lietotajvards} jau eksistē!")
        return False

def noņemt_dublētos():
    cur = conn.cursor()
    # noņem lietotājus, kuri dublējas, tos pievienojot
    cur.execute(
        """
        DELETE FROM registreti_lietotaji 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM registreti_lietotaji 
            GROUP BY vards, uzvards, lietotajvards
        )
        """
    )
    conn.commit()
    print("Dublētie ieraksti ir izdzēsti.")
    
    # iegūst visus reģistrētos lietotājus
def iegut_lietotajus():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, lietotajvards, id FROM registreti_lietotaji ORDER BY vards, uzvards"""
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

# izveido tabulu, kur tiek saglabātas lietotāju ziņas
def zinu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE zinas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zina NOT NULL,
        lietotaja_id INTEGER NOT NULL,
        izveidots DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lietotaja_id) REFERENCES registreti_lietotaji(id)
        )
        """)
    conn.commit()

# pievieno jaunu ziņu datubāzē
def pievienot_zinu(lietotaja_id, zina):
    cur = conn.cursor()
    cur.execute(
            f"""
        INSERT INTO zinas(lietotaja_id, zina) VALUES("{lietotaja_id}", "{zina}")
        """
    )
    conn.commit()

# iegūst visas ziņas no datubāzes
def iegut_zinu():
    cur = conn.cursor()
    cur.execute(
        """
        SELECT zinas.zina, registreti_lietotaji.vards, registreti_lietotaji.uzvards 
        FROM zinas 
        JOIN registreti_lietotaji ON zinas.lietotaja_id = registreti_lietotaji.id
        ORDER BY zinas.izveidots DESC 
        """
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

# iegūst statistiku par to, cik katrs lietotājs ziņas ir sūtījis
def iegut_statistiku():
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 
            registreti_lietotaji.vards, 
            registreti_lietotaji.uzvards, 
            COUNT(zinas.id) as zinojumu_skaits
        FROM 
            registreti_lietotaji
        LEFT JOIN 
            zinas ON registreti_lietotaji.id = zinas.lietotaja_id
        GROUP BY 
            registreti_lietotaji.id, 
            registreti_lietotaji.vards, 
            registreti_lietotaji.uzvards
        ORDER BY 
            zinojumu_skaits DESC 
        """
    )
    statistika = cur.fetchall()
    return statistika

