from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import db, Transaction
from .forms import TransactionForm
from .utils import generate_expense_chart

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    chart = generate_expense_chart()
    total_income = sum(t.amount for t in transactions if t.type == 'revenu')
    total_expenses = sum(t.amount for t in transactions if t.type == 'dépense')
    balance = total_income - total_expenses
    return render_template('index.html', 
                         transactions=transactions,
                         chart=chart,
                         balance=balance)

@bp.route('/add', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        try:
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
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de l\'ajout de la transaction.', 'error')
    return render_template('add_transaction.html', form=form)

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500