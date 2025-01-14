from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, NumberRange

class TransactionForm(FlaskForm):
    type = SelectField('Type', choices=[('revenu', 'Revenu'), ('dépense', 'Dépense')], 
                      validators=[DataRequired()])
    amount = FloatField('Montant', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Catégorie', choices=[
        ('salaire', 'Salaire'),
        ('alimentation', 'Alimentation'),
        ('transport', 'Transport'),
        ('loisirs', 'Loisirs'),
        ('factures', 'Factures'),
        ('autres', 'Autres')
    ])
    description = TextAreaField('Description')
    date = DateField('Date', validators=[DataRequired()])