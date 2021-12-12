from os import truncate
from src.main import app, port
 
if __name__ == "__main__":
    # "debug=True" refreshes app every time a change is made, but Debugging is only possible for "debug=False"
    app.run(debug = True)