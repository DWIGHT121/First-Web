from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_BINDS'] = {
    'second': 'sqlite:///demo1.db', 'third': 'sqlite:///demo2.db'}
db = SQLAlchemy(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    language = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return 'Movie No.' + str(self.id)


class User_data(db.Model):
    __bind_key__ = 'second'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return 'User No.' + str(self.id)


@app.route('/')
def basic():
    return render_template("homepage.html")


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        movie_name = request.form['Movie name']
        poster = request.form['Image']
        language = request.form['Language']
        addedmovie = Movies(name=movie_name, language=language, link=poster)
        db.session.add(addedmovie)
        db.session.commit()
        return redirect('/homepage')

    else:
        allmovies = Movies.query.order_by(Movies.date_posted).all()
        # return "{{ Movies.date_posted}}"
        return render_template("homepage.html", films=allmovies)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['f_name']
        lname = request.form['l_name']
        Email = request.form['email']
        Pw = request.form['password']
        info = User_data(f_name=fname, l_name=lname, email=Email, password=Pw)
        db.session.add(info)
        db.session.commit()
        return redirect('/signup')
    else:
        allusers = User_data.query.order_by(User_data.id).all()
        return render_template("signup.html", users=allusers)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        length = len(User_data.query.all())
        for i in range(0, length-1):
            if email == User_data.query.all()[i].email:
                temp_id = i
        if password == User_data.query.all()[temp_id].password:
            name = User_data.query.all(
            )[temp_id].f_name + User_data.query.all()[temp_id].l_name
            return render_template("/logged_homepage.html", name=name)
    else:
        return render_template("login.html")


if (__name__) == ("__main__"):
    app.run(debug=True)
