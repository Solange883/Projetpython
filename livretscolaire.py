from tkinter import *
from tkinter import  Frame, messagebox


class LivretManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def ajouter_livret_scolaire(self):
        def enregistrer():
            num_table = entry_num_table.get().strip()
            nombre_de_fois = entry_nombre_de_fois.get().strip()
            moyenne_6e = entry_moyenne_6e.get().strip()
            moyenne_5e = entry_moyenne_5e.get().strip()
            moyenne_4e = entry_moyenne_4e.get().strip()
            moyenne_3e = entry_moyenne_3e.get().strip()

            # Vérifier si tous les champs sont remplis
            if not all([num_table, nombre_de_fois, moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e]):
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
                return

            # Vérifier que toutes les valeurs numériques sont bien des nombres valides
            if not (moyenne_6e.replace(".", "", 1).isdigit() and
                    moyenne_5e.replace(".", "", 1).isdigit() and
                    moyenne_4e.replace(".", "", 1).isdigit() and
                    moyenne_3e.replace(".", "", 1).isdigit()):
                messagebox.showerror("Erreur", "Les moyennes doivent être des nombres valides.")
                return

            # Convertir en float
            moyenne_6e = float(moyenne_6e)
            moyenne_5e = float(moyenne_5e)
            moyenne_4e = float(moyenne_4e)
            moyenne_3e = float(moyenne_3e)

            # Vérifier que les moyennes sont entre 0 et 20
            if not all(0 <= note <= 20 for note in [moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e]):
                messagebox.showwarning("Erreur", "Les moyennes doivent être comprises entre 0 et 20.")
                return

            moyenne_cycle = (moyenne_6e + moyenne_5e + moyenne_4e + moyenne_3e) / 4

            livret = (num_table, nombre_de_fois, moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e, moyenne_cycle)

            # Enregistrement dans la base de données
            self.db_manager.insert_livret_scolaire(livret)
            messagebox.showinfo("Succès", "Livret scolaire ajouté avec succès.")
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


