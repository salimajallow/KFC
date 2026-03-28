import streamlit as st
import os
from utils.data_loader import charger_donnees, nettoyer_donnees, calculer_indicateurs, afficher_info_donnees
from utils.plots import afficher_tous_les_graphiques

# Configuration de la page
st.set_page_config(
    page_title="Dashboard KFC Sénégal",
    page_icon="🍗",
    layout="wide"
)

# Titre
st.title("🍗 Dashboard des commandes KFC Sénégal")
st.markdown("---")

# Barre latérale
st.sidebar.header("🎛️ Menu")
st.sidebar.markdown("Bienvenue sur votre tableau de bord KFC Sénégal")
st.sidebar.markdown("---")
st.sidebar.markdown("**Filtres disponibles :**")
st.sidebar.info("Utilisez les onglets ci-dessous pour explorer les données")

# Chercher le fichier Excel
dossier_donnees = "data"
fichiers_excel = []

if os.path.exists(dossier_donnees):
    for fichier in os.listdir(dossier_donnees):
        if fichier.endswith(('.xlsx', '.xls')):
            fichiers_excel.append(fichier)

if fichiers_excel:
    fichier = fichiers_excel[0]
    chemin = os.path.join(dossier_donnees, fichier)
    
    st.sidebar.success(f"📁 Fichier chargé : {fichier}")
    
    # Charger les données
    df = charger_donnees(chemin)
    
    if df is not None:
        # Nettoyer les données
        df = nettoyer_donnees(df)
        
        # Calculer les indicateurs
        indicateurs = calculer_indicateurs(df)
        
        # Afficher les indicateurs en haut
        st.subheader("📊 Indicateurs clés")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Chiffre d'affaires total", indicateurs['ca_total_format'])
        
        with col2:
            st.metric("📦 Nombre de commandes", f"{indicateurs['nb_commandes']:,}")
        
        with col3:
            st.metric("🛒 Panier moyen", indicateurs['panier_moyen_format'])
        
        with col4:
            st.metric("🏪 Nombre de restaurants", f"{df['restaurant_name'].nunique()}")
        
        st.markdown("---")
        
        # Onglets pour organiser
        onglet1, onglet2, onglet3 = st.tabs(["📊 Visualisations", "📋 Détails des données", "🔍 Données brutes"])
        
        with onglet1:
            afficher_tous_les_graphiques(df)
        
        with onglet2:
            afficher_info_donnees(df)
        
        with onglet3:
            st.subheader("📄 Données complètes")
            st.dataframe(df)
            # Ajouter un bouton pour télécharger
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données (CSV)",
                data=csv,
                file_name='donnees_kfc.csv',
                mime='text/csv',
            )
        
        # Pied de page
        st.markdown("---")
        st.markdown(f"📊 Tableau de bord mis à jour | {len(df):,} commandes analysées")
        st.markdown("🍗 KFC Sénégal - Analyse des ventes")
        
else:
    st.error("❌ Aucun fichier Excel trouvé dans le dossier 'data'")
    st.info("""
    **Comment faire ?**
    1. Placez votre fichier Excel (.xlsx) dans le dossier `data`
    2. Assurez-vous que le fichier a une extension .xlsx
    3. Rechargez cette page en appuyant sur le bouton "Rerun" en haut à droite
    """)