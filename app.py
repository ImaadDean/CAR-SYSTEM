from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from models import User
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MONGO_URI'] = "mongodb+srv://imaad:Ertdfgxc@cluster0.3fbel.mongodb.net/car_system?retryWrites=true&w=majority&appName=Cluster0"

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": user_id})
    if user_data:
        return User(user_data['_id'], user_data['username'])
    return None

def register_blueprints(app):
    from auth import auth
    from main import main
    from car import car
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(car)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'car.management.system.ug@gmail.com'
app.config['MAIL_PASSWORD'] = 'avbk tris kzri dlht'
app.config['MAIL_DEFAULT_SENDER'] = 'car.management.system.ug@gmail.com'
app.secret_key = 'your_secret_key_here'

mail = Mail(app)

if __name__ == '__main__':
    register_blueprints(app)
    app.run(debug=True, host='0.0.0.0')