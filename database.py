import sqlite3
from candidat import CandidatManager
from menu import UI
from noteSecondTour import NotesSecondTourManager
from notes import NotesManager
from anonymat import AnonymatManager
from livretscolaire import LivretManager

class DatabaseManager:
    def __init__(self, db_name="BD_BFEM.sqlite"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):

        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Candidats (
            `N° de table` INTEGER PRIMARY KEY,
            `Prenom (s)` TEXT,
            `NOM` TEXT,
            `Date de nais.` TEXT,
            `Lieu de nais.` TEXT,
            `Sexe` TEXT,
            `Type de candidat` TEXT,
            `Etablissement` TEXT,
            `Nationnallité` TEXT,
            `Etat Sportif` BOOLEAN,
            `Epreuve Facultative` TEXT
        )''')


        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS LivretScolaire (
                    `N° de table` INTEGER  ,
                    `nombre_de_fois` INTEGER,
                    `moyenne_6e` REAL,
                    `moyenne_5e` REAL,
                    `moyenne_4e` REAL,
                    `moyenne_3e` REAL,
                    `moyenne_cycle` REAL,
                    FOREIGN KEY(`N° de table`) REFERENCES Candidats(`N° de table`)
                )
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notes (
                  `N° de table` INTEGER PRIMARY KEY,
                  `Note CF  ` REAL,
                  `Note Ort  ` REAL,
                  `Note TSQ  ` REAL ,
                  `Note IC` REAL ,
                  `Note HG` REAL ,
                  `Note MATH` REAL ,
                  `Note PC/LV2` REAL ,
                  `Note SVT` REAL ,
                  `Note ANG1` REAL ,
                  `Note ANG2` REAL,
                  `Note EPS` REAL ,
                  `Note Ep Fac` REAL ,
                FOREIGN KEY(`N° de table`) REFERENCES Candidats(`N° de table`)
            )
        ''')

        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Anonymat (
                    `N° de table` INTEGER  PRIMARY KEY,
                    anonymat_principal INTEGER UNIQUE NOT NULL,
                    anonymats_epreuves TEXT,
                    FOREIGN KEY(`N° de table`) REFERENCES Candidats(`N° de table`) 
                )
            ''')


        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Notes_Second_Tour  (
                          `N° de table` INTEGER PRIMARY KEY,
                          `Francais` REAL,
                          `Mathematiques` REAL,
                          `PC/LV2` REAL ,
                        FOREIGN KEY(`N° de table`) REFERENCES Candidats(`N° de table`)
                    )
                ''')



        self.conn.commit()

    def fetch_candidats(self):
        self.cursor.execute("SELECT * FROM Candidats")
        return self.cursor.fetchall()

    def insert_candidat(self, candidat):
        self.cursor.execute("INSERT INTO Candidats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", candidat)
        self.conn.commit()

    def insert_notes(self, notes):
        self.cursor.execute("INSERT INTO Notes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", notes)
        self.conn.commit()

    def fetch_notes(self, numero_table):
        self.cursor.execute("SELECT * FROM Notes WHERE  `N° de table`= ?", (numero_table,))
        return self.cursor.fetchone()
    def fetch_notes2(self):
        self.cursor.execute("SELECT * FROM Notes")
        return self.cursor.fetchall()

    def get_nombre_total_candidats(self):
        self.cursor.execute("SELECT COUNT(*) FROM Candidats")
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_taux_reussite(self):

        self.cursor.execute("""
              SELECT COUNT(*) FROM Notes
              WHERE (
                  ("Note CF" + "Note Ort" + "Note TSQ" + "Note IC" + 
                  "Note HG" + "Note MATH" + "Note PC/LV2" + "Note SVT" + 
                  "Note ANG1" + "Note ANG2" + "Note EPS" + "Note Ep Fac") / 12) >= 10
          """)
        candidats_admis = self.cursor.fetchone()
        candidats_admis = candidats_admis[0] if candidats_admis else 0

        total_candidats = self.get_nombre_total_candidats()
        return f"{round((candidats_admis / total_candidats) * 100, 2)}%" if total_candidats > 0 else "0%"

    def get_moyenne_generale(self):

        self.cursor.execute("""
              SELECT AVG(("Note CF" + "Note Ort" + "Note TSQ" + "Note IC" + 
                          "Note HG" + "Note MATH" + "Note PC/LV2" + "Note SVT" + 
                          "Note ANG1" + "Note ANG2" + "Note EPS" + "Note Ep Fac") / 12) 
              FROM Notes
          """)

        moyenne_generale = self.cursor.fetchone()

        return round(moyenne_generale[0], 2) if moyenne_generale and moyenne_generale[0] else 0

    def fetch_statistiques(self):

        return {
            "nombre_candidats": self.get_nombre_total_candidats(),
            "moyenne_generale": self.get_moyenne_generale(),
            "taux_reussite": self.get_taux_reussite()
        }


    def fetch_moyenne_cycle(self, numero_table):
        self.cursor.execute("SELECT moyenne_cycle, nombre_de_fois FROM LivretScolaire WHERE `N° de table` = ?",
                            (numero_table,))
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None, 0

    def insert_livret_scolaire(self, livret):
        self.cursor.execute('''
        INSERT INTO LivretScolaire (`N° de table`, `nombre_de_fois`, moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e, moyenne_Cycle)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', livret)
        self.conn.commit()

    def insert_notes_second_tour(self, numero_table, francais, mathematiques, pc_lv2):
        query = """
            INSERT INTO Notes_Second_Tour (`N° de table`, Francais, Mathematiques, `PC/LV2`)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (numero_table, francais, mathematiques, pc_lv2))
        self.conn.commit()

    def fetch_notes_second_tour(self, numero_table):
        self.cursor.execute("SELECT * FROM Notes_Second_Tour WHERE  `N° de table`= ?", (numero_table,))
        return self.cursor.fetchone()
    def fetch_notes_second_tour_2(self):
        self.cursor.execute("SELECT * FROM Notes_Second_Tour ")
        return self.cursor.fetchall()

    def get_candidat_by_num_table(self, num_table):
        query = "SELECT * FROM Candidats WHERE `N° de table` = ?"
        self.cursor.execute(query, (num_table,))
        return self.cursor.fetchone()
    def update_candidat(self, num_table, nouvelles_valeurs):
        query = """
        UPDATE Candidats
        SET `Prenom (s)` = ?, `NOM` = ?, `Date de nais.` = ?, `Lieu de nais.` = ?,
            `Sexe` = ?, `Type de candidat` = ?, `Etablissement` = ?, `Nationnallité` = ?,
            `Etat Sportif` = ?, `Epreuve Facultative` = ?
        WHERE `N° de table` = ?
        """
        self.cursor.execute(query, (
            nouvelles_valeurs["Prenom (s)"], nouvelles_valeurs["NOM"], nouvelles_valeurs["Date de nais."],
            nouvelles_valeurs["Lieu de nais."], nouvelles_valeurs["Sexe"],nouvelles_valeurs["Type de candidat"],
            nouvelles_valeurs["Etablissement"], nouvelles_valeurs["Nationnallité"],
            nouvelles_valeurs["Etat Sportif"], nouvelles_valeurs["Epreuve Facultative"], num_table
        ))
        self.conn.commit()

    def supprimer_candidat(self, num_table):
            try:
                self.cursor.execute("DELETE FROM Notes WHERE `N° de table` = ?", (num_table,))
                self.cursor.execute("DELETE FROM Anonymat WHERE `N° de table` = ?", (num_table,))
                self.cursor.execute("DELETE FROM Candidats WHERE `N° de table` = ?", (num_table,))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()  # Annuler en cas d'erreur
                raise e




    def close(self):
        self.conn.close()




if __name__ == "__main__":

    db_manager = DatabaseManager()
    anonymat_manager = AnonymatManager()
    candidat_manager = CandidatManager(db_manager, anonymat_manager)
    notes_manager = NotesManager(db_manager, anonymat_manager)
    livret_manager= LivretManager(db_manager)
    notes_second_tour_manager=NotesSecondTourManager(db_manager, anonymat_manager)

    #pour generer tous les anonymat de la Base
    #anonymat_manager.generer_anonymats_pour_tous()


    # Créez une instance de UI et démarrez l'application
    ui = UI(candidat_manager, notes_manager, anonymat_manager, livret_manager,notes_second_tour_manager)
    ui.demarrer_application()


    db_manager.close()




