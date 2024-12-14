import board
import digitalio
import adafruit_max31865
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
# import RPi.GPIO as GPIO
from time import sleep
import random
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


# If code is stopped during active it will stay active
# This may produce a warning if restarted, this
# line prevents that.
GPIO.setwarnings(False)
# This means we will refer to the GPIO
# by the number after GPIO.
GPIO.setmode(GPIO.BCM)
# This sets up the GPIO 18 pin as an output pin
GPIO.setup(18, GPIO.OUT)

 #Create sensor object, communicating over the board's default SPI bus
 spi = board.SPI()
 cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
 sensor = adafruit_max31865.MAX31865(spi, cs)
 sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=1025, ref_resistor=4301, wires=2)
 bandera = False

# SECCION FLASK QUE PRENDE O APAGA EL CALENTADOR

app = Flask(__name__)
CORS(app)

# # SECCION DE CODIGO QUE DEVUELVE EL VALOR DE TEMPERATURA
 @app.route('/data')
 def obtenerTemperatura():
     temp = 0.13 * sensor.resistance -104.62
     if temp > 46:
        GPIO.output(18, 1) #Apagar rele
        bandera = False
     data = {
         'timestamp': time.time(),
         'value': temp
     }
     return jsonify(data)

@app.route('/rele')
def manejarRele():
    if temp < 30 and not bandera:
        GPIO.output(18, 0)  # Encender el rele
        bandera = True
        data = {
            'value': 1
        }
     return jsonify(data)

# SECCION DE CODIGO ENCARGADA DE LA COMUNICACION ENTRE
# LA RB QUE ES SERVIDOR Y EL USUARIO

@app.route('/grafico')
@login_required
def serve_grafico():
    return render_template('grafico.html')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('serve_grafico'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
