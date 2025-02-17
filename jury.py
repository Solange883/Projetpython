
from tkinter import Tk, Label, Entry, Button, messagebox, font, Frame


class JuryPage:
    def __init__(self, on_submit):
        self.on_submit = on_submit  # Fonction à appeler lorsque le formulaire est soumis

    def ouvrir_formulaire_jury(self):
        """Ouvre une fenêtre avec un message d'accueil et un bouton de connexion stylisé"""
        fenetre = Tk()
        fenetre.title("Page d'accueil")
        fenetre.geometry("600x400")  # Taille de la fenêtre
        fenetre.configure(bg="#f0f0f0")  # Couleur de fond de la fenêtre

        # Style de police pour le texte et les boutons
        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        button_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Message d'accueil stylisé
        Label(
            fenetre,
            text="Logiciel destiné à la gestion des données et à la délibération des candidats lors de l'examen du BFEM au Sénégal",
            wraplength=500,  # Largeur maximale du texte avant retour à la ligne
            justify="center",  # Centrer le texte
            bg="#f0f0f0",  # Couleur de fond du label
            fg="#333333",  # Couleur du texte
            font=title_font  # Police personnalisée
        ).pack(pady=50)

        # Bouton "Se connecter" stylisé
        Button(
            fenetre,
            text="Se connecter",
            command=self.ajouter_jury,
            bg="blue",  # Couleur de fond du bouton
            fg="white",  # Couleur du texte
            font=button_font,  # Police personnalisée
            padx=20,  # Espacement horizontal
            pady=10,  # Espacement vertical
            relief="flat",  # Style de bordure (flat pour un look moderne)
            bd=0,  # Pas de bordure supplémentaire
            highlightbackground="#4CAF50",  # Couleur de la bordure
            highlightthickness=2,  # Épaisseur de la bordure
            activebackground="#45a049",  # Couleur de fond au clic
            activeforeground="white"  # Couleur du texte au clic
        ).pack(pady=20)

        fenetre.mainloop()

    def ajouter_jury(self):


        fenetre = Tk()
        fenetre.title("Paramétrage du Jury")
        fenetre.geometry("600x700")
        fenetre.config(bg="#f0f8ff")

        # Titre principal
        Label(fenetre, text="Paramétrage du Jury", font=("Helvetica", 16, "bold"), fg="blue", bg="#f0f8ff").pack(
            pady=20)

        # Cadre pour le formulaire
        cadre = Frame(fenetre, bg="#f0f8ff", padx=20, pady=20)
        cadre.pack(pady=10)

        # Liste des champs du formulaire
        champs = [
            "IA [Région]", "IEF [Départements]", "Localité", "Centre d’Examen",
            "Président de Jury", "Téléphone"
        ]

        # Dictionnaire pour stocker les entrées
        entries = {}

        # Création des champs du formulaire
        for i, champ in enumerate(champs):
            Label(cadre, text=champ + ":", bg="#f0f8ff", fg="blue", font=("Helvetica", 12)).grid(row=i, column=0,
                                                                                                 sticky="w", pady=10)
            entry = Entry(cadre, font=("Helvetica", 12), width=30, bd=2, relief="solid", bg="#ffffff")
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries[champ] = entry

        # Bouton Valider
        bouton_valider = Button(cadre, text="Valider et Accéder au Menu", command=self.valider_formulaire,
                                font=("Helvetica", 12, "bold"), fg="black", bg="#007bff",
                                padx=20, pady=10, relief="solid", bd=3)
        bouton_valider.grid(row=len(champs), column=0, columnspan=2, pady=20)

        # Assigner les entrées aux variables
        entry_ia = entries["IA [Région]"]
        entry_ief = entries["IEF [Départements]"]
        entry_localite = entries["Localité"]
        entry_centre = entries["Centre d’Examen"]
        entry_president = entries["Président de Jury"]
        entry_telephone = entries["Téléphone"]

        fenetre.mainloop()
    def valider_formulaire(self):
        #valier et appelons onsubmit
        # Récupérer les valeurs des champs
        ia = self.entry_ia.get()
        ief = self.entry_ief.get()
        localite = self.entry_localite.get()
        centre = self.entry_centre.get()
        president = self.entry_president.get()
        telephone = self.entry_telephone.get()


        if ia and ief and localite and centre and president and telephone:
            # on stocke les val dans parametres_jury
            parametres_jury = {
                "IA": ia,
                "IEF": ief,
                "Localité": localite,
                "Centre d’Examen": centre,
                "Président de Jury": president,
                "Téléphone": telephone,
            }

            self.on_submit()  # on passe à la page principale
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

