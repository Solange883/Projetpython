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


    def generer_anonymat(self, numero_table):

        numero_table = int(numero_table)
        anonymat = numero_table * 3 + 7


        anonymats_epreuves = {
            "compo_franc": str(uuid.uuid4()),
            "dictee": str(uuid.uuid4()),
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


        self.cursor.execute("SELECT `N° de table` FROM Candidats")
        candidats = self.cursor.fetchall()

        # Générer un anonymat pour chaque candidat
        for candidat in candidats:
            numero_table = candidat[0]
            self.generer_anonymat(numero_table)

        print(f"Anonymats générés pour {len(candidats)} candidats.")



    def recuperer_tous_anonymats_principal(self):

        self.cursor.execute("SELECT `N° de table`, anonymat_principal  FROM Anonymat")
        return self.cursor.fetchall()

    def recuperer_tous_anonymats(self):
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


        anonymats = self.recuperer_tous_anonymats()


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


        for anonymat in anonymats:
            numero_table, anonymat_principal, anonymats_epreuves = anonymat


            listbox.insert(END, f"Numéro Table: {numero_table} | Anonymat Principal: {anonymat_principal}")


            if anonymats_epreuves:
                listbox.insert(END, "Anonymats d'Épreuves:")
                for epreuve, anonymat_epreuve in eval(anonymats_epreuves).items():
                    listbox.insert(END, f"  - {epreuve}: {anonymat_epreuve}")
            else:
                listbox.insert(END, "Aucun anonymat d'épreuve trouvé.")


            listbox.insert(END, "-" * 100)


        bouton_pdf = Button(fenetre_affichage, text="Générer le PDF",
                            command=self.generer_pdf_anonymats,
                            font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=5)
        bouton_pdf.pack(pady=10)

        fenetre_affichage.mainloop()

    def generer_pdf_anonymats(self):

        anonymats = self.recuperer_tous_anonymats()


        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()


        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, txt="Liste des Anonymats", ln=True, align="C")
        pdf.ln(10)


        colonnes = ["N° Table", "Anonymat Principal", "Anonymats d'Épreuves"]
        largeurs_colonnes = [30, 50, 110]

        pdf.set_font("Arial", 'B', 10)
        for col, largeur in zip(colonnes, largeurs_colonnes):
            pdf.cell(largeur, 8, col, border=1, align="C")
        pdf.ln()


        for anonymat in anonymats:
            numero_table, anonymat_principal, anonymats_epreuves = anonymat

            pdf.set_font("Arial", size=9)
            pdf.cell(30, 8, str(numero_table), border=1, align="C")
            pdf.cell(50, 8, str(anonymat_principal), border=1, align="C")

            pdf.set_font("Arial", size=7)


            if anonymats_epreuves:
                anonymats_epreuves_str = "\n".join(
                    [f"{epreuve}: {anonymat}" for epreuve, anonymat in eval(anonymats_epreuves).items()]
                )
                pdf.multi_cell(110, 6, anonymats_epreuves_str, border=1, align="L")
            else:
                pdf.cell(110, 8, "Aucun anonymat d'épreuve", border=1, align="C")

            pdf.ln()


        pdf.output("Liste_Anonymats.pdf")
        messagebox.showinfo("Succès", "Le PDF des anonymats a été généré avec succès !")




    def fermer_connexion(self):
        self.conn.close()