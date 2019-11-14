from wtforms import Form, StringField, validators


class UserForm(Form):
    first_name = StringField('First Name:', validators=[validators.Length(max=100)])
    last_name = StringField('Last Name:', validators=[validators.Length(max=100)])
    username = StringField('Username:', validators=[validators.Length(max=20)])
