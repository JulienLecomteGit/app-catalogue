
import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.stop()

# Deux graphiques cote a cote
gauche, droite = st.columns(2)

with gauche:
    st.subheader("Comment les prix se distribuent-ils ?")

    fig = px.histogram(
        selection,
        x="prix_gbp",
        nbins=10,
        labels={"prix_gbp": "Prix (GBP)"},
        title=f"Répartition des prix de {len(selection)} livres",
    )

    st.plotly_chart(fig, width="stretch")
    st.caption(
        f"Les prix vont de {selection['prix_gbp'].min():.2f} "
        f"à {selection['prix_gbp'].max():.2f} GBP, "
        f"avec une moyenne de {selection['prix_gbp'].mean():.2f} GBP."
    )
with droite:
    st.subheader("Combien de livres par note ?")

    par_note = selection["note"].value_counts().sort_index()

    st.bar_chart(par_note)
    notes_en_tete = par_note[par_note == par_note.max()]

    if len(notes_en_tete) > 1:
        st.caption(
            f"{len(notes_en_tete)} notes sont à égalité en tête, "
            f"avec {par_note.max()} livres chacune."
        )
    else:
        st.caption(
            f"La note {notes_en_tete.index[0]} est la plus fréquente, "
            f"avec {par_note.max()} livres."
        )

# Relation entre la note, le prix et le stock
st.subheader("Le prix ou le stock sont-ils liés à la note ?")

# Choix de la variable en abscisse
choix_x = st.selectbox(
    "Variable en abscisse",
    ["Prix (GBP)", "Stock (exemplaires)"]
)

# Correspondance avec les colonnes du CSV
if choix_x == "Prix (GBP)":
    axe_x = "prix_gbp"
else:
    axe_x = "stock"

# Construction du graphique
fig = px.scatter(
    selection,
    x=axe_x,
    y="note",
    size="stock",
    hover_name="titre",
    labels={
        "prix_gbp": "Prix (GBP)",
        "stock": "Stock (exemplaires)",
        "note": "Note sur 5"
    },
    title=f"Relation avec la note pour {len(selection)} livres",
)

# Affichage du graphique
st.plotly_chart(fig, width="stretch")
if (
    len(selection) < 3
    or selection["note"].min() == selection["note"].max()
    or selection[axe_x].min() == selection[axe_x].max()
):
    st.caption(
        "La sélection est trop petite ou une variable est constante : "
        "impossible d'interpréter correctement la corrélation."
    )
else:
    correlation = selection[axe_x].corr(selection["note"])

    st.caption(
        f"Corrélation entre {choix_x} et la note : {correlation:.2f}. "
        "Plus cette valeur est proche de zéro, "
        "moins la relation linéaire est marquée."
    )