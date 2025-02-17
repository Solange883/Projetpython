from tkinter import *
from tkinter import Button, messagebox, Text, Scrollbar
from notes import Notes  # Importer la classe Notes depuis notes.py
from calculrem import Notes


class NotesSecondTourManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager
        self.anonymats_second_tour = self.recuperer_anonymats_second_tour()

    def recuperer_anonymats_second_tour(self):
        """Récupère la liste des anonymats des candidats admissibles au second tour."""
        anonymats_admissibles = set()

        # Récupérer les anonymats principaux
        anonymats = self.anonymat_manager.recuperer_tous_anonymats_principal()
        anonymat_dict = {str(numero_table): str(anonymat_principal).strip() for numero_table, anonymat_principal in anonymats}

        # Récupérer les candidats et leurs notes
        candidats = self.db_manager.fetch_candidats()
        for candidat in candidats:
            notes = self.db_manager.fetch_notes(candidat[0])
            notes_obj = Notes(candidat[0], notes)
            resultats = notes_obj.calculer_resultats(self.db_manager)

            # Vérifier si le candidat est admissible au second tour
            if resultats['decision'] in ["Passage au second tour", "Repêchable au second tour",
                                         "Repêchable pour le second tour"]:
                numero_table_candidat = str(candidat[0])
                anonymat_admissible = anonymat_dict.get(numero_table_candidat, None)
                if anonymat_admissible:
                    anonymats_admissibles.add(anonymat_admissible)


        return anonymats_admissibles

    def saisir_notes_second_tour(self):


        def enregistrer():

            anonymat_principal = entry_anonymat_principal.get().strip()


            # Vérifier si l'anonymat appartient bien aux candidats admissibles
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

            # Validation des notes (doivent être entre 0 et 20)
            if not (0 <= francais <= 20) or not (0 <= mathematiques <= 20) or not (0 <= pc_lv2 <= 20):
                messagebox.showwarning("Erreur", "Les notes doivent être comprises entre 0 et 20.")
                return

            self.db_manager.insert_notes_second_tour(numero_table, francais, mathematiques, pc_lv2)
            messagebox.showinfo("Succès", "Les notes du second tour ont été enregistrées avec succès.")
            fenetre.destroy()

        fenetre = Tk()
        fenetre.title("Saisie des Notes du Second Tour")

        # Formulaire de saisie des notes du second tour
        Label(fenetre, text="Anonymat Principal:").grid(row=0, column=0)
        entry_anonymat_principal = Entry(fenetre)
        entry_anonymat_principal.grid(row=0, column=1)

        Label(fenetre, text="Français :").grid(row=1, column=0)
        entry_francais = Entry(fenetre)
        entry_francais.grid(row=1, column=1)

        Label(fenetre, text="Mathématiques :").grid(row=2, column=0)
        entry_mathematiques = Entry(fenetre)
        entry_mathematiques.grid(row=2, column=1)

        Label(fenetre, text="PC/LV2 :").grid(row=3, column=0)
        entry_pc_lv2 = Entry(fenetre)
        entry_pc_lv2.grid(row=3, column=1)

        Button(fenetre, text="Enregistrer", command=enregistrer).grid(row=4, column=0, columnspan=2)

        fenetre.mainloop()


        """fonction Affiche les résultats du second tour."""
