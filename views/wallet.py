import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np
import ta

def show_wallet():
    st.title("Wallet View")

    st.subheader("Répartition du portefeuille")
    col1, col2 = st.columns([2, 1])

     # Fonction pour récupérer les données actuelles des actifs
    @st.cache_data(ttl=300)  # Cache de 5 minutes
    def get_current_asset_data(symbols_dict):
        portfolio_data = []
        total_value = 0
        
        for name, quantity in symbols_dict.items():
            try:
                symbol = {
                    'Bitcoin': 'BTC-USD',
                    'Ethereum': 'ETH-USD',
                    'Solana': 'SOL-USD',
                    'Tesla': 'TSLA'
                }.get(name)
                
                if symbol is None:
                    st.warning(f"Symbole non trouvé pour {name}")
                    continue
                
                ticker = yf.Ticker(symbol)
                current_data = ticker.history(period='2d')  # 2 jours pour calculer la variation
                
                if not current_data.empty:
                    current_price = current_data['Close'].iloc[-1]
                    prev_price = current_data['Close'].iloc[0]
                    value = current_price * quantity
                    perf_24h = ((current_price - prev_price) / prev_price) * 100
                    
                    portfolio_data.append({
                        'Actif': name,
                        'Quantité': quantity,
                        'Prix actuel': current_price,
                        'Valeur totale': value,
                        'Performance 24h': f"{'↗️' if perf_24h >= 0 else '↘️'} {perf_24h:.2f}%"
                    })
                    
                    total_value += value

                    # Debug info
                    st.write(f"INFO : Données récupérées pour {name}: Prix = ${current_price:.2f}")
                else:
                    st.warning(f"Aucune donnée disponible pour {name}")
                
            except Exception as e:
                st.error(f"Erreur lors de la récupération des données pour {name}: {str(e)}")
        
        if not portfolio_data:
            return pd.DataFrame(), 0
            
        df = pd.DataFrame(portfolio_data)
        # Trier par valeur totale décroissante
        df = df.sort_values('Valeur totale', ascending=False)
        return df, total_value

    # Définition du portefeuille (quantités détenues)
    portfolio = {
        'Bitcoin': 0.5,
        'Ethereum': 4.2,
        'Solana': 25.0,
        'Tesla': 10
    }

    # Récupération des données actuelles
    portfolio_assets, total_portfolio_value = get_current_asset_data(portfolio)
    
    # Mise à jour des métriques du portfolio en haut de page
    col1.metric(
        label="Valeur totale du portefeuille",
        value=f"${total_portfolio_value:,.2f}",
        delta=f"{portfolio_assets['Performance 24h'].iloc[0]}" if not portfolio_assets.empty else None
    )
    
    with col1:
        if not portfolio_assets.empty:
            st.dataframe(
                portfolio_assets,
                column_config={
                    "Prix actuel": st.column_config.NumberColumn(
                        "Prix actuel",
                        format="$%.2f"
                    ),
                    "Valeur totale": st.column_config.NumberColumn(
                        "Valeur totale",
                        format="$%.2f"
                    )
                },
                hide_index=True
            )
        else:
            st.warning("Impossible de charger les données du portefeuille")
    
    with col2:
        if not portfolio_assets.empty:
        # Graphique en donut de répartition
            fig = go.Figure(data=[go.Pie(
                labels=portfolio_assets['Actif'],
                values=portfolio_assets['Valeur totale'],
                hole=.3
            )])
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0)
            )
        st.plotly_chart(fig, use_container_width=True)

    # Quatrième section : Activité récente
    st.subheader("Activité récente")
    activities = [
        {"date": "2024-03-20 14:30", "type": "Achat", "details": "0.1 BTC à $41,500"},
        {"date": "2024-03-19 09:15", "type": "Vente", "details": "100 SOL à $95"},
        {"date": "2024-03-18 16:45", "type": "Achat", "details": "2 ETH à $2,150"}
    ]
    
    for activity in activities:
        col1, col2, col3 = st.columns([2, 2, 4])
        with col1:
            st.text(activity["date"])
        with col2:
            st.text("🟢" if activity["type"] == "Achat" else "🔴" + " " + activity["type"])
        with col3:
            st.text(activity["details"])
        st.markdown("---")
