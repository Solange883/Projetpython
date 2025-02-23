from tkinter import *
from tkinter import Tk, Frame, Label, Entry, Button, Canvas, Scrollbar, messagebox,ttk
from calculrem import Notes
from fpdf import FPDF



class NotesManager:
    def __init__(self, db_manager, anonymat_manager):
        self.db_manager = db_manager
        self.anonymat_manager = anonymat_manager

    def ajouter_notes(self):
        def enregistrer():
            for champ, entry in entries.items():
                if not entry.get().strip():
                    messagebox.showerror("Erreur", f"Le champ '{champ}' est obligatoire.")
                    return

            anonymat_principal = entries["Anonymat Principal"].get()
            numero_table = self.anonymat_manager.recuperer_numero_table_par_anonymat(anonymat_principal)
            if not numero_table:
                messagebox.showerror("Erreur", "Anonymat principal non trouvé.")
                return


            notes = (
                numero_table, entries["Composition Français"].get(), entries["Dictée"].get(),
                entries["Étude de texte"].get(), entries["Instruction Civique"].get(),
                entries["Histoire Géographie"].get(), entries["Mathématiques"].get(),
                entries["PC/LV2"].get(), entries["SVT"].get(), entries["Anglais 1"].get(),
                entries["Anglais Oral"].get(), entries["EPS"].get(), entries["Épreuve Facultative"].get()
            )
            self.db_manager.insert_notes(notes)
            messagebox.showinfo("Succès", "Notes ajoutées avec succès")
            fenetre.destroy()

        fenetre = Tk()
        fenetre.title("Ajout Notes")
        fenetre.geometry("600x700")
        fenetre.configure(bg="#f0f8ff")

        Label(fenetre, text="Ajout des Notes", bg="#f0f8ff", fg="blue", font=("Helvetica", 14, "bold")).pack(pady=10)


        cadre_canvas = Frame(fenetre, bg="#f0f8ff")
        cadre_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = Canvas(cadre_canvas, bg="#f0f8ff", height=500)
        scrollbar = Scrollbar(cadre_canvas, orient="vertical", command=canvas.yview)
        contenu_frame = Frame(canvas, bg="#f0f8ff")

        contenu_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=contenu_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        champs = [
            "Anonymat Principal", "Composition Français", "Dictée", "Étude de texte", "Instruction Civique",
            "Histoire Géographie", "Mathématiques", "PC/LV2", "SVT", "Anglais 1", "Anglais Oral", "EPS",
            "Épreuve Facultative"
        ]

        entries = {}

        for i, champ in enumerate(champs):
            Label(contenu_frame, text=champ + ":", bg="#f0f8ff", fg="blue", font=("Helvetica", 12)).grid(row=i,
                                                                                                         column=0,
                                                                                                         sticky="w",
                                                                                                         pady=10)
            entry = Entry(contenu_frame, font=("Helvetica", 12), width=30, bd=2, relief="solid")
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries[champ] = entry

        bouton_enregistrer = Button(contenu_frame, text="Enregistrer", command=enregistrer,
                                    font=("Helvetica", 12, "bold"), fg="black", bg="#007bff",
                                    padx=20, pady=10, relief="solid", bd=3)
        bouton_enregistrer.grid(row=len(champs), column=0, columnspan=2, pady=20)

        fenetre.mainloop()





    def afficher_notes(self):

        notes = self.db_manager.fetch_notes2()

        fenetre_affichage = Tk()
        fenetre_affichage.title("Liste des notes")
        fenetre_affichage.geometry("900x500")
        fenetre_affichage.configure(bg="white")

        frame = Frame(fenetre_affichage)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        colonnes = ("N° de table",
                    "Note CF",
                    "Note Ort",
                    "Note TSQ",
                    "Note IC",
                    "Note HG",
                    "Note MATH",
                    "Note PC/LV2",
                    "Note SVT",
                    "Note ANG1",
                    "Note ANG2",
                    "Note EPS",
                    "Note Ep Fac")


        tree = ttk.Treeview(frame, columns=colonnes, show="headings")

        largeurs_colonnes = [100, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80]

        for col, largeur in zip(colonnes, largeurs_colonnes):
            tree.heading(col, text=col)  # Nom de la colonne
            tree.column(col, width=largeur, anchor="center")  # Largeur ajustée


        for note in notes:
            tree.insert("", "end", values=note)


        scrollbar_y = Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(frame, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)


        tree.pack(fill="both", expand=True)

        bouton_generer_pdf = Button(fenetre_affichage, text="Générer la liste des notes en PDF",
                                    command=self.generer_pdf_notes,
                                    font=("Helvetica", 12, "bold"), fg="black", bg="white", padx=10, pady=5)
        bouton_generer_pdf.pack(pady=10)


        fenetre_affichage.mainloop()

    def generer_pdf_notes(self):
        notes = self.db_manager.fetch_notes2()

        pdf = FPDF(orientation="L", unit="mm", format="A4")  # Mode paysage pour mieux afficher
        pdf.add_page()


        pdf.set_font("Arial", 'B', 14)
        pdf.cell(270, 10, txt="Liste des Notes des Candidats", ln=True, align="C")
        pdf.ln(10)  # Ajoute un espace


        pdf.set_font("Arial", size=10)


        colonnes = ["N°", "CF", "Ort", "TSQ", "IC", "HG", "MATH", "PC/LV2", "SVT", "ANG1", "ANG2", "EPS", "Ep Fac"]
        largeurs_colonnes = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]


        for col, largeur in zip(colonnes, largeurs_colonnes):
            pdf.cell(largeur, 8, col, border=1, align="C")
        pdf.ln()


        for note in notes:
            for data, largeur in zip(note, largeurs_colonnes):
                pdf.cell(largeur, 8, str(data), border=1, align="C")
            pdf.ln()


        pdf.output("Liste_des_notes_premierTour.pdf")
        messagebox.showinfo("Succès",
                            "Le PDF des notes (sous le nom Liste_des_notes.pdf) a été généré avec succès sur le dossier du projet !")

    def gerer_deliberation(self):
        self.fenetre_deliberation = Tk()
        self.fenetre_deliberation.title("Délibération des Candidats")
        self.fenetre_deliberation.geometry("600x400")

        Label(self.fenetre_deliberation, text="Délibération des Candidats du Premier Tour",
              font=("Arial", 14, "bold")).pack(pady=10)

        Button(self.fenetre_deliberation, text="Calculer les Résultats", command=self.afficher_resultats_PremierTour,
               bg="blue", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        self.resultat_text = Text(self.fenetre_deliberation, height=15, width=75)
        self.resultat_text.pack(pady=10)

        scrollbar = Scrollbar(self.fenetre_deliberation, command=self.resultat_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.resultat_text.config(yscrollcommand=scrollbar.set)

        Button(self.fenetre_deliberation, text="Générer PDF", command=self.generer_pdf_resultats,
               bg="blue", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        self.fenetre_deliberation.mainloop()

    def afficher_resultats_PremierTour(self):
        self.resultat_text.delete("1.0", "end")

        anonymats = self.anonymat_manager.recuperer_tous_anonymats_principal()
        anonymat_dict = {str(numero_table): str(anonymat_principal).strip() for numero_table, anonymat_principal in
                         anonymats}

        candidats = self.db_manager.fetch_candidats()
        for candidat in candidats:
            numero_table_candidat = str(candidat[0])
            anonymat_principal = anonymat_dict.get(numero_table_candidat, "Inconnu").strip()

            notes = self.db_manager.fetch_notes(candidat[0])
            if not notes:
                continue

            notes_obj = Notes(candidat[0], notes)
            resultats = notes_obj.calculer_resultats(self.db_manager)

            resultat_str = (f"Anonymat: {anonymat_principal} | "
                            f"Total: {resultats['total_points']} | "
                            f"Bonus EPS: {resultats['bonus_eps']} | "
                            f"Bonus Fac.: {resultats['bonus_facultatif']} | "
                            f"Décision: {resultats['decision']}\n")
            self.resultat_text.insert("end", resultat_str)

        if not self.resultat_text.get("1.0", "end-1c").strip():
            self.resultat_text.insert("end", "Aucun candidat trouvé pour le premier tour.\n")

    def generer_pdf_resultats(self):
        if not self.resultat_text.get("1.0", "end-1c").strip():
            messagebox.showerror("Erreur", "Aucun résultat à exporter en PDF.")
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Résultats du Premier Tour", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 10)
        colonnes = ["Anonymat", "Total", "Bonus EPS", "Bonus Fac.", "Décision"]
        largeurs_colonnes = [50, 30, 30, 30, 50]

        for col, largeur in zip(colonnes, largeurs_colonnes):
            pdf.cell(largeur, 8, col, border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", size=10)
        for row in self.resultat_text.get("1.0", "end-1c").splitlines():
            values = row.split('|')
            for value, largeur in zip(values, largeurs_colonnes):
                pdf.cell(largeur, 8, str(value).strip(), border=1, align="C")
            pdf.ln()

        pdf_filename = "resultats_premier_tour.pdf"
        pdf.output(pdf_filename)
        messagebox.showinfo("Succès", f"Le PDF {pdf_filename} a été généré avec succès dans le dossier du projet !")