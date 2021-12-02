from flask import Flask
from views import views

app = Flask(__name__)
port = 3000

app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    # "debug" refreshes app every time a change is made
    app.run(debug=True, port=port)
