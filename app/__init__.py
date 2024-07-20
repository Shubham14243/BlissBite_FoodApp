from flask import Flask
from . import routes

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = "enaef"
app.register_blueprint(routes.routes)
