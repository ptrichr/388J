from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError

class SearchForm(FlaskForm):
    search_query = StringField('Enter Movie Name', validators=[InputRequired(), Length(min=1, max=30)])
    submit = SubmitField('Submit')
    
class MovieReviewForm(FlaskForm):
    name = StringField('Username', validators=[InputRequired(), Length(min=1, max=50)])
    text = TextAreaField('Review Contents', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')
    