import plotly.express as px
import pandas as pd
from .models import Transaction

def generate_expense_chart():
    transactions = Transaction.query.all()
    if not transactions:
        return None
        
    df = pd.DataFrame([{
        'type': t.type,
        'amount': t.amount,
        'category': t.category,
        'date': t.date
    } for t in transactions])
    
    # Créer un DataFrame séparé pour les dépenses uniquement
    expenses_df = df[df['type'] == 'dépense']
    
    if expenses_df.empty:
        return None
    
    # Grouper par catégorie et sommer uniquement les montants
    summary = expenses_df.groupby('category')['amount'].sum().reset_index()
    
    fig = px.bar(
        summary,
        x='category',
        y='amount',
        title='Dépenses par catégorie',
        labels={'category': 'Catégorie', 'amount': 'Montant (€)'}
    )
    
    # Personnalisation du graphique
    fig.update_layout(
        xaxis_title="Catégorie",
        yaxis_title="Montant total (€)",
        bargap=0.2,
        bargroupgap=0.1
    )
    
    # Formatage des étiquettes de l'axe Y en euros
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Montant: %{y:.2f} €<extra></extra>"
    )
    
    return fig.to_html(full_html=False)