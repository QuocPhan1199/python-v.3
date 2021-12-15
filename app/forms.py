# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, validators, PasswordField,TextField,validators
# from wtforms.validators import DataRequired
# from app.models import User
# from app.models import LoaiTin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")
class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    confirmpassword = PasswordField("confirmpassword",validators=[DataRequired()])
    submit = SubmitField("Submit")
class LoaiTinForm(FlaskForm):
    tenloai = StringField('Tenloai', validators=[DataRequired()])
    submit = SubmitField('Submit')
class TinForm(FlaskForm):
    loaitin =StringField('Loaitin', validators=[DataRequired()])
    tieude = StringField('Tieude', validators=[DataRequired()])
    tomtat = StringField('Tomtat', validators=[DataRequired()])
    noidung = StringField('Noidung', validators=[DataRequired()])
    images = StringField('Images', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Submit')   