from tkinter import *
from tkinter import Listbox, Scrollbar, Frame, END, messagebox


class CandidatManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager

    def afficher_candidats(self):

        candidats = self.db_manager.fetch_candidats()

        fenetre_affichage = Tk()
        fenetre_affichage.title("Liste des Candidats")
        fenetre_affichage.geometry("600x400")

        frame = Frame(fenetre_affichage)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = Listbox(frame, width=100, height=20)
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")

        listbox.config(yscrollcommand=scrollbar.set)

        # Affichage des candidats dans une liste
        for candidat in candidats:
            texte_candidat = f"Num: {candidat[0]} | Nom: {candidat[2]} {candidat[1]} | Naissance: {candidat[3]} | Sexe: {candidat[5]}"
            listbox.insert(END, texte_candidat)

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

        # Formulaire d'ajout de candidat
        Label(fenetre, text="Numéro Table:").grid(row=0, column=0)
        entry_numero = Entry(fenetre)
        entry_numero.grid(row=0, column=1)

        Label(fenetre, text="Prénom(s):").grid(row=1, column=0)
        entry_prenom = Entry(fenetre)
        entry_prenom.grid(row=1, column=1)

        Label(fenetre, text="Nom:").grid(row=2, column=0)
        entry_nom = Entry(fenetre)
        entry_nom.grid(row=2, column=1)

        Label(fenetre, text="Date Naissance:").grid(row=3, column=0)
        entry_date_naissance = Entry(fenetre)
        entry_date_naissance.grid(row=3, column=1)

        Label(fenetre, text="Lieu Naissance:").grid(row=4, column=0)
        entry_lieu_naissance = Entry(fenetre)
        entry_lieu_naissance.grid(row=4, column=1)

        Label(fenetre, text="Sexe (M/F):").grid(row=5, column=0)
        entry_sexe = Entry(fenetre)
        entry_sexe.grid(row=5, column=1)

        Label(fenetre, text="Etablissement:").grid(row=6, column=0)
        entry_etablissement = Entry(fenetre)
        entry_etablissement.grid(row=6, column=1)

        Label(fenetre, text="Type de candidat:").grid(row=7, column=0)
        entry_typecandidat = Entry(fenetre)
        entry_typecandidat.grid(row=7, column=1)

        Label(fenetre, text="Nationalité:").grid(row=8, column=0)
        entry_nationalite = Entry(fenetre)
        entry_nationalite.grid(row=8, column=1)

        Label(fenetre, text="Aptitude Sportive (OUI/NON):").grid(row=9, column=0)
        entry_apt_sport = Entry(fenetre)
        entry_apt_sport.grid(row=9, column=1)

        Label(fenetre, text="Epreuve Facultative:").grid(row=10, column=0)
        entry_epr_fac = Entry(fenetre)
        entry_epr_fac.grid(row=10, column=1)

        Button(fenetre, text="Enregistrer", command=enregistrer).grid(row=11, column=0, columnspan=2)

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