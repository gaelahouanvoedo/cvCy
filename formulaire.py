import streamlit as st
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
    st.title("Formulaire de recrutement")
    
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
            st.success("Formulaire soumis avec succès !")
        else:
            st.warning("Veuillez remplir tous les champs du formulaire.")

# Créer la table dans la base de données (si elle n'existe pas déjà)
create_table()

# Exécuter l'application Streamlit
formulaire_recrutement()
