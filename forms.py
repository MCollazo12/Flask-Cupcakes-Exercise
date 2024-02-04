from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, URL, NumberRange


class CupcakeForm(FlaskForm):
    
    flavor = StringField("Flavor", validators=[InputRequired()])
    size = StringField("Size", validators=[InputRequired()])
    rating = FloatField(
        "Rating", validators=[InputRequired(), NumberRange(min=0, max=5)]
    )
    image = StringField("Image URL", validators=[InputRequired(), URL()])
