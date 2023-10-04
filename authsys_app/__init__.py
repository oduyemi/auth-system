from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent = False)

db = SQLAlchemy(app)
mail = Mail(app)



from authsys_app import routes