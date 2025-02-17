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
            # Accéder aux entrées via le dictionnaire `entries`
            candidat = (
                entries["Numéro Table"].get(), entries["Prénom(s)"].get(), entries["Nom"].get(),
                entries["Date Naissance"].get(), entries["Lieu Naissance"].get(), entries["Sexe (M/F)"].get(),
                entries["Etablissement"].get(), entries["Type de candidat"].get(), entries["Nationalité"].get(),
                entries["Aptitude Sportive (OUI/NON)"].get(), entries["Epreuve Facultative"].get()
            )
            self.db_manager.insert_candidat(candidat)
            messagebox.showinfo("Succès", "Candidat ajouté avec succès")

        fenetre = Tk()
        fenetre.title("Ajout Candidat")
        fenetre.geometry("500x650")
        fenetre.configure(bg="white")

        Label(fenetre, text="Ajout d'un Candidat", bg="white", fg="blue", font=("Helvetica", 16, "bold")).pack(pady=10)

        cadre = Frame(fenetre, bg="white", padx=20, pady=20)
        cadre.pack(pady=10)

        champs = [
            "Numéro Table", "Prénom(s)", "Nom", "Date Naissance",
            "Lieu Naissance", "Sexe (M/F)", "Etablissement", "Type de candidat",
            "Nationalité", "Aptitude Sportive (OUI/NON)", "Epreuve Facultative"
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

    def afficher_statistiques(self):
        fenetre_statistiques = Tk()
        fenetre_statistiques.title("Statistiques")
        fenetre_statistiques.geometry("400x300")
        fenetre_statistiques.configure(bg="white")

        Label(fenetre_statistiques, text="Statistiques des Candidats", bg="white", fg="blue",
              font=("Helvetica", 16, "bold")).pack(pady=10)

        stats = self.db_manager.fetch_statistiques()
        Label(fenetre_statistiques, text=f"Nombre de candidats: {stats['nombre_candidats']}", bg="white",
              font=("Helvetica", 12)).pack(pady=5)
        Label(fenetre_statistiques, text=f"Moyenne générale: {stats['moyenne_generale']}", bg="white",
              font=("Helvetica", 12)).pack(pady=5)


        fenetre_statistiques.mainloop()