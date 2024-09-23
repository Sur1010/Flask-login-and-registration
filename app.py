from flask import Flask
from flask_mail import Mail
from models.user import db
import secrets
from flask_migrate import Migrate
from controllers.auth import auth_bp

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sur1234@localhost/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
