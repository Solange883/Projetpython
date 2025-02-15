import sqlite3
import uuid
from tkinter import *
from tkinter import Listbox, Scrollbar, Frame, END


class AnonymatManager:
    def __init__(self, db_name="BD_BFEM.sqlite"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()



    def recuperer_numero_table_par_anonymat(self, anonymat_principal):
        """ pour recuperer le numero de table associé a un anonymat principal."""
        self.cursor.execute("SELECT `N° de table` FROM Anonymat WHERE anonymat_principal = ?", (anonymat_principal,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    #generer et inserer pour ajout candidat
    def generer_anonymat(self, numero_table):
        #genere un anonymat principal et anonymat epreuve
        numero_table = int(numero_table)  # conversionde la chaîne en entier
        anonymat = numero_table * 3 + 7  # ex simple de génération

        # Générer des anonymats d'épreuves
        anonymats_epreuves = {
            "compo_franc": str(uuid.uuid4()),  # Exemple d'anonymat pour une épreuve
            "dictee": str(uuid.uuid4()),  # Exemple d'anonymat pour une autre épreuve
            # Ajoutez d'autres épreuves ici
        }

        # Vérifier si le numéro de table existe déjà
        self.cursor.execute("SELECT COUNT(*) FROM Anonymat WHERE `N° de table` = ?", (numero_table,))
        existe = self.cursor.fetchone()[0]

        if existe:
            print(f"Le numéro de table {numero_table} existe déjà. Mise à jour en cours...")
            self.cursor.execute("""
                   UPDATE Anonymat 
                   SET anonymat_principal = ?, anonymats_epreuves = ?
                   WHERE `N° de table` = ?
               """, (anonymat, str(anonymats_epreuves), numero_table))
        else:
            self.cursor.execute("""
                   INSERT INTO Anonymat (`N° de table`, anonymat_principal, anonymats_epreuves) 
                   VALUES (?, ?, ?)
               """, (numero_table, anonymat, str(anonymats_epreuves)))

        self.conn.commit()
        return anonymat

    def generer_anonymats_pour_tous(self):
        """ genere des anonymats principal pour chaque candidat en mm temps pour toutes les donnees de la base """
        # Récupérer tous les candidats de la base de données
        self.cursor.execute("SELECT `N° de table` FROM Candidats")
        candidats = self.cursor.fetchall()

        # Générer un anonymat pour chaque candidat
        for candidat in candidats:
            numero_table = candidat[0]
            self.generer_anonymat(numero_table)

        print(f"Anonymats générés pour {len(candidats)} candidats.")



    def recuperer_tous_anonymats_principal(self):
        """ on recupere seulement tous les anonymats principaux de la base de données pour deliberer """
        self.cursor.execute("SELECT `N° de table`, anonymat_principal  FROM Anonymat")
        return self.cursor.fetchall()

    def recuperer_tous_anonymats(self):
        """ onrecupere tous les anonymats de la base de données pour affichage """
        self.cursor.execute("SELECT `N° de table`, anonymat_principal,anonymats_epreuves  FROM Anonymat")
        return self.cursor.fetchall()

    def recuperer_anonymats_epreuves(self, anonymat_principal):
            """test"""
            self.cursor.execute("SELECT anonymats_epreuves FROM Anonymat WHERE anonymat_principal = ?",
                                (anonymat_principal,))
            result = self.cursor.fetchone()
            if result and result[0]:
                return eval(result[0])  # Convertit la chaîne JSON en dictionnaire
            return None

    def afficher_anonymats(self):
        """Affiche les anonymats et les anonymats d'épreuves dans une fenêtre dédiée."""
        # Récupérer les anonymats depuis la base de données
        anonymats = self.recuperer_tous_anonymats()

        # Créer une nouvelle fenêtre pour afficher les anonymats
        fenetre_affichage = Tk()
        fenetre_affichage.title("Liste des Anonymats et Anonymats d'Épreuves")
        fenetre_affichage.geometry("800x600")

        frame = Frame(fenetre_affichage)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = Listbox(frame, width=120, height=30)
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")

        listbox.config(yscrollcommand=scrollbar.set)

        # Affichage des anonymats et des anonymats d'épreuves dans la liste
        for anonymat in anonymats:
            numero_table = anonymat[0]
            anonymat_principal = anonymat[1]
            anonymats_epreuves = anonymat[2]

            # Afficher l'anonymat principal
            texte_anonymat = f"Numéro Table: {numero_table} | Anonymat Principal: {anonymat_principal}"
            listbox.insert(END, texte_anonymat)

            # Afficher les anonymats d'épreuves
            if anonymats_epreuves:
                listbox.insert(END, "Anonymats d'Épreuves:")
                for epreuve, anonymat_epreuve in eval(anonymats_epreuves).items():
                    listbox.insert(END, f"  - {epreuve}: {anonymat_epreuve}")
            else:
                listbox.insert(END, "Aucun anonymat d'épreuve trouvé.")

            # Ajouter une séparation entre les candidats
            listbox.insert(END, "-" * 100)

        fenetre_affichage.mainloop()


    def fermer_connexion(self):
        self.conn.close()