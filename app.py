from flask import Flask
from settings import Settings
from blueprint.login.login import LOGIN
from blueprint.view.view import View

var = Settings()
var.variables()

app = Flask(__name__)
app.register_blueprint(LOGIN, name="/log")
app.register_blueprint(View)

app.secret_key = var.SECRET_KEY


app.register_blueprint(LOGIN)
