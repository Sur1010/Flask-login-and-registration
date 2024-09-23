from flask import Flask
from models.user import db
import secrets
from flask_migrate import Migrate
from controllers.auth import auth_bp
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
