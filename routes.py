from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .models import db, Transaction
from .forms import TransactionForm
from .utils import generate_expense_chart
from datetime import datetime
from sqlalchemy import desc
from functools import wraps

bp = Blueprint('main', __name__)

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'error')
            return redirect(url_for('main.index'))
    return decorated_function

@bp.route('/')
@handle_errors
def index():
    chart_type = request.args.get('chart_type', 'bar')
    transactions = Transaction.query.order_by(desc(Transaction.date)).limit(10).all()
    chart = generate_expense_chart(chart_type)
    total_income = db.session.query(db.func.sum(Transaction.amount)).\
        filter(Transaction.type == 'revenu').scalar() or 0
    total_expenses = db.session.query(db.func.sum(Transaction.amount)).\
        filter(Transaction.type == 'dépense').scalar() or 0
    balance = total_income - total_expenses
    return render_template('index.html', 
                         transactions=transactions,
                         chart=chart,
                         balance=balance,
                         chart_type=chart_type)

@bp.route('/add', methods=['GET', 'POST'])
@handle_errors
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            type=form.type.data,
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction ajoutée avec succès!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_transaction.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@handle_errors
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    form = TransactionForm(obj=transaction)
    
    if form.validate_on_submit():
        transaction.type = form.type.data
        transaction.amount = form.amount.data
        transaction.category = form.category.data
        transaction.description = form.description.data
        transaction.date = form.date.data
        db.session.commit()
        flash('Transaction mise à jour avec succès!', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('edit_transaction.html', form=form, transaction=transaction)

@bp.route('/delete/<int:id>', methods=['POST'])
@handle_errors
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction supprimée avec succès!', 'success')
    return redirect(url_for('main.index'))