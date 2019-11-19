from wtforms import Form, StringField, validators, PasswordField


class UserForm(Form):
    first_name = StringField('First Name:', validators=[validators.Length(max=100)])
    last_name = StringField('Last Name:', validators=[validators.Length(max=100)])
    email = StringField('Email:', validators=[validators.Length(max=20)])
    password = PasswordField('Password:', validators=[validators.Length(max=20)])
