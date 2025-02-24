from tkinter import *
from tkinter import  Scrollbar, Frame, messagebox, ttk
from fpdf import FPDF


class CandidatManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager

    def afficher_candidats(self):
        candidats = self.db_manager.fetch_candidats()  # Récupération des candidats


        fenetre_affichage = Tk()
        fenetre_affichage.title("Liste des Candidats")
        fenetre_affichage.geometry("700x450")
        fenetre_affichage.configure(bg="white")


        frame = Frame(fenetre_affichage)
        frame.pack(fill="both", expand=True, padx=10, pady=10)


        colonnes = ("Numéro de table", "Prénom(s)", "Nom", "Date de naissance", "Lieu de naissance",
                    "Sexe", "Type de candidat", "Etablissement", "Nationalité", "Etat Sportif", "Épreuve Facultative")


        tree = ttk.Treeview(frame, columns=colonnes, show="headings")

        for col in colonnes:
            tree.heading(col, text=col)  # Nom de la colonne
            tree.column(col, width=120, anchor="center")  # Largeur des colonnes ajustée


        for candidat in candidats:
            tree.insert("", "end", values=candidat)


        scrollbar_y = Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(frame, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)

        tree.pack(fill="both", expand=True)

        bouton_generer_pdf = Button(fenetre_affichage, text="Générer la liste des candidats en PDF", command=self.generer_pdf,
                                    font=("Helvetica", 12, "bold"), fg="black", bg="white", padx=10, pady=5)
        bouton_generer_pdf.pack(pady=10)


        fenetre_affichage.mainloop()

    def generer_pdf(self):
        candidats = self.db_manager.fetch_candidats()


        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()


        pdf.set_font("Arial", 'B', 14)
        pdf.cell(275, 10, txt="Liste des Candidats", ln=True, align="C")
        pdf.ln(8)  # Ajoute un espace

        colonnes = [
            ("Numéro", 18),
            ("Prénom(s)", 32),
            ("Nom", 30),
            ("Naissance", 28),
            ("Lieu", 28),
            ("Sexe", 12),
            ("Type de candidat", 25),
            ("Établissement", 42),
            ("Nationalité", 20),
            ("Sportif", 20),
            ("Épreuve Fac.", 30)
        ]


        pdf.set_font("Arial", size=9)


        for col_name, col_width in colonnes:
            pdf.cell(col_width, 8, col_name, border=1, align="C")
        pdf.ln()


        for candidat in candidats:
            for i, (col_name, col_width) in enumerate(colonnes):
                pdf.cell(col_width, 8, str(candidat[i]), border=1, align="C")
            pdf.ln()


        pdf.output("Liste_des_candidats.pdf")
        messagebox.showinfo("Succès", "Le PDF a été généré avec succès sous le nom Liste_des_candidats.pdf !")

    def ajouter_candidat(self):
        def enregistrer():
            for champ, entry in entries.items():
                if not entry.get().strip():
                    messagebox.showerror("Erreur", f"Le champ '{champ}' est obligatoire.")
                    return


            candidat = (
                entries["Numéro Table"].get(), entries["Prénom(s)"].get(), entries["Nom"].get(),
                entries["Date Naissance"].get(), entries["Lieu Naissance"].get(), entries["Sexe (M/F)"].get(),
                entries["Type de candidat"].get(),
                entries["Etablissement"].get(), entries["Nationnallité"].get(),
                entries["Etat Sportif"].get(), entries["Epreuve Facultative"].get()
            )
            self.db_manager.insert_candidat(candidat)
            messagebox.showinfo("Succès", "Candidat ajouté avec succès")
            anonymat = self.anonymat_manager.generer_anonymat(entries["Numéro Table"].get())


        fenetre = Tk()
        fenetre.title("Ajout Candidat")
        fenetre.geometry("500x650")
        fenetre.configure(bg="white")

        Label(fenetre, text="Ajout d'un Candidat", bg="white", fg="blue", font=("Helvetica", 16, "bold")).pack(pady=10)

        cadre = Frame(fenetre, bg="white", padx=20, pady=20)
        cadre.pack(pady=10)

        champs = [
            "Numéro Table", "Prénom(s)", "Nom", "Date Naissance",
            "Lieu Naissance", "Sexe (M/F)", "Type de candidat", "Etablissement",
            "Nationnallité", "Etat Sportif", "Epreuve Facultative"
        ]

        entries = {}

        for i, champ in enumerate(champs):
            Label(cadre, text=champ + ":", bg="white", fg="blue", font=("Helvetica", 10)).grid(row=i, column=0,
                                                                                               sticky="w", pady=5)
            entry = Entry(cadre, font=("Helvetica", 12), width=30, bd=2, relief="solid")
            entry.grid(row=i, column=1, pady=5, padx=10)
            entries[champ] = entry  # Ajouter chaque entry dans le dictionnaire `entries`

        bouton_enregistrer = Button(cadre, text="Enregistrer", command=enregistrer,
                                    font=("Helvetica", 12, "bold"), fg="black", bg="white",
                                    padx=10, pady=5, relief="solid", bd=3,
                                    highlightbackground="black", highlightthickness=2)
        bouton_enregistrer.grid(row=len(champs), column=0, columnspan=2, pady=20)

        fenetre.mainloop()


    def modifier_candidat(self):
        def charger_candidat():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Avertissement", "Veuillez sélectionner un candidat à modifier.")
                return


            num_table = tree.item(selected_item, 'values')[0]
            candidat = self.db_manager.get_candidat_by_num_table(num_table)


            champ_to_index = {
                "N° de table": 0,
                "Prenom (s)": 1,
                "NOM": 2,
                "Date de nais.": 3,
                "Lieu de nais.": 4,
                "Sexe": 5,
                "Type de candidat": 6,
                "Etablissement": 7,
                "Nationnallité": 8,
                "Etat Sportif": 9,
                "Epreuve Facultative": 10
            }


            for champ, entry in entries.items():
                entry.delete(0, END)
                entry.insert(0, candidat[champ_to_index[champ]])

        def enregistrer_modifications():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Avertissement", "Veuillez sélectionner un candidat à modifier.")
                return

            num_table = tree.item(selected_item, 'values')[0]


            nouvelles_valeurs = {
                "N° de table": num_table,
                "Prenom (s)": entries["Prenom (s)"].get(),
                "NOM": entries["NOM"].get(),
                "Date de nais.": entries["Date de nais."].get(),
                "Lieu de nais.": entries["Lieu de nais."].get(),
                "Sexe": entries["Sexe"].get(),
                "Type de candidat": entries["Type de candidat"].get(),
                "Etablissement": entries["Etablissement"].get(),
                "Nationnallité": entries["Nationnallité"].get(),
                "Etat Sportif": entries["Etat Sportif"].get().upper() in ["OUI", "TRUE", "1"],
                "Epreuve Facultative": entries["Epreuve Facultative"].get()
            }


            self.db_manager.update_candidat(num_table, nouvelles_valeurs)
            messagebox.showinfo("Succès", "Candidat modifié avec succès")


            self.recharger_candidats(tree)


        fenetre_modification = Tk()
        fenetre_modification.title("Modifier un Candidat")
        fenetre_modification.geometry("1000x700")
        fenetre_modification.configure(bg="white")


        frame_tree = Frame(fenetre_modification, bg="white")
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)


        colonnes = (
            "N° de table", "Prenom (s)", "NOM", "Date de nais.", "Lieu de nais.",
            "Sexe", "Type de candidat","Etablissement",  "Nationnallité", "Etat Sportif", "Epreuve Facultative"
        )
        tree = ttk.Treeview(frame_tree, columns=colonnes, show="headings")

        for col in colonnes:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")


        candidats = self.db_manager.fetch_candidats()
        for candidat in candidats:
            tree.insert("", "end", values=candidat)


        scrollbar_y = Scrollbar(frame_tree, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)

        tree.pack(fill="both", expand=True)


        frame_saisie = Frame(fenetre_modification, bg="white", padx=20, pady=20)
        frame_saisie.pack(fill="both", expand=True)

        champs = [
            "N° de table", "Prenom (s)", "NOM", "Date de nais.", "Lieu de nais.",
            "Sexe" , "Type de candidat", "Etablissement", "Nationnallité", "Etat Sportif", "Epreuve Facultative"
        ]

        entries = {}
        for i, champ in enumerate(champs):
            row = i // 2
            column = i % 2


            Label(frame_saisie, text=champ + ":", bg="white", fg="blue", font=("Helvetica", 10)).grid(row=row,
                                                                                                      column=column * 2,
                                                                                                      sticky="w",
                                                                                                      pady=5, padx=10)
            entry = Entry(frame_saisie, font=("Helvetica", 12), width=30, bd=2, relief="solid")
            entry.grid(row=row, column=column * 2 + 1, pady=5, padx=10)
            entries[champ] = entry


        bouton_charger = Button(frame_saisie, text="Charger Candidat", command=charger_candidat,
                                font=("Helvetica", 12, "bold"), fg="black", bg="white",
                                padx=10, pady=5, relief="solid", bd=3,
                                highlightbackground="black", highlightthickness=2)
        bouton_charger.grid(row=(len(champs) // 2) + 1, column=0, columnspan=2, pady=20)

        bouton_enregistrer = Button(frame_saisie, text="Enregistrer Modifications", command=enregistrer_modifications,
                                    font=("Helvetica", 12, "bold"), fg="black", bg="white",
                                    padx=10, pady=5, relief="solid", bd=3,
                                    highlightbackground="black", highlightthickness=2)
        bouton_enregistrer.grid(row=(len(champs) // 2) + 1, column=2, columnspan=2, pady=20)

        fenetre_modification.mainloop()

    def recharger_candidats(self, tree):
        for row in tree.get_children():
            tree.delete(row)


        candidats = self.db_manager.fetch_candidats()


        for candidat in candidats:
            tree.insert("", "end", values=candidat)



    def supprimer_candidat(self):
        def supprimer():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Avertissement", "Veuillez sélectionner un candidat à supprimer.")
                return

            num_table = tree.item(selected_item, 'values')[0]  # "N° de table" est la clé primaire


            confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce candidat ?")
            if confirmation:
                self.db_manager.supprimer_candidat(num_table)

                self.recharger_candidats(tree)

                messagebox.showinfo("Succès", "Candidat supprimé avec succès")


        fenetre_suppression = Tk()
        fenetre_suppression.title("Supprimer un Candidat")
        fenetre_suppression.geometry("800x600")
        fenetre_suppression.configure(bg="white")


        frame_tree = Frame(fenetre_suppression, bg="white")
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)


        colonnes = (
            "N° de table", "Prenom (s)", "NOM", "Date de nais.", "Lieu de nais.",
            "Sexe", "Type de candidat", "Etablissement",  "Nationnallité", "Etat Sportif", "Epreuve Facultative"
        )
        tree = ttk.Treeview(frame_tree, columns=colonnes, show="headings")

        for col in colonnes:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")


        candidats = self.db_manager.fetch_candidats()
        for candidat in candidats:
            tree.insert("", "end", values=candidat)


        scrollbar_y = Scrollbar(frame_tree, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)

        tree.pack(fill="both", expand=True)


        bouton_supprimer = Button(fenetre_suppression, text="Supprimer", command=supprimer,
                                  font=("Helvetica", 12, "bold"), fg="black", bg="white",
                                  padx=10, pady=5, relief="solid", bd=3,
                                  highlightbackground="black", highlightthickness=2)
        bouton_supprimer.pack(pady=20)

        fenetre_suppression.mainloop()

    def recharger_candidats(self, tree):
        for row in tree.get_children():
            tree.delete(row)

        candidats = self.db_manager.fetch_candidats()

        for candidat in candidats:
            tree.insert("", "end", values=candidat)


    def afficher_statistiques(self):
        stats = self.db_manager.fetch_statistiques()

        fenetre_statistiques = Tk()
        fenetre_statistiques.title("Statistiques")
        fenetre_statistiques.geometry("400x300")
        fenetre_statistiques.configure(bg="white")

        Label(fenetre_statistiques, text="Statistiques des Candidats", bg="white", fg="blue",
              font=("Helvetica", 16, "bold")).pack(pady=10)

        Label(fenetre_statistiques, text=f"Nombre de candidats: {stats['nombre_candidats']}", bg="white",
              font=("Helvetica", 12)).pack(pady=5)

        Label(fenetre_statistiques, text=f"Taux de réussite: {stats['taux_reussite']}", bg="white",
              font=("Helvetica", 12)).pack(pady=5)

        Label(fenetre_statistiques, text=f"Moyenne générale des notes : {stats['moyenne_generale']} / 20", bg="white",
              font=("Helvetica", 12)).pack(pady=5)


        fenetre_statistiques.mainloop()