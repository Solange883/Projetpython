#DEUXIEMETOUR


class Notes2:
    def __init__(self, numero_table, notes,nbre_fois=None,moyenne_cycle=None):
        self.numero_table = numero_table

        #converir tuple en dico
        if isinstance(notes, tuple):

            self.notes = {
                " Francais": notes[1],
                "Mathematiques": notes[2],
                "PC/LV2": notes[3],

            }
        else:
            self.notes = notes if notes else {i: 0 for i in range(1, 4)}

        self.moyenne_cycle = moyenne_cycle
        self.nbre_fois = nbre_fois
        self.total_points = 0
        self.decision = ""


    def calcul_total_points(self):

        coef_notes = {
            "Francais": 3, "Mathematiques": 3, "PC/LV2": 2
        }

        total = 0
        for matiere, coef in coef_notes.items():
            note = self.notes.get(matiere, 0)  #si ya pas de note on utilise 0
            if note is None:
                note = 0
            total += note * coef
        self.total_points = total


    def determiner_decision(self, db_manager):
        """Détermine la décision en fonction des règles métiers."""

        # Récupérer la moyenne du cycle depuis la table LivretScolaire
        self.moyenne_cycle ,self.nbre_fois= db_manager.fetch_moyenne_cycle(self.numero_table)

        # RM11 : Admis si total_points >= 80
        if self.total_points >= 80:
            self.decision = "Admis"
            return

        # RM12 : Vérifier si le candidat a passé le BFEM plus de 2 fois
        if self.nbre_fois > 2:
            self.decision = "Échec"
            return

        # RM11 : Repêchable si 76 <= total_points < 80
        if 76 <= self.total_points < 80:
            self.decision = "Repêchable pour passer le second tour"
            return

        # Si total_points < 76, le candidat est éliminé
        self.decision = "Échec"






    def calculer_resultats(self,db_manager):
        self.calcul_total_points()
        self.determiner_decision(db_manager)
        return {
            "total_points": self.total_points,
            "decision": self.decision
        }
