import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .models import Transaction
from datetime import datetime

def generate_expense_chart(chart_type='bar'):
    transactions = Transaction.query.all()
    if not transactions:
        return None
        
    # Create DataFrame
    df = pd.DataFrame([{
        'type': t.type,
        'amount': t.amount if t.type == 'revenu' else -t.amount,
        'category': t.category,
        'date': t.date,
        'month_year': t.date.strftime('%Y-%m')
    } for t in transactions])
    
    df = df.sort_values('date')
    
    if chart_type == 'bar':
        # Grouper par mois et catégorie pour le graphique en barres
        monthly_expenses = df[df['amount'] < 0].groupby(['month_year', 'category'])['amount'].sum().abs().reset_index()
        fig = px.bar(monthly_expenses,
                    x='month_year',
                    y='amount',
                    color='category',
                    title='Dépenses mensuelles par catégorie',
                    labels={'amount': 'Montant (€)', 'month_year': 'Mois', 'category': 'Catégorie'})

    elif chart_type == 'scatter':
        # Graphique de dispersion des dépenses
        expenses_df = df[df['amount'] < 0].copy()
        fig = px.scatter(expenses_df,
                        x='date',
                        y='amount',
                        color='category',
                        size=abs(expenses_df['amount']),
                        title='Distribution des dépenses',
                        labels={'amount': 'Montant (€)', 'date': 'Date', 'category': 'Catégorie'})

    elif chart_type == 'histogram':
        # Histogramme des dépenses
        expenses_df = df[df['amount'] < 0].copy()
        fig = px.histogram(expenses_df,
                          x='amount',
                          nbins=30,
                          color='category',
                          title='Distribution des montants des dépenses',
                          labels={'amount': 'Montant (€)', 'count': 'Nombre de transactions'})

    elif chart_type == 'cumulative':
        # Dépenses cumulées
        df['cumulative'] = df['amount'].cumsum()
        fig = px.line(df,
                     x='date',
                     y='cumulative',
                     title='Évolution des dépenses cumulées',
                     labels={'cumulative': 'Montant cumulé (€)', 'date': 'Date'})

    elif chart_type == 'pie':
        # Keep existing pie chart code
        expenses_df = df[df['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()
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
            hovertemplate="<b>%{label}</b><br>Montant: %{value:.2f}€<br>Pourcentage: %{percent}<extra></extra>"
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

    else:
        # Line chart as default
        return generate_expense_chart('line')

    # Common layout updates
    fig.update_layout(
        font_family="Roboto",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.02)',
        hovermode='x unified',
        margin=dict(t=100, l=50, r=50, b=50),
        height=500,
        template='plotly_white'
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

def plot_expenses_bar(data, date_column, amount_column, category_column):
    """Create a bar chart showing expenses over time"""
    fig = px.bar(data,
                 x=date_column,
                 y=amount_column,
                 color=category_column,
                 title='Dépenses au fil du temps',
                 labels={
                     date_column: 'Date',
                     amount_column: 'Montant (€)',
                     category_column: 'Catégorie'
                 })
    return fig

def plot_cumulative_expenses(data, date_column, amount_column):
    """Create a line chart showing cumulative expenses"""
    cumsum = data.sort_values(date_column)[amount_column].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[date_column],
        y=cumsum,
        mode='lines',
        name='Dépenses cumulées'
    ))
    fig.update_layout(
        title='Évolution des dépenses cumulées',
        xaxis_title='Date',
        yaxis_title='Montant cumulé (€)'
    )
    return fig

def plot_expense_distribution(data, amount_column, category_column):
    """Create a scatter plot of expense distribution"""
    fig = px.scatter(data,
                    x=category_column,
                    y=amount_column,
                    color=category_column,
                    title='Distribution des dépenses par catégorie',
                    labels={
                        amount_column: 'Montant (€)',
                        category_column: 'Catégorie'
                    })
    return fig

def plot_expense_histogram(data, amount_column, bins=30):
    """Create a histogram of expense frequencies"""
    fig = px.histogram(data,
                      x=amount_column,
                      nbins=bins,
                      title='Distribution des montants des dépenses',
                      labels={amount_column: 'Montant (€)'})
    return fig