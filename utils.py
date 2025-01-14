import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .models import Transaction
from datetime import datetime

def generate_expense_chart(chart_type='bar'):
    transactions = Transaction.query.all()
    if not transactions:
        return None
        
    # Création du DataFrame avec toutes les transactions
    df = pd.DataFrame([{
        'type': t.type,
        'amount': t.amount if t.type == 'revenu' else -t.amount,  # Montant négatif pour les dépenses
        'category': t.category,
        'date': t.date,
        'month_year': t.date.strftime('%Y-%m')
    } for t in transactions])
    
    # Trier les transactions par date
    df = df.sort_values('date')
    
    if chart_type == 'line':
        # Calculer le solde cumulatif
        df['balance'] = df['amount'].cumsum()
        
        # Créer la figure
        fig = go.Figure()
        
        # Ajouter la ligne du solde
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['balance'],
            mode='lines',
            name='Solde',
            line=dict(
                color='rgb(136, 132, 216)',
                width=3
            ),
            fill='tonexty',
            fillcolor='rgba(136, 132, 216, 0.1)'
        ))
        
        # Ajouter les points
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['balance'],
            mode='markers',
            name='Transactions',
            marker=dict(
                size=8,
                color=df['balance'].apply(lambda x: 'green' if x >= 0 else 'red'),
                line=dict(
                    color='white',
                    width=1
                )
            ),
            hovertemplate="<b>Date:</b> %{x|%d/%m/%Y}<br>" +
                         "<b>Solde:</b> %{y:.2f}€<br>" +
                         "<extra></extra>"
        ))

        # Ligne horizontale à y=0
        fig.add_hline(
            y=0,
            line_width=1,
            line_dash="dash",
            line_color="gray",
            opacity=0.5
        )

        # Mise à jour du layout
        fig.update_layout(
            title={
                'text': 'Évolution du solde dans le temps',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            xaxis=dict(
                title="Date",
                gridcolor='rgba(128, 128, 128, 0.1)',
                tickformat='%d/%m/%Y'
            ),
            yaxis=dict(
                title="Solde (€)",
                ticksuffix="€",
                zeroline=False
            ),
            showlegend=False
        )

    elif chart_type == 'pie':
        # Filtrer uniquement les dépenses pour le camembert
        expenses_df = df[df['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()  # Convertir en positif pour l'affichage
        summary = expenses_df.groupby('category')['amount'].sum().reset_index()
        total_expenses = summary['amount'].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=summary['category'],
            values=summary['amount'],
            hole=0.4,
            textinfo='percent',
            textfont_size=12,
            marker=dict(
                colors=px.colors.qualitative.Set3,
                line=dict(color='white', width=2)
            ),
            hovertemplate="<b>%{label}</b><br>" +
                         "Montant: %{value:.2f}€<br>" +
                         "Pourcentage: %{percent}<extra></extra>"
        )])
        
        fig.update_layout(
            title={
                'text': 'Répartition des dépenses par catégorie',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            annotations=[dict(
                text=f'Total:<br>{total_expenses:.2f}€',
                x=0.5,
                y=0.5,
                font_size=14,
                showarrow=False
            )]
        )

    else:  # bar par défaut
        # On utilise le graphique en ligne comme défaut
        return generate_expense_chart('line')

    # Configuration commune pour tous les graphiques
    fig.update_layout(
        font_family="Roboto",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.02)',
        hovermode='x unified',
        margin=dict(t=100, l=50, r=50, b=50),
        height=500,
        template='plotly_white'
    )

    # Amélioration des axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.1)',
        showline=True,
        linewidth=1,
        linecolor='rgba(128, 128, 128, 0.2)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.1)',
        showline=True,
        linewidth=1,
        linecolor='rgba(128, 128, 128, 0.2)',
        ticksuffix="€"
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d']
        }
    )