# Chemin vers le fichier de données.
data_path = './data/mock_data_4.csv'

#Création des listes des filtres
list_erc = ["Sans ERC","Léger", "Modérée", "Sévère", "Dialisis"]
list_fish = ["Aucun", "del17p1", "t_1114", "t414", "amp1q211", "Autres"]

#Liste des menus
menu_eng =['Descriptive Statistics', 'Survival Functions','Groups Comparison', 
           'Tests Comparisons', 'Survival Regression (Cox)','Economic Analysis', 'Missing Data']

menu =  [ "Statistiques descriptives", "Fonctions de Survie", "Comparaison des Groupes",
         "Comparaisons des Tests", "Régression de Survie (Cox)", "Analyse Economique", "Données Manquantes"]

# Création du menu :
#   id : identifiant de l'onglet (facultatif).
#   label : Le nom de l'onglet tel qu'il apparaît dans le menu.
#   icon : un emoji ou un faticon visible sur l'onglet dans le menu.
menu_icons = [
    {'label': "Accueil", 'icon': "🏠", 'id': "home"},
    {'label': "Statistiques descriptives", 'icon': "🏠", 'id': "statistiques"},
    {'label': "Fonctions de Survie", 'icon': "📖", 'id': "survie"},
    {'label': "Comparaison des Groupes", 'icon': "⚙️", 'id': "groupes"},
    {'label': "Comparaisons des Tests", 'icon': "🧮", 'id': "tests"},
    {'label': "Régression de Survie (Cox)", 'icon': "📊", 'id': "regression"},
    {'label': "Analyse Economique", 'icon': "📈", 'id': "economique"},
    {'label': "Données Manquantes", 'icon': "🔎", 'id': "data_manquante"}
]

# Création d'une liste de colonnes pour créer les filtres dans l'application.
# clé: valeur
# [nom compréhensible]: [nom de la colonne]
option_descriptives = {
    "Temps": "time",
    "Mortalité": "Evento",
    "Indice de Masse Corporelle": "IMC",
    "Assurance maladie": "Regimenafiliacion",
    "Anémie": "Anemia",
    "Fragilité": "Fragilidad",
    "FISH (del17p1)": "FISHdel17p1",
    "Sous-classification par plateforme": "SubclasificacionplataformaMM",
    "ISS par la plateforme": "ISSPlataforma1",
    "Traitement du myélome multiple 1": "TtoMM1",
    "Traitement du myélome multiple 2": "TtoMM2",
    "Temps avant hospitalisation": "time2",
    "Hospitalisation": "hospitalisation",
    "Tranche d'âge": "age_range",
    "Age": "age",
    "Pays": "country",
}


filters = {
    "Genre": "Genero",
    "Indice de Masse Corporelle": "IMC",
    "Assurance maladie": "Regimenafiliacion",
    "Anémie": "Anemia",
    "Hypercalcémie": "Hipercalcemia",
    "Examen Clinique Rationnel(ECR) Léger": "ERC_Leve",
    "Examen Clinique Rationnel(ECR) Modérée": "ERC_moderada",
    "Examen Clinique Rationnel(ECR) Sévère": "ERC_severa",
    "Examen Clinique Rationnel(ECR) Dialisis": "ERC_dialisis",
    "Lésions Osseuses": "Lesiones_oseas",
    "Infections Récurentes": "Infecciones_recurrentes",
    "Fragilité": "Fragilidad",
    "FISH (del17p1)": "FISHdel17p1",
    "FISH (t_1114)": "FISHt_1114",
    "FISH (t414)": "FISHt414",
    "FISH (amp1q211)": "FISHamp1q211",
    "FISH other": "FISHother",
    "Sous-classification par plateforme": "SubclasificacionplataformaMM",
    "ISS par la plateforme": "ISSPlataforma1",
    "Traitement du myélome multiple 1": "TtoMM1",
    "Traitement du myélome multiple 2": "TtoMM2",
    "Tranche d'âge": "age_range",
    "Age": "age",
    "Pays": "country",
}
#CoadOseo1 il en manque pas mal je trouve