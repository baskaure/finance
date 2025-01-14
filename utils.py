import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .models import Transaction

def generate_expense_chart(chart_type='bar'):
    transactions = Transaction.query.all()
    if not transactions:
        return None
        
    df = pd.DataFrame([{
        'type': t.type,
        'amount': t.amount,
        'category': t.category,
        'date': t.date.strftime('%Y-%m')
    } for t in transactions])
    
    expenses_df = df[df['type'] == 'dépense']
    if expenses_df.empty:
        return None
    
    summary = expenses_df.groupby('category')['amount'].sum().reset_index()
    
    if chart_type == 'pie':
        fig = px.pie(
            summary,
            values='amount',
            names='category',
            title='Répartition des dépenses par catégorie',
            hole=0.3
        )
    elif chart_type == 'line':
        monthly_summary = expenses_df.groupby('date')['amount'].sum().reset_index()
        fig = px.line(
            monthly_summary,
            x='date',
            y='amount',
            title='Évolution des dépenses dans le temps'
        )
    else:  # bar par défaut
        fig = px.bar(
            summary,
            x='category',
            y='amount',
            title='Dépenses par catégorie'
        )
    
    fig.update_layout(
        font_family="Roboto",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=True)