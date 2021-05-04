from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class CycleConfigForm(FlaskForm):
    frequency = IntegerField("Frequency (per hour)")
    hr = IntegerField("Duration (hr)")
    min = IntegerField("Duration (min)")
    sec = IntegerField("Duration (sec)")
    site_id = IntegerField("Site ID (integer)")

class AddSiteForm(FlaskForm):
    name = StringField()
    latitude = StringField()
    longitude = StringField()
    depth = StringField()


