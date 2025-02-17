from tkinter import *
from tkinter import  Frame, messagebox


class LivretManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def ajouter_livret_scolaire(self):
        def enregistrer():
            num_table = entry_num_table.get()
            nombre_de_fois = entry_nombre_de_fois.get()
            moyenne_6e = float(entry_moyenne_6e.get())
            moyenne_5e = float(entry_moyenne_5e.get())
            moyenne_4e = float(entry_moyenne_4e.get())
            moyenne_3e = float(entry_moyenne_3e.get())

            moyenne_cycle = (moyenne_6e + moyenne_5e + moyenne_4e + moyenne_3e) / 4

            livret = (
                num_table, nombre_de_fois, moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e, moyenne_cycle
            )
            self.db_manager.insert_livret_scolaire(livret)
            messagebox.showinfo("Succès", "Livret scolaire ajouté avec succès")
            fenetre.destroy()

        fenetre = Tk()
        fenetre.title("Ajout Livret Scolaire")



        # Changer le fond et la couleur des textes
        fenetre.config(bg="#f0f8ff")  # Bleu clair pour le fond


        # Frame avec un peu plus de marge
        frame = Frame(fenetre, bg="#f0f8ff", padx=20, pady=20)
        frame.grid(row=0, column=0)



        # Formulaire d'ajout de livret scolaire avec de l'espacement
        Label(frame, text="Numéro de Table:", bg="#f0f8ff", font=("Arial", 12)).grid(row=0, column=0, sticky=W, pady=10)
        entry_num_table = Entry(frame, font=("Arial", 12), width=25)
        entry_num_table.grid(row=0, column=1, pady=10)

        Label(frame, text="Nombre de fois:", bg="#f0f8ff", font=("Arial", 12)).grid(row=1, column=0, sticky=W, pady=10)
        entry_nombre_de_fois = Entry(frame, font=("Arial", 12), width=25)
        entry_nombre_de_fois.grid(row=1, column=1, pady=10)

        Label(frame, text="Moyenne 6e:", bg="#f0f8ff", font=("Arial", 12)).grid(row=2, column=0, sticky=W, pady=10)
        entry_moyenne_6e = Entry(frame, font=("Arial", 12), width=25)
        entry_moyenne_6e.grid(row=2, column=1, pady=10)

        Label(frame, text="Moyenne 5e:", bg="#f0f8ff", font=("Arial", 12)).grid(row=3, column=0, sticky=W, pady=10)
        entry_moyenne_5e = Entry(frame, font=("Arial", 12), width=25)
        entry_moyenne_5e.grid(row=3, column=1, pady=10)

        Label(frame, text="Moyenne 4e:", bg="#f0f8ff", font=("Arial", 12)).grid(row=4, column=0, sticky=W, pady=10)
        entry_moyenne_4e = Entry(frame, font=("Arial", 12), width=25)
        entry_moyenne_4e.grid(row=4, column=1, pady=10)

        Label(frame, text="Moyenne 3e:", bg="#f0f8ff", font=("Arial", 12)).grid(row=5, column=0, sticky=W, pady=10)
        entry_moyenne_3e = Entry(frame, font=("Arial", 12), width=25)
        entry_moyenne_3e.grid(row=5, column=1, pady=10)

        # Bouton Enregistrer stylisé
        bouton_enregistrer = Button(frame, text="Enregistrer", command=enregistrer, font=("Arial", 12, "bold"),
                                    bg="#007bff", fg="black", relief=RAISED, width=20, height=2)
        bouton_enregistrer.grid(row=6, column=0, columnspan=2, pady=20)

        fenetre.mainloop()


