from tkinter import *
from tkinter import Button


class UI:
    def __init__(self, candidat_manager, notes_manager,anonymat_manager,livret_manager):
        self.candidat_manager = candidat_manager
        self.notes_manager = notes_manager
        self.anonymat_manager=anonymat_manager
        self.livret_manager=livret_manager

    def creer_page_principale(self):
        """La page principale elle contient tous les boutons'"""
        fenetre = Tk()
        fenetre.title("Gestion des Candidats")


        Button(fenetre, text="Ajouter", command=self.candidat_manager.ajouter_candidat).pack(pady=20)


        Button(fenetre, text="Afficher", command=self.candidat_manager.afficher_candidats).pack(pady=20)

        Button(fenetre, text="AjouterLivretScolaire", command=self.livret_manager.ajouter_livret_scolaire).pack(pady=10)


        Button(fenetre, text="Gérer les Notes", command=self.notes_manager.ajouter_notes).pack(pady=10)


        Button(fenetre, text="Délibération", command=self.notes_manager.gerer_deliberation).pack(pady=10)


        Button(fenetre, text="Statistiques", command=self.candidat_manager.afficher_statistiques).pack(pady=10)


        Button(fenetre, text="Afficher les Anonymats", command=self.anonymat_manager.afficher_anonymats).pack(pady=10)

        #Button(fenetre, text="Genererpdf", command=self.).pack(pady=10)

        fenetre.mainloop()