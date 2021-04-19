from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class CycleConfigForm(FlaskForm):
    frequency = IntegerField("Frequency (per sec)", validators=[DataRequired()])
    duration = IntegerField("Duration (min)", validators=[DataRequired()])



