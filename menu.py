from tkinter import *
from tkinter import Button
from jury import JuryPage

class UI:
    def __init__(self, candidat_manager, notes_manager,anonymat_manager,livret_manager,notes_second_tour_manager):
        self.candidat_manager = candidat_manager
        self.notes_manager = notes_manager
        self.anonymat_manager=anonymat_manager
        self.livret_manager=livret_manager
        self.notes_second_tour_manager=notes_second_tour_manager

    def creer_page_principale(self):
        fenetre = Tk()
        fenetre.title("Gestion des Candidats")
        fenetre.configure(bg="white")

        # Titre principal
        Label(fenetre, text="Gestion des Candidats", font=("Helvetica", 16, "bold"), fg="blue", bg="#f0f8ff").pack(
            pady=20)

        bouton_style = {
            "font": ("Helvetica", 9, "bold"),
            "fg": "black",
            "bg": "white",
            "padx": 20,
            "pady": 10,
            "relief": "solid",
            "bd": 3,
            "highlightbackground": "blue",
            "highlightthickness": 2
        }

        Button(fenetre, text="Ajouter Candidat", command=self.candidat_manager.ajouter_candidat, **bouton_style).pack(
            pady=5)
        Button(fenetre, text="Afficher Candidats", command=self.candidat_manager.afficher_candidats,
               **bouton_style).pack(pady=5)
        Button(fenetre, text="Ajouter Livret Scolaire", command=self.livret_manager.ajouter_livret_scolaire,
               **bouton_style).pack(pady=5)
        Button(fenetre, text="Ajouter Notes Premier Tour", command=self.notes_manager.ajouter_notes,
               **bouton_style).pack(pady=5)
        Button(fenetre, text="Afficher Notes Premier Tour", command=self.notes_manager.afficher_notes,
               **bouton_style).pack(pady=5)
        Button(fenetre, text="Délibération 1er Tour", command=self.notes_manager.gerer_deliberation,
               **bouton_style).pack(pady=5)
        Button(fenetre, text="Statistiques", command=self.candidat_manager.afficher_statistiques, **bouton_style).pack(
            pady=5)
        Button(fenetre, text="Afficher Anonymats", command=self.anonymat_manager.afficher_anonymats,
               **bouton_style).pack(pady=5)
        Button(fenetre, text="Ajouter Notes Second Tour",
               command=self.notes_second_tour_manager.saisir_notes_second_tour, **bouton_style).pack(pady=5)

        fenetre.mainloop()

    def demarrer_application(self):
            """Démarre l'application avec la page du jury."""
            # Crée la page du jury et passe une fonction pour naviguer vers la page principale
            jury_page = JuryPage(on_submit=self.creer_page_principale)
            jury_page.ouvrir_formulaire_jury()