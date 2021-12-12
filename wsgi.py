from app.main import app
 
if __name__ == "__main__":
    # "debug=True" refreshes app every time a change is made, but Debugging is only possible for "debug=False"
    app.run(debug=True, port=5000)