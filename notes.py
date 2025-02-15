from tkinter import *
from tkinter import Button, messagebox, Text, Scrollbar
from calculrem import Notes


class NotesManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager

    def ajouter_notes(self):


        def enregistrer():
            # pour récupérer l'anonymat principal saisi
            anonymat_principal = entry_anonymat_principal.get()

            # pour avoir le numéro de table associé à l'anonymat principal
            numero_table = self.anonymat_manager.recuperer_numero_table_par_anonymat(anonymat_principal)
            if not numero_table:
                messagebox.showerror("Erreur", "Anonymat principal non trouvé.")
                return


            notes = (
                numero_table , entry_compo_franc.get(), entry_dictee.get(), entry_etude_de_texte.get(),
                entry_instruction_civique.get(), entry_histoire_geographie.get(), entry_mathematiques.get(),
                entry_pc_lv2.get(), entry_svt.get(), entry_anglais1.get(), entry_anglais_oral.get(),
                entry_eps.get(), entry_epreuve_facultative.get()
            )
            self.db_manager.insert_notes(notes)
            messagebox.showinfo("Succès", "Notes ajoutées avec succès")
            fenetre.destroy()

        fenetre = Tk()
        fenetre.title("Ajout Notes")

        # Formulaire d'ajout des notes
        Label(fenetre, text="Anonymat Principal:").grid(row=0, column=0)
        entry_anonymat_principal = Entry(fenetre)
        entry_anonymat_principal.grid(row=0, column=1)

        Label(fenetre, text="Composition Français:").grid(row=1, column=0)
        entry_compo_franc = Entry(fenetre)
        entry_compo_franc.grid(row=1, column=1)

        Label(fenetre, text="Dictée:").grid(row=2, column=0)
        entry_dictee = Entry(fenetre)
        entry_dictee.grid(row=2, column=1)

        Label(fenetre, text="Étude de texte:").grid(row=3, column=0)
        entry_etude_de_texte = Entry(fenetre)
        entry_etude_de_texte.grid(row=3, column=1)

        Label(fenetre, text="Instruction Civique:").grid(row=4, column=0)
        entry_instruction_civique = Entry(fenetre)
        entry_instruction_civique.grid(row=4, column=1)

        Label(fenetre, text="Histoire Géographie:").grid(row=5, column=0)
        entry_histoire_geographie = Entry(fenetre)
        entry_histoire_geographie.grid(row=5, column=1)

        Label(fenetre, text="Mathématiques:").grid(row=6, column=0)
        entry_mathematiques = Entry(fenetre)
        entry_mathematiques.grid(row=6, column=1)

        Label(fenetre, text="PC/LV2:").grid(row=7, column=0)
        entry_pc_lv2 = Entry(fenetre)
        entry_pc_lv2.grid(row=7, column=1)

        Label(fenetre, text="SVT:").grid(row=8, column=0)
        entry_svt = Entry(fenetre)
        entry_svt.grid(row=8, column=1)

        Label(fenetre, text="Anglais 1:").grid(row=9, column=0)
        entry_anglais1 = Entry(fenetre)
        entry_anglais1.grid(row=9, column=1)

        Label(fenetre, text="Anglais Oral:").grid(row=10, column=0)
        entry_anglais_oral = Entry(fenetre)
        entry_anglais_oral.grid(row=10, column=1)

        Label(fenetre, text="EPS:").grid(row=11, column=0)
        entry_eps = Entry(fenetre)
        entry_eps.grid(row=11, column=1)

        Label(fenetre, text="Épreuve Facultative:").grid(row=12, column=0)
        entry_epreuve_facultative = Entry(fenetre)
        entry_epreuve_facultative.grid(row=12, column=1)

        Button(fenetre, text="Enregistrer", command=enregistrer).grid(row=13, column=0, columnspan=2)

        fenetre.mainloop()

    def gerer_deliberation(self):
        fenetre_deliberation = Tk()
        fenetre_deliberation.title("Délibération des Candidats")
        fenetre_deliberation.geometry("600x400")

        Label(fenetre_deliberation, text="Délibération des Candidats", font=("Arial", 14, "bold")).pack(pady=10)

        Button(fenetre_deliberation, text="Calculer les Résultats", command=self.afficher_resultats, bg="blue",
               fg="white").pack(pady=10)

        # Zone pour affichager les résultats
        self.resultat_text = Text(fenetre_deliberation, height=15, width=75)
        self.resultat_text.pack(pady=10)

        scrollbar = Scrollbar(fenetre_deliberation, command=self.resultat_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.resultat_text.config(yscrollcommand=scrollbar.set)

        fenetre_deliberation.mainloop()

    def afficher_resultats(self):
        """affichage resultat deliberation"""
        self.resultat_text.delete("1.0", "end")  # Efface le texte précédent

        # on récupére tous les anonymatsprincipaux
        anonymats = self.anonymat_manager.recuperer_tous_anonymats_principal()
        anonymat_dict = {str(numero_table): anonymat_principal for numero_table, anonymat_principal in anonymats}  # Dictionnaire danonymats

        candidats = self.db_manager.fetch_candidats()
        for candidat in candidats:
            # Récupérer les notes pour chaque candidat
            notes = self.db_manager.fetch_notes(candidat[0])  # Utilisez le numéro de table pour récupérer les notes
            notes_obj = Notes(candidat[0], notes)

            # Récupérer l'anonymat principal correspondant au numéro de table du candidat
            numero_table_candidat = str(candidat[0])  # Assurez-vous que le numéro de table est en chaîne
            anonymat_principal = anonymat_dict.get(numero_table_candidat, "Inconnu")

            # Calculer les résultats
            resultats = notes_obj.calculer_resultats(self.db_manager)
            resultat_str = (f"Anonymat Principal: {anonymat_principal} | Total: {resultats['total_points']} | "
                            f"Bonus EPS: {resultats['bonus_eps']} | Bonus Fac.: {resultats['bonus_facultatif']} | "
                            f"Décision: {resultats['decision']}\n")
            self.resultat_text.insert("end", resultat_str)



