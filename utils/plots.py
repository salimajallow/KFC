import plotly.express as px
import streamlit as st
import pandas as pd

def graphique_evolution_ca(df):
    """Évolution du CA par jour"""
    df_journalier = df.groupby('date_commande')['ca_ligne'].sum().reset_index()
    fig = px.line(df_journalier, x='date_commande', y='ca_ligne', 
                  title='📈 Évolution du Chiffre d\'Affaires',
                  labels={'ca_ligne': 'CA (FCFA)', 'date_commande': 'Date'})
    return fig

def graphique_ca_par_restaurant(df):
    """CA par restaurant"""
    ca_resto = df.groupby('restaurant_name')['ca_ligne'].sum().sort_values(ascending=True)
    fig = px.bar(ca_resto, x=ca_resto.values, y=ca_resto.index, orientation='h',
                 title='🏢 CA par restaurant',
                 labels={'x': 'CA (FCFA)', 'y': 'Restaurant'})
    return fig

def graphique_commandes_par_jour(df):
    """Nombre de commandes par jour de la semaine"""
    commandes_jour = df.groupby('jour').size().reset_index(name='nb_commandes')
    
    # Ordonner les jours en FRANÇAIS (Lundi à Dimanche)
    ordre_jours_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    commandes_jour['jour'] = pd.Categorical(commandes_jour['jour'], categories=ordre_jours_fr, ordered=True)
    commandes_jour = commandes_jour.sort_values('jour')
    
    fig = px.bar(commandes_jour, x='jour', y='nb_commandes',
                 title='📅 Nombre de commandes par jour',
                 labels={'nb_commandes': 'Nombre de commandes', 'jour': 'Jour'})
    return fig

def graphique_heatmap_jour_heure(df):
    """Carte de chaleur des commandes par jour et heure"""
    # Compter les commandes par jour et heure
    heatmap_data = df.groupby(['jour', 'heure']).size().unstack(fill_value=0)
    
    # Réordonner les jours en FRANÇAIS (Lundi à Dimanche)
    ordre_jours_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    heatmap_data = heatmap_data.reindex(ordre_jours_fr)
    
    fig = px.imshow(heatmap_data, 
                    title='🔥 Volume de commandes par jour et heure',
                    labels={'x': 'Heure', 'y': 'Jour', 'color': 'Nombre de commandes'},
                    color_continuous_scale='YlOrRd')
    return fig

def graphique_distribution_paiement(df):
    """Répartition par mode de paiement"""
    paiement_counts = df['modedepayement'].value_counts().reset_index()
    paiement_counts.columns = ['Mode de paiement', 'Nombre']
    fig = px.pie(paiement_counts, values='Nombre', names='Mode de paiement',
                 title='💳 Répartition des modes de paiement')
    return fig

def graphique_top_zones(df):
    """Répartition par zone de livraison"""
    zone_counts = df['zone de livraison'].value_counts().head(10).reset_index()
    zone_counts.columns = ['Zone', 'Nombre']
    fig = px.bar(zone_counts, x='Zone', y='Nombre',
                 title='📍 Top 10 des zones de livraison',
                 labels={'Nombre': 'Nombre de commandes'})
    return fig

def graphique_distribution_statuts(df):
    """Répartition par statut de commande"""
    status_counts = df['statut_name'].value_counts().reset_index()
    status_counts.columns = ['Statut', 'Nombre']
    fig = px.pie(status_counts, values='Nombre', names='Statut',
                 title='📋 Répartition des statuts de commande')
    return fig

def afficher_tous_les_graphiques(df):
    """
    Affiche tous les graphiques
    """
    st.subheader("📊 Visualisations")
    
    # Ligne 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(graphique_evolution_ca(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(graphique_ca_par_restaurant(df), use_container_width=True)
    
    # Ligne 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(graphique_commandes_par_jour(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(graphique_distribution_paiement(df), use_container_width=True)
    
    # Ligne 3
    st.plotly_chart(graphique_heatmap_jour_heure(df), use_container_width=True)
    
    # Ligne 4
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(graphique_top_zones(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(graphique_distribution_statuts(df), use_container_width=True)