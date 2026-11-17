
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Catalogue", page_icon="📚", layout="wide")

FICHIER = "data/livres_poetry.csv"

st.title("Catalogue de livres")
st.caption("Explore le catalogue de livres grâce aux filtres.")
@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)

df = charger_donnees(FICHIER)

# Filtres dans la barre latérale
st.sidebar.header("Filtres")

note_mini = st.sidebar.slider("Note minimale", 1, 5, 1)
prix_min, prix_max = st.sidebar.slider("Prix", 0.0, 60.0, (0.0, 60.0))
recherche = st.sidebar.text_input("Le titre contient")

# Application des filtres
selection = df.copy()

selection = selection[selection["note"] >= note_mini]
selection = selection[selection["prix_gbp"] >= prix_min]
selection = selection[selection["prix_gbp"] <= prix_max]

if recherche:
    selection = selection[
        selection["titre"].str.contains(recherche, case=False)
    ]

# Affichage des resultats
if len(selection) == 0:
    st.warning("Aucun livre ne correspond a ces criteres.")

else:
    # Quatre indicateurs en haut
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Livres retenus", len(selection))
    col2.metric("Prix moyen", f"{selection['prix_gbp'].mean():.2f} GBP")
    col3.metric("Note moyenne", f"{selection['note'].mean():.2f} / 5")
    col4.metric("Stock total", selection["stock"].sum())

    # Tableau des livres filtrés
    st.dataframe(selection)

    # Deux palmarès côte à côte
    gauche, droite = st.columns(2)

    with gauche:
        st.subheader("Les mieux notés")
        st.dataframe(selection.nlargest(5, "note")[["titre", "note"]])

    with droite:
        st.subheader("Les moins chers")
        st.dataframe(selection.nsmallest(5, "prix_gbp")[["titre", "prix_gbp"]])
# Donnees originales, accessibles meme si aucun livre n'est retenu
with st.expander("Voir les donnees brutes"):
    st.dataframe(df)
