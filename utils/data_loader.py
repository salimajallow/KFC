import pandas as pd
import streamlit as st

@st.cache_data
def charger_donnees(chemin_fichier):
    """
    Charge les données depuis un fichier Excel
    """
    try:
        df = pd.read_excel(chemin_fichier, engine='openpyxl')
        st.success(f"✅ Données chargées : {len(df)} lignes")
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {e}")
        return None

def nettoyer_donnees(df):
    """
    Nettoie et prépare les données pour KFC Sénégal
    """
    df = df.copy()
    
    # 1. Convertir la date
    df['date_commande'] = pd.to_datetime(df['date_commande'])
    
    # 2. Créer les colonnes de temps en FRANÇAIS
    # Dictionnaire pour traduire les jours
    jours_en_francais = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        'Sunday': 'Dimanche'
    }
    
    # Dictionnaire pour traduire les mois
    mois_en_francais = {
        'January': 'Janvier',
        'February': 'Février',
        'March': 'Mars',
        'April': 'Avril',
        'May': 'Mai',
        'June': 'Juin',
        'July': 'Juillet',
        'August': 'Août',
        'September': 'Septembre',
        'October': 'Octobre',
        'November': 'Novembre',
        'December': 'Décembre'
    }
    
    # Appliquer les traductions
    df['jour'] = df['date_commande'].dt.day_name().map(jours_en_francais)
    df['mois'] = df['date_commande'].dt.month_name().map(mois_en_francais)
    df['annee'] = df['date_commande'].dt.year
    df['heure'] = df['date_commande'].dt.hour
    
    # 3. Créer des tranches horaires
    def tranche_horaire(h):
        if 6 <= h < 11: return 'Matin (6h-10h)'
        elif 11 <= h < 15: return 'Déjeuner (11h-14h)'
        elif 15 <= h < 18: return 'Goûter (15h-17h)'
        elif 18 <= h < 23: return 'Dîner (18h-22h)'
        else: return 'Nuit (23h-5h)'
    
    df['tranche_horaire'] = df['heure'].apply(tranche_horaire)
    
    # 4. Renommer la colonne total en ca_ligne (pour faciliter)
    if 'total' in df.columns:
        df['ca_ligne'] = df['total']
    
    # 5. Nettoyer les noms des colonnes (enlever les espaces)
    df.columns = df.columns.str.strip()
    
    return df

def calculer_indicateurs(df):
    """
    Calcule les indicateurs clés
    """
    ca_total = df['ca_ligne'].sum()
    nb_commandes = df['numero_commande'].nunique()
    panier_moyen = ca_total / nb_commandes if nb_commandes > 0 else 0
    
    return {
        'ca_total': ca_total,
        'nb_commandes': nb_commandes,
        'panier_moyen': panier_moyen,
        'ca_total_format': f"{ca_total:,.0f} FCFA",
        'panier_moyen_format': f"{panier_moyen:,.0f} FCFA"
    }

def afficher_info_donnees(df):
    """
    Affiche les informations sur les données
    """
    st.subheader("📋 Informations sur les données")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📦 Nombre de commandes", f"{len(df):,}")
    
    with col2:
        st.metric("🏪 Nombre de restaurants", f"{df['restaurant_name'].nunique():,}")
    
    with col3:
        st.metric("👥 Nombre de clients", f"{df['client_name'].nunique():,}")
    
    st.write("**Aperçu des données :**")
    st.dataframe(df.head())