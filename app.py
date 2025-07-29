
from flask import Flask 
app = Flask(__name__)
@app.route('/')
def helloworld():
    return 'Hello, Annuaire!'
if __name__ == '__main__':
    app.run(debug=True)  # debug=True permet de voir les erreurs et recharger auto

print("h;das")
