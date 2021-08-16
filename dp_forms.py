from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DecimalField, IntegerField
from wtforms.fields import SelectField
from wtforms.validators import ValidationError


class Addnwew_form(FlaskForm):
    carat = DecimalField(u"Diamonds Carat has about 60 precent of the ability "
                         u"to predict the price. so this is a mandatory field",
                         validators=[DataRequired()])
    cut = SelectField(u"Diamonds Cut has about 30 precent of theability "
                      u"to predict the price. so this is a mandatory field",
                      validators=[DataRequired()],
                      choices=[(u'Ideal', u'Ideal'), (u'Premium',
                               u'Premium'), (u'Very Good', u'Very Good'),
                               (u'Good', u'Good'), (u'Fair', u'Fair')])
    color = SelectField(u'Diamonds Color',
                        choices=[(u'G', u'G'), (u'E', u'E'),
                                 (u'F', u'F'), (u'H', u'H'), (u'D', u'D'),
                                 (u'I', u'I'), (u'J', u'J')])
    clarity = SelectField(u'Diamonds Clarity', choices=[(u'SI1', u'SI1'),
                          (u'VS2', u'VS2'), (u'SI2', u'SI2'), (u'VS1', u'VS1'),
                          (u'WS2', u'WS2'), (u'WS1', u'WS1'),  (u'IF', u'IF'),
                          (u'I1', u'I1')])
    depth = DecimalField(u'Diamonds Depth', validators=[DataRequired(u"If"
                         " a decimal value is unknown pleas insert -1")])
    table1 = DecimalField(u'Diamonds Table', validators=[DataRequired(u"If"
                          " a decimal value is unknown pleas insert -1")])
    x = DecimalField(u'Diamonds X', validators=[DataRequired(u"If a decimal"
                     " value is unknown pleas insert -1")])
    y = DecimalField(u'Diamonds Y', validators=[DataRequired(u"If a decimal "
                     "value is unknown pleas insert -1")])
    z = DecimalField(u'Diamonds Z', validators=[DataRequired(u"If a decimal "
                     "value is unknown pleas insert -1")])
    price = IntegerField(u"Diamonds Price have top importance to this work"
                         u" spacialy and Machine Lerning the main subject "
                         u"so Price also is a mandatory field",
                         validators=[DataRequired()])
    submit = SubmitField(u'Add This diamond')


class Predict_form(FlaskForm):
    carat = DecimalField(u"Diamonds Carat has about 60 precent of the ability "
                         u"to predict the price. so this is a mandatory field",
                         validators=[DataRequired()])
    cut = SelectField(u"Diamonds Cut has about 30 precent of theability "
                      u"to predict the price. so this is a mandatory field",
                      validators=[DataRequired()],
                      choices=[(u'Ideal', u'Ideal'), (u'Premium',
                               u'Premium'), (u'Very Good', u'Very Good'),
                               (u'Good', u'Good'), (u'Fair', u'Fair')])
    color = SelectField(u'Diamonds Color',
                        choices=[(u'G', u'G'), (u'E', u'E'),
                                 (u'F', u'F'), (u'H', u'H'), (u'D', u'D'),
                                 (u'I', u'I'), (u'J', u'J')])
    clarity = SelectField(u'Diamonds Clarity', choices=[(u'SI1', u'SI1'),
                          (u'VS2', u'VS2'), (u'SI2', u'SI2'), (u'VS1', u'VS1'),
                          (u'VVS2', u'VVS2'), (u'VVS1', u'VVS1'),
                          (u'IF', u'IF'), (u'I1', u'I1')])
    depth = DecimalField(u'Diamonds Depth', validators=[DataRequired(u"If"
                         " a decimal value is unknown pleas insert -1")])
    table1 = DecimalField(u'Diamonds Table', validators=[DataRequired(u"If"
                          " a decimal value is unknown pleas insert -1")])
    x = DecimalField(u'Diamonds X', validators=[DataRequired(u"If a decimal"
                     " value is unknown pleas insert -1")])
    y = DecimalField(u'Diamonds Y', validators=[DataRequired(u"If a decimal "
                     "value is unknown pleas insert -1")])
    z = DecimalField(u'Diamonds Z', validators=[DataRequired(u"If a decimal "
                     "value is unknown pleas insert -1")])
    submit = SubmitField(u'Predict The Price For This Diamond')
