import sqlite3
import uuid
from tkinter import *
from tkinter import Listbox, Scrollbar, Frame, END, messagebox
from fpdf import FPDF


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
            "dictee": str(uuid.uuid4()), # Exemple d'anonymat pour une autre épreuve
            "etude_de_texte": str(uuid.uuid4()),
            "instruction_civique":str(uuid.uuid4()),
            "histoire_geographie":str(uuid.uuid4()),
            "mathematiques": str(uuid.uuid4()),
            "pc_lv2": str(uuid.uuid4()),
            "svt": str(uuid.uuid4()),
            "anglais1": str(uuid.uuid4()),
            "anglais_oral": str(uuid.uuid4()),
            "eps": str(uuid.uuid4()),
            "epreuve_fac": str(uuid.uuid4()),

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
        """Affiche les anonymats dans une interface et ajoute un bouton pour générer un PDF."""

        # Récupérer les anonymats
        anonymats = self.recuperer_tous_anonymats()

        # Création de la fenêtre principale
        fenetre_affichage = Tk()
        fenetre_affichage.title("Liste des Anonymats")
        fenetre_affichage.geometry("800x600")

        frame = Frame(fenetre_affichage)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = Listbox(frame, width=120, height=30)
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        # Affichage des anonymats et anonymats d'épreuves
        for anonymat in anonymats:
            numero_table, anonymat_principal, anonymats_epreuves = anonymat

            # Afficher l'anonymat principal
            listbox.insert(END, f"Numéro Table: {numero_table} | Anonymat Principal: {anonymat_principal}")

            # Afficher les anonymats d'épreuves
            if anonymats_epreuves:
                listbox.insert(END, "Anonymats d'Épreuves:")
                for epreuve, anonymat_epreuve in eval(anonymats_epreuves).items():
                    listbox.insert(END, f"  - {epreuve}: {anonymat_epreuve}")
            else:
                listbox.insert(END, "Aucun anonymat d'épreuve trouvé.")

            # Ajouter une séparation
            listbox.insert(END, "-" * 100)

        # Bouton pour générer le PDF
        bouton_pdf = Button(fenetre_affichage, text="Générer le PDF",
                            command=self.generer_pdf_anonymats,
                            font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=5)
        bouton_pdf.pack(pady=10)

        fenetre_affichage.mainloop()

    def generer_pdf_anonymats(self):
        """Génère un PDF contenant les anonymats et anonymats d'épreuves bien organisés."""

        anonymats = self.recuperer_tous_anonymats()

        # Création du fichier PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Titre du document
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, txt="Liste des Anonymats", ln=True, align="C")
        pdf.ln(10)

        # Définition des colonnes
        colonnes = ["N° Table", "Anonymat Principal", "Anonymats d'Épreuves"]
        largeurs_colonnes = [30, 50, 110]

        # En-tête du tableau
        pdf.set_font("Arial", 'B', 10)
        for col, largeur in zip(colonnes, largeurs_colonnes):
            pdf.cell(largeur, 8, col, border=1, align="C")
        pdf.ln()

        # Remplissage des données
        for anonymat in anonymats:
            numero_table, anonymat_principal, anonymats_epreuves = anonymat

            pdf.set_font("Arial", size=9)
            pdf.cell(30, 8, str(numero_table), border=1, align="C")
            pdf.cell(50, 8, str(anonymat_principal), border=1, align="C")

            # Formatage de la colonne des anonymats d'épreuves avec une police plus petite
            pdf.set_font("Arial", size=7)

            # Gestion du retour à la ligne pour éviter le débordement
            if anonymats_epreuves:
                anonymats_epreuves_str = "\n".join(
                    [f"{epreuve}: {anonymat}" for epreuve, anonymat in eval(anonymats_epreuves).items()]
                )
                pdf.multi_cell(110, 6, anonymats_epreuves_str, border=1, align="L")
            else:
                pdf.cell(110, 8, "Aucun anonymat d'épreuve", border=1, align="C")

            pdf.ln()

        # Sauvegarde du fichier PDF
        pdf.output("Liste_Anonymats.pdf")
        messagebox.showinfo("Succès", "Le PDF des anonymats a été généré avec succès !")




    def fermer_connexion(self):
        self.conn.close()