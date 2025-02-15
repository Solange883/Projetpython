


class Notes:
    def __init__(self, numero_table, notes):
        self.numero_table = numero_table

        #converir tuple en dico
        if isinstance(notes, tuple):

            self.notes = {
                "compo_franc": notes[1],
                "dictee": notes[2],
                "etude_de_texte": notes[3],
                "instruction_civique": notes[4],
                "histoire_geographie": notes[5],
                "mathematiques": notes[6],
                "pc_lv2": notes[7],
                "svt": notes[8],
                "anglais1": notes[9],
                "anglais_oral": notes[10],
                "eps": notes[11],
                "epreuve_fac": notes[12],
            }
        else:
            self.notes = notes if notes else {i: 0 for i in range(1, 13)}
        self.bonus_eps = 0
        self.bonus_facultatif = 0
        self.total_points = 0
        self.decision = ""



    def calcul_bonus(self):
       #bonus de leps et epreuvefac
        eps = self.notes.get("eps", 0)  # Note EPS
        epreuve_fac = self.notes.get("epreuve_fac", 0)


        if epreuve_fac is None:
            epreuve_fac = 0


        if eps is None:
            eps = 0


        if eps >= 10:
                self.bonus_eps = eps - 10  # Bonus si EPS >= 10
        else:
                self.bonus_eps = eps - 10  # Malus si EPS < 10


        if epreuve_fac > 10:
            self.bonus_facultatif = (epreuve_fac - 10) / 2

    def calcul_total_points(self):

        coef_notes = {
            "compo_franc": 2, "dictee": 1, "etude_de_texte": 1, "instruction_civique": 1,
            "histoire_geographie": 2, "mathematiques": 4, "pc_lv2": 2, "svt": 2,
            "anglais1": 2, "anglais_oral": 1
        }

        total = 0
        for matiere, coef in coef_notes.items():
            note = self.notes.get(matiere, 0)  #si ya pas de note on utilise 0
            if note is None:
                note = 0
            total += note * coef
        self.total_points = total + self.bonus_eps + self.bonus_facultatif

    def determiner_decision(self):

        seuil_admission = 180
        seuil_repechage = 160

        if self.total_points >= seuil_admission:
            self.decision = "Admis"
        elif self.total_points >= seuil_repechage:
            self.decision = "Repêchage"
        else:
            self.decision = "Échec"

    def calculer_resultats(self):
        self.calcul_bonus()
        self.calcul_total_points()
        self.determiner_decision()
        return {
            "total_points": self.total_points,
            "bonus_eps": self.bonus_eps,
            "bonus_facultatif": self.bonus_facultatif,
            "decision": self.decision
        }




