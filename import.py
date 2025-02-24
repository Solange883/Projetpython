import sqlite3
import pandas as pd


df = pd.read_excel("BD_BFEM.xlsx")


df['Date de nais.'] = pd.to_datetime(df['Date de nais.']).dt.date



conn = sqlite3.connect("BD_BFEM.sqlite")


cursor = conn.cursor()


df_candidats = df[['N° de table', 'Prenom (s)', 'NOM', 'Date de nais.', 'Lieu de nais.', 'Sexe','Type de candidat','Etablissement', 'Nationnallité', 'Etat Sportif', 'Epreuve Facultative']]
df_candidats.to_sql("Candidats", conn, if_exists="replace", index=False)

df_livret = df[['N° de table', 'Nb fois', 'Moy_6e', 'Moy_5e', 'Moy_4e',
    'Moy_3e']]

df_livret['Moy_Cycle'] = (df_livret['Moy_6e'] + df_livret['Moy_5e'] + df_livret['Moy_4e'] + df_livret['Moy_3e']) / 4
df_livret.to_sql('Livret_Scolaire', conn, if_exists='replace', index=False)



df_notes = df[[
    'N° de table','Note CF','Note Ort','Note TSQ','Note IC','Note HG','Note MATH','Note PC/LV2','Note SVT','Note ANG1',
'Note ANG2','Note EPS','Note Ep Fac']]



df_notes.to_sql("Notes", conn, if_exists="replace", index=False)


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables existantes :", cursor.fetchall())

# affichagede quelquesdonnees
cursor.execute("SELECT * FROM Candidats LIMIT 5;")
print("Exemple de données 'candidats' :", cursor.fetchall())

cursor.execute("SELECT * FROM Livret_Scolaire LIMIT 5;")
print("Exemple de données 'livrets' :", cursor.fetchall())

cursor.execute("SELECT * FROM Notes LIMIT 5;")
print("Exemple de données 'notes' :", cursor.fetchall())


conn.close()
