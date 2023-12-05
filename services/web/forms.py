from flask_security.forms import RegisterForm, LoginForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Regexp


class ValidExpirationDate(object):
    def __call__(self, form, field):
        value = field.data
        if not (len(value) == 5 and value[2] == '/' and value[:2].isdigit() and value[3:].isdigit()):
            raise ValidationError('Invalid expiration date format. Please use mm/yy.')


class CheckoutForm(FlaskForm):
    fname = StringField('First name', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='First name must contain only letters.')
    ])
    lname = StringField('Last name', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='Last name must contain only letters.')
    ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='City must contain only letters.')
    ])
    country = StringField('Country', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='Country must contain only letters.')
    ])
    state = StringField('State', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z]+$', message='State must contain only letters.')
    ])
    zip = StringField('Zip', validators=[
        DataRequired()
    ])

    save_info = BooleanField('Save this information for next time')

    cc_name = StringField('Name on card', validators=[DataRequired()])
    cc_number = StringField('Credit card number', validators=[
        DataRequired(),
        Regexp(r'^\d{16}$', message="Credit card number must be 16 digits.")
    ])
    cc_expiration = StringField('Expiration', validators=[
        DataRequired(),
        ValidExpirationDate()
    ])
    cc_cvv = StringField('CVV', validators=[
        DataRequired(),
        Regexp(r'^\d{3,4}$', message="CVV must be 3 or 4 digits.")
    ])

    submit = SubmitField('Continue to checkout')


class ExtendedRegisterForm(RegisterForm):
    recaptcha = RecaptchaField()


class ExtendedLoginForm(LoginForm):
    recaptcha = RecaptchaField()

