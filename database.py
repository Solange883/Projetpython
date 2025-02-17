#ce qui reste
#RM sur second tour(le probleme lajout des notesdusecondtour)?

#Bouton et fonction modifier candidat

#bouton et fonction afficher listes notes

#table jury(je sais pas si on doit le faire)

#statistiques(le taux de réussite, la moyenne des notes)


#FICHIER GENEREPDF


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
            `Etablissement` TEXT,
            `Type de candidat` TEXT,
            `Nationnallite` TEXT,
            `Etat Sportif` BOOLEAN,
            `Epreuve_Facultative` TEXT
        )''')

        # Table du livret scolaire
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

        # Table des notes
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

        # Table des anonymats
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Anonymat (
                    `N° de table` INTEGER  PRIMARY KEY,
                    anonymat_principal INTEGER UNIQUE NOT NULL,
                    anonymats_epreuves TEXT,
                    FOREIGN KEY(`N° de table`) REFERENCES Candidats(`N° de table`) 
                )
            ''')

        # Table des notes Second Tour
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

    def fetch_statistiques(self):
        # Exemplede statistique cest a refaire
        self.cursor.execute("SELECT * FROM Candidats")
        return {"nombre_candidats": 2, "moyenne_generale": 14.5}

    def fetch_moyenne_cycle(self, numero_table):
        """Récupère la moy du cycle et le nbre de fois pour un candidat donné."""
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
        """Enregistre les notes du second tour dans la base de données."""
        query = """
            INSERT INTO Notes_Second_Tour (`N° de table`, Francais, Mathematiques, `PC/LV2`)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (numero_table, francais, mathematiques, pc_lv2))
        self.conn.commit()



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




