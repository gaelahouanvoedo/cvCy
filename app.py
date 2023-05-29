# STARTING PAGE
import streamlit as st
from PIL import Image

st.set_page_config(
     page_title="cvCy - ♥ IA of Gael Ahouanvoedo",
     page_icon="🤥",
     initial_sidebar_state="expanded",
 )

with st.sidebar:
         image = Image.open('C:/Users/LENOVO/DATA/FUTURE/CV/log.png')
         st.image(image, width=180)
         with open('C:/Users/LENOVO/DATA/FUTURE/CV/CV.pdf', "rb") as file:
             btn = st.download_button(
             label="Télécharger mon CV",
             data=file,
             file_name="CV GAEL AHOUANVOEDO.pdf",
             mime="CV GAEL AHOUANVOEDO/pdf"
                )
             st.text('Pour toutes collaboration')
             menu = st.selectbox("",('Introduction',"Charger","Rechercher"))
             st.success("Lancez l'application ici")
             st.subheader("Informations")
             st.write("Cette application permet d'analyser les sentiments de données textuelles.",unsafe_allow_html=True)
             '***' 
             '**Build with ♥ by Gael Ahouanvoedo**'

if menu == ("Introduction"):
    

    st.write("""
    # Sélection de CV.
    
    Cette application permet de sélectionner le CV qui répond le mieux à une liste de compétences. 
                   
    """)
    
    ''
    ''
    
    st.write("""
    **👈 Pour continuer, sélectionnez "Lancer l'app" dans la barre latérale.**             
    """)
    
    st.write("""
    ### Credit
    Gael Ahouanvoedo, sayadebayo@gmail.com
                 
    """)

    
    st.write("""
    ### LinkedIn
    https://www.linkedin.com/in/gaelahouanvoedo/         
    """)
    
    st.write("""
    ### Avertissement
    Il s'agit uniquement d'une étude expérimentale et non d'un procédé exploitable auprès d'une structure tiers. Nous ne sommes en aucun cas, responsable d'une utilisation à des fins autre que de testing.
    """)

# FORMULAIRE

