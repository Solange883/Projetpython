from tkinter import *
from tkinter import Listbox, Scrollbar, Frame,  messagebox,ttk


class CandidatManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager

    def afficher_candidats(self):
        """Affiche tous les candidats avec tous les champs de la table."""

        candidats = self.db_manager.fetch_candidats()  # Récupération des candidats

        # Création de la fenêtre principale
        fenetre_affichage = Tk()
        fenetre_affichage.title("Liste des Candidats")
        fenetre_affichage.geometry("700x450")
        fenetre_affichage.configure(bg="white")


        # Création d'un frame pour contenir le Treeview et les scrollbars
        frame = Frame(fenetre_affichage)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Définition des colonnes
        colonnes = ("Numéro de table", "Prénom(s)", "Nom", "Date de naissance", "Lieu de naissance",
                    "Sexe", "Etablissement", "Type de candidat", "Nationalité", "Etat Sportif", "Épreuve Facultative")

        # Création du Treeview
        tree = ttk.Treeview(frame, columns=colonnes, show="headings")

        # Définition des en-têtes de colonnes
        for col in colonnes:
            tree.heading(col, text=col)  # Nom de la colonne
            tree.column(col, width=120, anchor="center")  # Largeur des colonnes ajustée

        # Ajout des données dans le tableau
        for candidat in candidats:
            tree.insert("", "end", values=candidat)

        # Scrollbars
        scrollbar_y = Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(frame, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)

        # Placement du tableau dans la fenêtre
        tree.pack(fill="both", expand=True)

        # Lancer l'interface
        fenetre_affichage.mainloop()

    def ajouter_candidat(self):

        def enregistrer():
            candidat = (
                entry_numero.get(), entry_prenom.get(), entry_nom.get(), entry_date_naissance.get(),
                entry_lieu_naissance.get(), entry_sexe.get(), entry_etablissement.get(), entry_typecandidat.get(),
                entry_nationalite.get(), entry_epr_fac.get(), entry_apt_sport.get()
            )
            self.db_manager.insert_candidat(candidat)
            messagebox.showinfo("Succès", "Candidat ajouté avec succès")
            # Générer un anonymat principal
            numero_table = candidat[0]  # on suppose que le premier élément est le numéro de table
            anonymat_principal = self.anonymat_manager.generer_anonymat(numero_table)

        fenetre = Tk()
        fenetre.title("Ajout Candidat")
        fenetre.geometry("600x700")  # Taille de la fenêtre
        fenetre.configure(bg="#f0f8ff")  # Fond de la fenêtre

        # Titre principal
        Label(fenetre, text="Ajout d'un candidat", font=("Helvetica", 16, "bold"), fg="blue", bg="#f0f8ff").pack(
            pady=20)

        # Cadre pour le formulaire
        cadre = Frame(fenetre, bg="#f0f8ff", padx=20, pady=20)
        cadre.pack(pady=10)

        # Liste des champs du formulaire
        champs = [
            "Numéro Table", "Prénom(s)", "Nom", "Date Naissance", "Lieu Naissance",
            "Sexe (M/F)", "Etablissement", "Type de candidat", "Nationalité",
            "Aptitude Sportive (OUI/NON)", "Epreuve Facultative"
        ]

        # Dictionnaire pour stocker les entrées
        entries = {}

        # Création des champs du formulaire
        for i, champ in enumerate(champs):
            Label(cadre, text=champ + ":", bg="#f0f8ff", fg="blue", font=("Helvetica", 12)).grid(row=i, column=0,
                                                                                                 sticky="w", pady=10)
            entry = Entry(cadre, font=("Helvetica", 12), width=30, bd=2, relief="solid")
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries[champ] = entry

        # Bouton Enregistrer
        bouton_enregistrer = Button(cadre, text="Enregistrer", command=enregistrer,
                                    font=("Helvetica", 12, "bold"), fg="black", bg="#007bff",
                                    padx=20, pady=10, relief="solid", bd=3)
        bouton_enregistrer.grid(row=len(champs), column=0, columnspan=2, pady=20)

        # Assigner les entrées aux variables
        entry_numero = entries["Numéro Table"]
        entry_prenom = entries["Prénom(s)"]
        entry_nom = entries["Nom"]
        entry_date_naissance = entries["Date Naissance"]
        entry_lieu_naissance = entries["Lieu Naissance"]
        entry_sexe = entries["Sexe (M/F)"]
        entry_etablissement = entries["Etablissement"]
        entry_typecandidat = entries["Type de candidat"]
        entry_nationalite = entries["Nationalité"]
        entry_apt_sport = entries["Aptitude Sportive (OUI/NON)"]
        entry_epr_fac = entries["Epreuve Facultative"]

        fenetre.mainloop()

    def afficher_statistiques(self):

        fenetre_statistiques = Tk()
        fenetre_statistiques.title("Statistiques")
        fenetre_statistiques.geometry("400x300")

        Label(fenetre_statistiques, text="Statistiques des Candidats").pack(pady=10)

        # Exemple de statistiques
        stats = self.db_manager.fetch_statistiques()
        Label(fenetre_statistiques, text=f"Nombre de candidats: {stats['nombre_candidats']}").pack()
        Label(fenetre_statistiques, text=f"Moyenne générale: {stats['moyenne_generale']}").pack()

        fenetre_statistiques.mainloop()