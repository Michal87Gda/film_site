from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB

class Base(DeclarativeBase):
  pass
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE


class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(250))
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[str] = mapped_column(String(250))
    review: Mapped[str] = mapped_column(String(250))
    img_url: Mapped[str] = mapped_column(String(250))

class Edit(FlaskForm):
    new_rating = FloatField('Your rating out of 10 eg 7.5', validators=[DataRequired(), NumberRange(min=0, max=10)])
    new_review = StringField('Your new review', validators=[DataRequired()])
    submit = SubmitField('Done')

class Add_Movie(FlaskForm):
    new_movie = StringField('Movie title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

#
# with app.app_context():
#     db.create_all()
#
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.add(second_movie)
#     db.session.commit()


@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    all_movies = movies.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
        db.session.commit()
    return render_template("index.html", all_movies=all_movies)

@app.route('/edit', methods=["POST", "GET"])
def edit_rating():
    form = Edit()
    movie_id = request.args.get("movie_id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = form.new_rating.data
        movie.review = form.new_review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('edit.html', form=form, movie=movie)

@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("movie_id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=["POST", "GET"])
def add_movie():
    form = Add_Movie()
    if form.validate_on_submit():
        movie = form.new_movie.data
        url = f"https://api.themoviedb.org/3/search/movie?query={movie}"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4Zjk4MWQ3YThhZjFmYjZlMWI4YjYxMzgzMzE4Yjk3MSIsInN1YiI6IjY1NTUzM2NmOTY1M2Y2MTNmNThhNWYxYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VQuWqWjwGjcV8Ij4UK9sYeTgjW2ShSdpxH__rLUXbSU"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return render_template("select.html", data=data['results'])
    return render_template("add.html", form=form)

@app.route("/select")
def select_movie():
    movie_id = request.args.get("movie_id")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4Zjk4MWQ3YThhZjFmYjZlMWI4YjYxMzgzMzE4Yjk3MSIsInN1YiI6IjY1NTUzM2NmOTY1M2Y2MTNmNThhNWYxYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VQuWqWjwGjcV8Ij4UK9sYeTgjW2ShSdpxH__rLUXbSU"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    new_movie = Movie(
        title = data['original_title'],
        img_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
        year = data['release_date'].split("-")[0],
        description = data['overview'],
        rating = "0",
        ranking = "0",
        review = "0"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("edit_rating", movie_id=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
