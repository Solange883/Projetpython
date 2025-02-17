from tkinter import *
from tkinter import Button,Tk, Label
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
        Label(fenetre, text="Gestion des Candidats", font=("Helvetica", 16, "bold"), fg="blue", bg="#f0f8ff").grid(
            row=0, column=0, columnspan=2, pady=20
        )

        bouton_style = {
            "font": ("Helvetica", 9, "bold"),
            "fg": "black",
            "bg": "white",
            "padx": 20,
            "pady": 10,
            "relief": "solid",
            "bd": 3,
            "highlightbackground": "blue",
            "highlightthickness": 2,
            "width": 20  # Largeur fixe pour tous les boutons
        }

        # Liste des boutons avec leurs commandes
        boutons = [
            ("Ajouter Candidat", self.candidat_manager.ajouter_candidat),
            ("Afficher Candidats", self.candidat_manager.afficher_candidats),
            ("Ajouter Livret Scolaire", self.livret_manager.ajouter_livret_scolaire),
            ("Ajouter Notes Premier Tour", self.notes_manager.ajouter_notes),
            ("Afficher Notes Premier Tour", self.notes_manager.afficher_notes),
            ("Délibération 1er Tour", self.notes_manager.gerer_deliberation),
            ("Statistiques", self.candidat_manager.afficher_statistiques),
            ("Afficher Anonymats", self.anonymat_manager.afficher_anonymats),
            ("Ajouter Notes Second Tour", self.notes_second_tour_manager.saisir_notes_second_tour),
            ("Afficher Notes Second Tour", self.notes_second_tour_manager.afficher_notes_second_tour),
            ("Délibération 2eme Tour", self.notes_second_tour_manager.gerer_deliberation)
        ]

        # Placement des boutons en 2 colonnes
        for i, (texte, commande) in enumerate(boutons):
            row = (i // 2) + 1  # Ligne calculée en fonction de l'index
            column = i % 2  # Colonne alternée (0 ou 1)
            Button(fenetre, text=texte, command=commande, **bouton_style).grid(
                row=row, column=column, padx=10, pady=5
            )

        fenetre.mainloop()

    def demarrer_application(self):
            """Démarre l'application avec la page du jury."""
            # Crée la page du jury et passe une fonction pour naviguer vers la page principale
            jury_page = JuryPage(on_submit=self.creer_page_principale)
            jury_page.ouvrir_formulaire_jury()