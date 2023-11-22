from wtforms import Form, StringField, EmailField, PasswordField, validators

class UserCreateValidator(Form):
  name = StringField('Name', [
    validators.DataRequired(),
    validators.Length(min=3, max=64),
  ])
  email = EmailField('Email', [
    validators.Length(max=64),
    validators.Email(),
  ])
  password = PasswordField('Password', [
    validators.Length(min=6, max=32)
  ])
  confirm_password = PasswordField('Confirm your password', [
    validators.EqualTo('password'),
  ])