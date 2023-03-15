from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField
from wtforms.validators import NumberRange, InputRequired



class AddPropertyForm(FlaskForm):
  title = StringField('Property Title', validators=[InputRequired()])
  description = TextAreaField('Description', validators=[InputRequired()])
  no_rooms = IntegerField('No. of Rooms', validators=[InputRequired(), NumberRange(min=1)])
  no_bathrooms = IntegerField('No. of Bathrooms', validators=[InputRequired(), NumberRange(min=1)])
  price: IntegerField = IntegerField('Price', validators=[InputRequired(), NumberRange(min=1)])
  property_type = SelectField('Property Type', choices=[('house', 'House'), ('apartment', 'Apartment')], validators=[InputRequired()])
  location = StringField('Location', validators=[InputRequired()])
  photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only!')])






