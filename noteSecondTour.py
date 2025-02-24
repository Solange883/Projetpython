
from tkinter import Tk,ttk,  Label,  Button, Text, Scrollbar, messagebox,Frame
import tkinter as tk

from fpdf import FPDF

from calculrem import Notes
from calculrem2 import Notes2


class NotesSecondTourManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager
        self.anonymats_second_tour = self.recuperer_anonymats_second_tour()

    def recuperer_anonymats_second_tour(self):
        anonymats_admissibles = set()


        anonymats = self.anonymat_manager.recuperer_tous_anonymats_principal()
        anonymat_dict = {str(numero_table): str(anonymat_principal).strip() for numero_table, anonymat_principal in anonymats}



        candidats = self.db_manager.fetch_candidats()
        for candidat in candidats:
            notes = self.db_manager.fetch_notes(candidat[0])
            notes_obj = Notes(candidat[0], notes)
            resultats = notes_obj.calculer_resultats(self.db_manager)

            if resultats['decision'] in ["Repêchable d'office","Passage au second tour","Repêchable au second tour"]:
                numero_table_candidat = str(candidat[0])
                anonymat_admissible = anonymat_dict.get(numero_table_candidat, None)
                if anonymat_admissible:
                    anonymats_admissibles.add(anonymat_admissible)

        return anonymats_admissibles


    def saisir_notes_second_tour(self):
        def enregistrer():
            anonymat_principal = entry_anonymat_principal.get().strip()

            anonymat_principal = str(anonymat_principal)


            if anonymat_principal not in self.anonymats_second_tour:
                messagebox.showerror("Erreur", "Ce candidat n'est pas admissible au second tour.")
                return


            numero_table = self.anonymat_manager.recuperer_numero_table_par_anonymat(anonymat_principal)
            if not numero_table:
                messagebox.showerror("Erreur", "Anonymat principal non trouvé.")
                return

            francais = float(entry_francais.get())
            mathematiques = float(entry_mathematiques.get())
            pc_lv2 = float(entry_pc_lv2.get())

            if not all(0 <= note <= 20 for note in [francais, mathematiques, pc_lv2]):
                messagebox.showwarning("Erreur", "Les notes doivent être comprises entre 0 et 20.")
                return


            if not all([anonymat_principal, francais, mathematiques, pc_lv2]):
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
                return


            self.db_manager.insert_notes_second_tour(numero_table, francais, mathematiques, pc_lv2)
            messagebox.showinfo("Succès", "Les notes du second tour ont été enregistrées avec succès.")
            fenetre.destroy()

        fenetre = tk.Tk()
        fenetre.title("Saisie des Notes du Second Tour")
        fenetre.geometry("400x300")
        fenetre.configure(bg="white")

        tk.Label(fenetre, text="Saisie des Notes du Second Tour", bg="white", fg="blue",
                 font=("Helvetica", 16, "bold")).pack(pady=10)

        cadre = tk.Frame(fenetre, bg="white", padx=20, pady=20)
        cadre.pack(pady=10)

        champs = ["Anonymat Principal", "Français", "Mathématiques", "PC/LV2"]
        entries = {}

        for i, champ in enumerate(champs):
            tk.Label(cadre, text=champ + ":", bg="white", fg="blue", font=("Helvetica", 12)).grid(row=i, column=0,
                                                                                                  sticky="w", pady=5)
            entry = tk.Entry(cadre, font=("Helvetica", 12), width=25, bd=2, relief="solid")
            entry.grid(row=i, column=1, pady=5, padx=10)
            entries[champ] = entry

        bouton_enregistrer = tk.Button(cadre, text="Enregistrer", command=enregistrer,
                                       font=("Helvetica", 12, "bold"), fg="black", bg="white",
                                       padx=10, pady=5, relief="solid", bd=3,
                                       highlightbackground="black", highlightthickness=2)
        bouton_enregistrer.grid(row=len(champs), column=0, columnspan=2, pady=20)

        entry_anonymat_principal = entries["Anonymat Principal"]
        entry_francais = entries["Français"]
        entry_mathematiques = entries["Mathématiques"]
        entry_pc_lv2 = entries["PC/LV2"]

        fenetre.mainloop()



    def afficher_notes_second_tour(self):
        notes = self.db_manager.fetch_notes_second_tour_2()


        fenetre_affichage = Tk()
        fenetre_affichage.title("Liste des notes du 2nd tour")
        fenetre_affichage.geometry("700x450")
        fenetre_affichage.configure(bg="white")

        frame = Frame(fenetre_affichage)
        frame.pack(fill="both", expand=True, padx=10, pady=10)


        colonnes = ("N° de table", "Note CF", "Note MATH", "Note PC/LV2")

        self.tree = ttk.Treeview(frame, columns=colonnes, show="headings")


        for col in colonnes:
            self.tree.heading(col, text=col)  # Nom de la colonne
            self.tree.column(col, width=120, anchor="center")  # Largeur des colonnes ajustée


        for note in notes:
            self.tree.insert("", "end", values=note)

        scrollbar_y = Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scrollbar_x.set)


        self.tree.pack(fill="both", expand=True)


        bouton_pdf = Button(fenetre_affichage, text="Générer les notes du 2nd tour en PDF", command=self.generer_pdf_notes_second_tour,
                            bg="green", fg="white", font=("Helvetica", 12, "bold"), padx=10)
        bouton_pdf.pack(pady=10)

        # Lancer l'interface
        fenetre_affichage.mainloop()



    def gerer_deliberation(self):
        fenetre_deliberation = Tk()
        fenetre_deliberation.title("Délibération des Candidats")
        fenetre_deliberation.geometry("600x400")

        Label(fenetre_deliberation, text="Délibération des Candidats du Second Tour", font=("Arial", 14, "bold")).pack(
            pady=10)

        Button(fenetre_deliberation, text="Calculer les Résultats", command=self.afficher_resultats_second_tour,
               bg="blue", fg="white").pack(pady=10)


        self.resultat_text = Text(fenetre_deliberation, height=15, width=75)
        self.resultat_text.pack(pady=10)

        scrollbar = Scrollbar(fenetre_deliberation, command=self.resultat_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.resultat_text.config(yscrollcommand=scrollbar.set)


        Button(fenetre_deliberation, text="Générer PDF", command=self.generer_pdf_resultats_second_tour,
               bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        fenetre_deliberation.mainloop()

    def afficher_resultats_second_tour(self):
        self.resultat_text.delete("1.0", "end")  # Efface les résultats précédents


        anonymats_admissibles = self.recuperer_anonymats_second_tour()
        anonymats_admissibles = {anonymat.strip() for anonymat in anonymats_admissibles}


        anonymats = self.anonymat_manager.recuperer_tous_anonymats_principal()
        anonymat_dict = {str(numero_table): str(anonymat_principal).strip() for numero_table, anonymat_principal in
                         anonymats}


        self.resultats_list = []
        candidats = self.db_manager.fetch_candidats()

        for candidat in candidats:
            numero_table_candidat = str(candidat[0])
            anonymat_principal = anonymat_dict.get(numero_table_candidat, "Inconnu").strip()

            if anonymat_principal in anonymats_admissibles:
                notes = self.db_manager.fetch_notes_second_tour(candidat[0])

                # Vérifier si `notes` est `None` ou si toutes les notes sont vides
                if not notes or not any(note is not None for note in notes):
                    continue  # Ignorer ce candidat

                notes_obj = Notes2(candidat[0], notes)
                resultats = notes_obj.calculer_resultats(self.db_manager)

                resultat_str = (f"Anonymat Principal: {anonymat_principal} | Total: {resultats['total_points']} | "
                                f"Décision: {resultats['decision']}\n")
                self.resultat_text.insert("end", resultat_str)
                self.resultats_list.append((anonymat_principal, resultats['total_points'], resultats['decision']))


        if not self.resultat_text.get("1.0", "end-1c").strip():
            self.resultat_text.insert("end", "Aucun candidat admissible au second tour.\n")


    def generer_pdf_resultats_second_tour(self):
        if not self.resultats_list:
            messagebox.showerror("Erreur", "Aucun résultat à exporter en PDF.")
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Résultats du Second Tour", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 10)
        colonnes = ["Anonymat", "Total Points", "Décision"]
        largeurs_colonnes = [50, 40, 60]

        for col, largeur in zip(colonnes, largeurs_colonnes):
            pdf.cell(largeur, 8, col, border=1, align="C")
        pdf.ln()


        pdf.set_font("Arial", size=10)
        for anonymat, total, decision in self.resultats_list:
            pdf.cell(50, 8, str(anonymat), border=1, align="C")
            pdf.cell(40, 8, str(total), border=1, align="C")
            pdf.cell(60, 8, decision, border=1, align="C")
            pdf.ln()


        pdf_filename = "resultats_second_tour.pdf"
        pdf.output(pdf_filename)
        messagebox.showinfo("Succès", f"Le PDF {pdf_filename} a été généré avec succès sur le dossier du projet !")

