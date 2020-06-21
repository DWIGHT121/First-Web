from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    language = db.Column(db.String(30), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    link = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return 'Movie No.' + str(self.id)

@app.route('/')
def basic():
    return render_template("homepage.html")

@app.route('/homepage', methods = ['GET','POST'])
def homepage():
    if request.method == 'POST':
        movie_name = request.form('nameofmovie')
        poster = request.form('poster_link')
        language = request.form('language')
        addedmovie = Movies(name=movie_name, language = language, link = poster)
        db.session.add(addedmovie)
        db.session.commit()
        return redirect('/homepage')

    else:
        allmovies = Movies.query.order_by(Movies.date_posted).all()
        return render_template("homepage.html", films=allmovies)

if (__name__) == ("__main__"):
    app.run(debug = True)
