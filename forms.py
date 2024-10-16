from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField
from wtforms.validators import DataRequired, URL


class AddCafeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    map_url = URLField('Map URL', validators=[DataRequired(), URL()])
    img_url = URLField('Image URL', validators=[URL()])
    has_sockets = BooleanField('Does the café have power outlets?', validators=[DataRequired()])
    has_toilet = BooleanField('Does café have restrooms for use?', validators=[DataRequired()])
    has_wifi = BooleanField('Does café have Wi-fi to use?', validators=[DataRequired()])
    can_take_calls = BooleanField('Good setting for phone calls?', validators=[DataRequired()])
    seats = StringField('How many seats are in the café?', validators=[DataRequired()])
    coffee_price = StringField('What is the average price for coffee here?', validators=[DataRequired()])
    submit = SubmitField('Submit Café')



