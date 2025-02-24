
from tkinter import Tk, Label, Entry, Button, messagebox, font, Frame, Image, Canvas

from PIL import Image, ImageTk



class JuryPage:
    def __init__(self, on_submit):
        self.on_submit = on_submit

    def ouvrir_formulaire_jury(self):

        fenetre = Tk()
        fenetre.title("Page d'accueil")
        fenetre.geometry("600x400")

        image_fond = Image.open("image.jpg")
        fond_image = ImageTk.PhotoImage(image_fond)

        canvas = Canvas(fenetre, width=600, height=400)
        canvas.pack(fill="both", expand=True)

        image_on_canvas = canvas.create_image(300, 200, anchor="center", image=fond_image)


        title_font = font.Font(family="Helvetica", size=14, weight="bold")


        text_on_canvas = canvas.create_text(300, 120,
                                            text="Bienvenue sur le logiciel destiné à la gestion des données et à la délibération des candidats lors de l'examen du BFEM au Sénégal",
                                            width=500, justify="center", fill="black", font=title_font)

        def resize_elements(event):
            new_width = event.width
            new_height = event.height


            canvas.coords(image_on_canvas, new_width // 2, new_height // 2)

            resized_image = image_fond.resize((new_width, new_height), Image.Resampling.LANCZOS)
            canvas.image = ImageTk.PhotoImage(resized_image)
            canvas.itemconfig(image_on_canvas, image=canvas.image)

            canvas.coords(text_on_canvas, new_width // 2, new_height // 4)

        canvas.bind("<Configure>", resize_elements)

        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        bouton_connexion = Button(
            fenetre, text="Se connecter", command=self.ajouter_jury,
            bg="white", fg="black", font=button_font, padx=20, pady=10,
            relief="flat", bd=0, highlightbackground="#007BFF",
            highlightthickness=2, activebackground="#0056b3", activeforeground="white",
        )
        bouton_connexion.place(relx=0.5, rely=0.6, anchor="center")  # Position du bouton

        bouton_connexion.bind("<Enter>", lambda e: bouton_connexion.config(bg="blue"))
        bouton_connexion.bind("<Leave>", lambda e: bouton_connexion.config(bg="white"))

        fenetre.mainloop()

    def ajouter_jury(self):
        fenetre = Tk()
        fenetre.title("Paramétrage du Jury")
        fenetre.geometry("600x700")
        fenetre.config(bg="#f0f8ff")

        Label(fenetre, text="Paramétrage du Jury", font=("Helvetica", 16, "bold"), fg="blue", bg="#f0f8ff").pack(
            pady=20)

        cadre = Frame(fenetre, bg="#f0f8ff", padx=20, pady=20)
        cadre.pack(pady=10)

        champs = [
            "IA [Région]", "IEF [Départements]", "Localité", "Centre d’Examen",
            "Président de Jury", "Téléphone"
        ]

        entries = {}

        for i, champ in enumerate(champs):
            Label(cadre, text=champ + ":", bg="#f0f8ff", fg="blue", font=("Helvetica", 12)).grid(row=i, column=0,
                                                                                                 sticky="w", pady=10)
            entry = Entry(cadre, font=("Helvetica", 12), width=30, bd=2, relief="solid", bg="#ffffff")
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries[champ] = entry

        bouton_valider = Button(cadre, text="Valider et Accéder au Menu", command=self.valider_formulaire,
                                font=("Helvetica", 12, "bold"), fg="black", bg="white", padx=20, pady=10,
                                relief="solid", bd=3)
        bouton_valider.grid(row=len(champs), column=0, columnspan=2, pady=20)

        self.entries = entries

        fenetre.mainloop()

    def valider_formulaire(self):
        IA = self.entries["IA [Région]"].get()
        IEF = self.entries["IEF [Départements]"].get()
        localite = self.entries["Localité"].get()
        centre = self.entries["Centre d’Examen"].get()
        president = self.entries["Président de Jury"].get()
        telephone = self.entries["Téléphone"].get()

        if IA and IEF and localite and centre and president and telephone:
            parametres_jury = {
                "IA": IA,
                "IEF": IEF,
                "Localité": localite,
                "Centre d’Examen": centre,
                "Président de Jury": president,
                "Téléphone": telephone,
            }

            self.on_submit()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
