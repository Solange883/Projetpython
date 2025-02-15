from tkinter import *
from tkinter import Listbox, Scrollbar, Frame, END, messagebox


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

        # Formulaire d'ajout de livret scolaire
        Label(fenetre, text="Numéro de Table:").grid(row=0, column=0)
        entry_num_table = Entry(fenetre)
        entry_num_table.grid(row=0, column=1)

        Label(fenetre, text="Nombre de fois:").grid(row=1, column=0)
        entry_nombre_de_fois = Entry(fenetre)
        entry_nombre_de_fois.grid(row=1, column=1)

        Label(fenetre, text="Moyenne 6e:").grid(row=2, column=0)
        entry_moyenne_6e = Entry(fenetre)
        entry_moyenne_6e.grid(row=2, column=1)

        Label(fenetre, text="Moyenne 5e:").grid(row=3, column=0)
        entry_moyenne_5e = Entry(fenetre)
        entry_moyenne_5e.grid(row=3, column=1)

        Label(fenetre, text="Moyenne 4e:").grid(row=4, column=0)
        entry_moyenne_4e = Entry(fenetre)
        entry_moyenne_4e.grid(row=4, column=1)

        Label(fenetre, text="Moyenne 3e:").grid(row=5, column=0)
        entry_moyenne_3e = Entry(fenetre)
        entry_moyenne_3e.grid(row=5, column=1)

        Button(fenetre, text="Enregistrer", command=enregistrer).grid(row=6, column=0, columnspan=2)

        fenetre.mainloop()