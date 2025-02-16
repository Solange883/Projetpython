
from tkinter import Tk, Label, Entry, Button, messagebox

class JuryPage:
    def __init__(self, on_submit):
        self.on_submit = on_submit  # Fonction à appeler lorsque le formulaire est soumis

    def ajouter_jury(self):
        """Crée la page du jury avec les champs de paramétrage."""
        fenetre = Tk()
        fenetre.title("Paramétrage du Jury")

        # Champ IA [Région]
        Label(fenetre, text="IA [Région] :").pack(pady=5)
        self.entry_ia = Entry(fenetre)
        self.entry_ia.pack(pady=5)

        # Champ IEF [Départements]
        Label(fenetre, text="IEF [Départements] :").pack(pady=5)
        self.entry_ief = Entry(fenetre)
        self.entry_ief.pack(pady=5)

        # Champ Localité
        Label(fenetre, text="Localité :").pack(pady=5)
        self.entry_localite = Entry(fenetre)
        self.entry_localite.pack(pady=5)

        # Champ Centre d’Examen
        Label(fenetre, text="Centre d’Examen :").pack(pady=5)
        self.entry_centre = Entry(fenetre)
        self.entry_centre.pack(pady=5)

        # Champ Président de Jury
        Label(fenetre, text="Président de Jury :").pack(pady=5)
        self.entry_president = Entry(fenetre)
        self.entry_president.pack(pady=5)

        # Champ Téléphone
        Label(fenetre, text="Téléphone :").pack(pady=5)
        self.entry_telephone = Entry(fenetre)
        self.entry_telephone.pack(pady=5)

        # Bouton pour soumettre le formulaire
        Button(fenetre, text="Valider et Accéder au Menu", command=self.valider_formulaire).pack(pady=20)

        fenetre.mainloop()

    def valider_formulaire(self):
        """Valide le formulaire et appelle la fonction on_submit."""
        # Récupérer les valeurs des champs
        ia = self.entry_ia.get()
        ief = self.entry_ief.get()
        localite = self.entry_localite.get()
        centre = self.entry_centre.get()
        president = self.entry_president.get()
        telephone = self.entry_telephone.get()


        if ia and ief and localite and centre and president and telephone:
            # Vous pouvez stocker ces valeurs dans une structure de données si nécessaire
            parametres_jury = {
                "IA": ia,
                "IEF": ief,
                "Localité": localite,
                "Centre d’Examen": centre,
                "Président de Jury": president,
                "Téléphone": telephone,
            }
            print("Paramètres du jury :", parametres_jury)  # Afficher les paramètres (à des fins de débogage)
            self.on_submit()  # Passer à la page principale
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