if menu == ("Charger"):
    #importer image
    image = Image.open('C:/Users/LENOVO/DATA/FUTURE/CV/log.png')
    #centrer image
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image(image, width=250)
    with col3:
        st.write(' ')
        
    
    # Titre de l'application
    st.title("Chargez un CV.")

    import sqlite3
    import os
    import PyPDF2

    # Vérifier si la base de données existe
    if not os.path.exists('C:/Users/LENOVO/DATA/FUTURE/CV/recrutement.db'):
        # Créer la base de données
        conn = sqlite3.connect('C:/Users/LENOVO/DATA/FUTURE/CV/recrutement.db')
        conn.close()

    # Fonction pour créer la table dans la base de données
    def create_table():
        conn = sqlite3.connect('C:/Users/LENOVO/DATA/FUTURE/CV/recrutement.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS candidats
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    prenom TEXT,
                    email TEXT,
                    cv TEXT)''')
        conn.commit()
        conn.close()

    # Fonction pour extraire le texte d'un fichier PDF
    def extract_text_from_pdf(file):
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page).extractText()
        return text

    # Fonction pour extraire le texte d'un fichier DOCX
    def extract_text_from_docx(file):
        doc = Document(file)
        paragraphs = doc.paragraphs
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text + "\n"
        return text

    # Fonction pour insérer les données dans la base de données
    def insert_data(nom, prenom, email, cv):
        if cv.type == "application/pdf":
            cv_text = extract_text_from_pdf(cv)
        else:
            st.warning("Format de fichier non pris en charge. Veuillez télécharger un fichier PDF.")
            return
        
        conn = sqlite3.connect('C:/Users/LENOVO/DATA/FUTURE/CV/recrutement.db')
        c = conn.cursor()
        c.execute("INSERT INTO candidats (nom, prenom, email, cv) VALUES (?, ?, ?, ?)",
                (nom, prenom, email, cv_text))
        conn.commit()
        conn.close()

    # Fonction principale de l'application Streamlit
    def formulaire_recrutement():
        
        # Champ Nom
        nom = st.text_input("Nom")
        
        # Champ Prénom
        prenom = st.text_input("Prénom")
        
        # Champ Adresse e-mail
        email = st.text_input("Adresse e-mail")
        
        # Champ CV (Téléchargement de fichier)
        cv = st.file_uploader("CV du candidat", type=["pdf"])
        
        # Bouton de soumission
        if st.button("Soumettre"):
            if nom and prenom and email and cv:
                # Insérer les données dans la base de données
                insert_data(nom, prenom, email, cv)
                st.success("CV soumis avec succès !")
            else:
                st.warning("Veuillez remplir tous les champs du formulaire.")

    # Créer la table dans la base de données (si elle n'existe pas déjà)
    create_table()

    # Exécuter l'application Streamlit
    formulaire_recrutement()

#APP

import os
import PyPDF2
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings(action = 'ignore')



if menu == ("Rechercher"):
    #importer image
    image = Image.open('C:/Users/LENOVO/DATA/FUTURE/CV/log.png')
    #centrer image
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image(image, width=250)
    with col3:
        st.write(' ')
        
    
    # Titre de l'application
    st.title("Trouvez le meilleur canditat.")

    import os
    import PyPDF2
    import pandas as pd
    import streamlit as st

    import sqlite3

    # Établir une connexion à la base de données
    conn = sqlite3.connect('C:/Users/LENOVO/DATA/FUTURE/CV/recrutement.db')

    # Créer un curseur pour exécuter des requêtes SQL
    cur = conn.cursor()

    # Exécuter une requête SQL pour extraire la table (remplacez "nom_table" par le nom réel de la table)
    cur.execute('SELECT * FROM candidats')

    # Récupérer les résultats de la requête dans une liste de tuples
    table_data = cur.fetchall()

    # Récupérer les noms des colonnes de la table
    column_names = [description[0] for description in cur.description]

    # Fermer le curseur et la connexion à la base de données
    cur.close()
    conn.close()

    # Créer un dataframe à partir des données récupérées
    df = pd.DataFrame(table_data, columns=column_names)

    df.drop(['id'],axis=1,inplace=True)

    # Champ de saisie pour l'utilisateur
    user_input = st.text_input("Saisir des compétences séparées par des virgules : ")

    # Stocker les valeurs saisies dans une liste
    competences = user_input.split(',')

    # Bouton pour lancer la recherche
    if st.button("Rechercher"):

        # Création du DataFrame df_select vide
        df_select = pd.DataFrame(columns=df.columns)

        # Parcours du DataFrame df
        for index, row in df.iterrows():
            cv = row['cv']
            for competence in competences:
                if competence.lower() in cv.lower():
                    df_select = df_select.append(row, ignore_index=True)
                    break

        # Ajouter une nouvelle colonne "skills" à df_select
        df_select['skills'] = df_select['cv'].apply(lambda x: [comp for comp in competences if comp.lower() in x.lower()])
        df_select.drop(['cv'],axis=1,inplace=True)

        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        # Créer une instance de CountVectorizer
        vectorizer = CountVectorizer()

        # Transformer les compétences en une matrice de vecteurs
        skills_matrix = vectorizer.fit_transform(df_select['skills'].apply(lambda x: ', '.join(x)))

        # Calculer la similarité cosinus entre les compétences recherchées et les compétences de chaque ligne
        similarity_scores = cosine_similarity(skills_matrix, vectorizer.transform([', '.join(competences)]))

        # Ajouter une colonne "similarity" au DataFrame df_select avec les scores de similarité
        df_select['similarite'] = similarity_scores.flatten()
        df_select = df_select.sort_values('similarite', ascending=False)


        # Afficher le DataFrame df_select avec la colonne "similarity"
        st.write(df_select)




        
        

    
         
