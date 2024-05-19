# Chemin vers le fichier de données.
data_path = './data/mock_data_4.csv'

#Création des listes des filtres
list_erc = ["Sans ERC","Léger", "Modérée", "Sévère", "Dialisis"]
list_fish = ["Aucun", "del17p1", "t_1114", "t414", "amp1q211", "Autres"]

#Liste des menus
menu_eng =['🏠 Home', '🔎 Descriptive Statistics', '🩺 Survival Functions','👥 Groups Comparison', 
           '📖 Tests Comparisons', '📊 Survival Regression (Cox)','📈 Economic Analysis', '📚 Missing Data']

menu =  ["🏠 Accueil", "🔎 Statistiques descriptives", "🩺 Fonctions de Survie", "👥 Comparaison des Groupes",
         "📖 Comparaisons des Tests", "📊 Régression de Survie (Cox)", "📈 Analyse Economique", "📚 Données Manquantes"]

colors = [
    (255,   0,   0),
    (  0, 255,   0),
    (  0,   0, 255),
    (255, 128,   0),
    (  0, 255, 128),
    (128,   0, 255),
    (128, 255,   0),
    (  0, 128, 255),
    (255,   0, 128),
    (255, 255,   0),
    (  0, 255, 255),
    (255,   0, 255),
    (128, 128, 128),
]

colors_desc = ["#FF336E", "#5233FF", "#FF8033", "#1E8E26", "#8336AD", "#CDC521", "#21CDBD", "#520B0C"]


selected_cols_desc = {
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
    "Processus de redressement" : 'CoadOseo1', 
    "Adhésion de MM1M à 1" : "AdherienciaTtoMM1Mto1",
    "Opportunité de traitement" : "Oportunidadtratamiento",
    "Jour suspendu" : "Dias_suspendidos",
    "Jour en thérapie" : "Dias_en_terapia",
    "Date de réponse de la clinique" : "Fecha_respuesta_clinica",
    "Réponse de la clinique" : 'RespuestaClinica', 
    "Mortalité" : 'Evento', 
    "Durée" : "Time",
    "Traitement du myélome multiple 1": "TtoMM1",
    "Traitement du myélome multiple 2": "TtoMM2",
    "Hospitalisation ou non" : "hospitalisation_ou_non",
    "Durée avant l'hospitalisation" : "time_before_hospitalisation",
    "Tranche d'âge": "age_range",
    "Age": "age",
    "Pays": "country",
    "Hôpital" : "Hospital",
    "Type de myélome" : "TypeMyeloma",
    "Date de diagnostic" : "DateDiagnosis",
    "Prix" : "Cost",
    "Rémission" : "Remission"
}

selected_cols_desc_keys = list(selected_cols_desc.keys())

selected_cols_group = {
    "Genre": "Genero",
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
    "Processus de redressement" : 'CoadOseo1', 
    "Réponse de la clinique" : 'RespuestaClinica', 
    "Pays" : 'Country', 
    "Hôpital" : 'Hospital', 
    "Type de myélome" : 'TypeMyeloma',
    "Tranche d'âge" : 'Age_range', 
    "Mortalité" : 'Evento', 
    "Traitement du myélome multiple 1" : "TtoMM1",
    "Traitement du myélome multiple 2" : "TtoMM2"
}

selected_cols_group_keys = list(selected_cols_group.keys())

selected_cols_tests = {
    "Genre": "Genero",
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
    "Processus de redressement" : 'CoadOseo1', 
    "Réponse de la clinique" : 'RespuestaClinica', 
    "Pays" : 'Country', 
    "Hôpital" : 'Hospital', 
    "Type de myélome" : 'TypeMyeloma',
    "Mortalité" : 'Evento', 
    "Traitement du myélome multiple 1" : "TtoMM1",
    "Traitement du myélome multiple 2" : "TtoMM2"
}

selected_cols_tests_keys = list(selected_cols_tests.keys())


