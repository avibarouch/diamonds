from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DecimalField, IntegerField
from wtforms.fields import SelectField
from wtforms.validators import ValidationError


class Addnwew_form(FlaskForm):
    carat = DecimalField('Diamond carat',
                         validators=[DataRequired(u"This field"
                                                  " have hige ability to "
                                                  "predict the price, "
                                                  "about 60 percent. so "
                                                  " carat is a mandatory "
                                                  "field")])
    cut = SelectField(u'Diamond cut',
                      validators=[DataRequired(u"Cut has about 30 precent"
                                               "of theability to predict "
                                               "the price. so this is a "
                                               "mandatory field",)],
                      choices=[('Ideal', 'Ideal'), ('Premium',
                               'Premium'), ('Very Good', 'Very Good'),
                               ('Good', 'Good'), ('Fair', 'Fair')])

    color = SelectField(u'Diamond color', choices=[('G', 'G'), ('E', 'E'),
                                                   ('F', 'F'), ('H', 'H'),
                                                   ('D', 'D'),
                                                   ('I', 'I'), ('J', 'J')])
    clarity = SelectField(u'Diamond clarity', choices=[('SI1', 'SI1'),
                          ('VS2', 'VS2'), ('SI2', 'SI2'), ('VS1', 'VS1'),
                          ('WS2', 'WS2'), ('WS1', 'WS1'), ('IF', 'IF'),
                          ('I1', 'I1')])
    depth = DecimalField('Diamond depth')
    table1 = DecimalField('Diamond table')
    x = DecimalField('Diamond x')
    y = DecimalField('Diamond y')
    z = DecimalField('Diamond z')
    price = IntegerField('Diamond price',
                         validators=[DataRequired(u"This  field have "
                                                  "vary importent to "
                                                  "machine lerning, "
                                                  "so price is a "
                                                  "mandatory field")])
    submit = SubmitField('Add This diamond')
