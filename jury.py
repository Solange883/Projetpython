
from tkinter import Tk, Label, Entry, Button, messagebox,font

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
        fenetre.config(bg="white")

        label_style = {"bg": "white", "fg": "blue", "font": ("Helvetica", 12)}
        entry_style = {"width": 40, "bg": "#f0f8ff", "font": ("Helvetica", 12), "bd": 1, "relief": "solid"}

        Label(fenetre, text="IA [Région] :", **label_style).pack(pady=10)
        self.entry_ia = Entry(fenetre, **entry_style)
        self.entry_ia.pack(pady=5)

        Label(fenetre, text="IEF [Départements] :", **label_style).pack(pady=10)
        self.entry_ief = Entry(fenetre, **entry_style)
        self.entry_ief.pack(pady=5)

        Label(fenetre, text="Localité :", **label_style).pack(pady=10)
        self.entry_localite = Entry(fenetre, **entry_style)
        self.entry_localite.pack(pady=5)

        Label(fenetre, text="Centre d’Examen :", **label_style).pack(pady=10)
        self.entry_centre = Entry(fenetre, **entry_style)
        self.entry_centre.pack(pady=5)

        Label(fenetre, text="Président de Jury :", **label_style).pack(pady=10)
        self.entry_president = Entry(fenetre, **entry_style)
        self.entry_president.pack(pady=5)

        Label(fenetre, text="Téléphone :", **label_style).pack(pady=10)
        self.entry_telephone = Entry(fenetre, **entry_style)
        self.entry_telephone.pack(pady=5)

        Button(fenetre, text="Valider et Accéder au Menu", command=self.valider_formulaire, bg="blue", fg="white",
               font=("Helvetica", 12), bd=0, relief="flat").pack(pady=20)

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

