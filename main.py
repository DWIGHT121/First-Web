from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class Movies(db.Model):
    id = db.column(db.Integer, primary_key = True)
    name = db.column(db.String(30), nullable = False)
    language = db.Column(db.String(30), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

@app.route('/')
def basic():
    return "Hello World"

@app.route('/homepage', methods = ['GET','POST'])
def homepage():
    if request.method == 'POST':
        movie_name = request.form('nameofmovie')
        poster = request.form('poster_link')
        language = request.form('language')
        addedmovie = Movies(name=movie_name, language = language)
        db.session.add(addedmovie)
        db.session.commit()
        return redirect('/homepage')

    else:
        allmovies = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("homepage.html", films=allmovies)

if (__name__) == ("__main__"):
    app.run(debug = True)