home = """
# Analyse de survie - M1 MIAGE

Clément Fresnel, Alexandra Martin, Zoé Martinez
Projet d’Ingénierie des Données - Master 1 MIAGE Polytech Lyon

## Définition 

L’analyse de survie de données est une méthode, tirée des sciences statistiques, utilisée dans de nombreuses sciences du vivant comme la médecine ou la biologie mais aussi parfois en ingénierie ou en économie. 
L’analyse de survie prédit grâce à des formules mathématiques le temps qu’il faudra à un événement, de quel type que ce soit (mort, défaillance, fin de contrat, …) pour se produire. 

On parle également d’analyse de durée de vie ou analyse de temps jusqu'à un événement.

## Données de survie

La variable Y à analyser correspond à une durée de processus ou de survenue d’un événement. C’est une données aléatoire continue qui dispose tout de même de deux caractéristiques majeures : 


ses valeurs sont positives ou nulles,



elle n’est pas forcément mesurée ou même observée pendant le temps de l’étude, Y est alors “censurée”.


La variable Y est constituée de deux paramètres : 


le temps, une variable continue,



la survenue, ou non, de l’événement, une variable discrète codée en binaire.



## Fonction de densité, de survie et de risque

### Fonction de densité 

La fonction de densité décrit la distribution des temps jusqu’à l’événement d’intérêt.

> Soit t (t > 0) le temps et μ (μ > 0) la durée moyenne de survie d’un individu, alors le modèle paramétrique de survie le plus simple correspond à un modèle exponentiel dont la fonction de densité est : 
> f(t) = (1/μ) e^(-(1/μ)t)
> Avec T la variable aléatoire continue et positive qui représente le temps de survie.

La fonction f de densité correspond à la proportion de survenue d’événement entre t et t+Δt rapporté au nombre total d’individus à l’instant initial t0.


### Fonction de répartition

La fonction de répartition associée à la fonction de densité donne la probabilité qu’un événement ne survienne pas au-delà d’un certain temps t. Les fonctions de densité et de répartition sont complémentaires : quand l’une donne la probabilité à un instant précis, l’autre donne la probabilité cumulative de survie jusqu’à un instant donné.

> Soit F la fonction de répartition associée à une fonction de densité : 
> F(t) = 1 - e^(-t/μ)
> Avec T la variable aléatoire continue et positive qui représente le temps de survie.

### Fonction de survie et de risque

La fonction S de survie est la probabilité qu’un individu survive jusqu’à l’instant t.

> Par définition : 
> S(0) = 1
> S(∞) = 0

La fonction h de risque correspond au taux de mortalité instantané entre t et t+Δt sachant que le temps de survie T est supérieur à t.

## Kaplan-Meier

Le modèle de Kaplan-Meier est une méthode statistique de l’étude de survie qui prend en compte la présence de données censurées. Il permet de calculer la fonction de survie empirique en divisant le temps en intervalles et en estimant la probabilité de survie pour chaque intervalle.

## Modèle de Cox

Le modèle de Cox exprime la fonction de risque h sous forme d’un produit correspondant aux quantités suivantes : 

h0 : le risque de base qui est fonction uniquement du temps mais indépendant des variables explicatives,


e^η : l’exponentiel du terne η à modéliser qui est fonction des variables explicatives mais totalement indépendant du temps.


Dans ce modèle, chaque variable explicative est indépendante du temps. 

# Description de la base de données 

Cette base de données regroupe des informations sur des patients.Chaque patient est identifié par un identifiant propre et unique, son sexe est repertorié ainsi que son IMC, son âge (et sa catégorie d’âge) et son régime d’affiliation à la sécurité sociale. Le pays et l’hôpital dans lesquels sont traités les patients sont renseignés. 
Les données de santé des patients sont décrites avec beaucoup de précision. On apprend notamment les symptômes, les facteurs de risques ou comorbidités, les réponses des patients aux différents traitements, … ainsi que des données relatives aux hospitalisations des patients.

"""




