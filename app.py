from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# tworze aplikację flask odnoszącą się do nazwy projektu
app=Flask(__name__)
# lokalizacja i inicjalizacja bazy danych, /// relative path
app.config['SQLAlchemy_DATABASE_URI'] = "sqlite:///biuropodrozy.db"
db=SQLAlchemy(app)
db.init_app(app)


@app.route('/', methods=['POST, GET'])
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(port=5000, debug=True)

