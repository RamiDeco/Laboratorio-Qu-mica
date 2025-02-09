from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config
from models import db
from routes import app as routes_app
from routes import routes as routes_blueprint

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(experiment_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)