from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class CycleConfigForm(FlaskForm):
    frequency = IntegerField("Frequency (per hour)", validators=[DataRequired()])

    hr = IntegerField("Duration (hr)", validators=[DataRequired()])
    min = IntegerField("Duration (min)", validators=[DataRequired()])
    sec = IntegerField("Duration (sec)", validators=[DataRequired()])


