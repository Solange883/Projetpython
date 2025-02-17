
from tkinter import messagebox
import tkinter as tk

from calculrem import Notes


class NotesSecondTourManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager
        self.anonymats_second_tour = self.recuperer_anonymats_second_tour()

    def recuperer_anonymats_second_tour(self):
        """Récupère la liste des anonymats des candidats admissible au second tour."""
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




    """fonction Affiche les résultats du second tour?"""
