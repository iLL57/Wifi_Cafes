from random import random, randint

from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import func, select
import os
from forms import AddCafeForm
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application")

Bootstrap(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jaredward/PycharmProjects/internetCafes/instance/cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Configure Table
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


# Home route to display cafes
@app.route("/")
def home():
    newest_cafes = Cafe.query.order_by(Cafe.id.desc()).limit(4).all()
    cafe_locations = Cafe.query.order_by(Cafe.location).distinct()
    colors = ['#11dbcf', '#5578ff', '#e80368', '#e361ff', '#47aeff', '#ffa76e', '#4233ff', '#b2904f', '#b20969',
              '#ff5828', '#29cc61']
    return render_template("index_copy.html", cafes=newest_cafes, locations=cafe_locations, colors=colors)


@app.route("/location/<string:location>")
def cafe_by_location(location):
    selected_location = Cafe.query.filter_by(location=location).all()
    cafe_count = len(selected_location)
    return render_template('location.html', cafes=selected_location, location=location, cafe_count=cafe_count)


@app.route("/random")
def get_random_cafe():
    random_cafe = Cafe.query.order_by(func.random()).first()
    return render_template('random.html', cafe=random_cafe)


@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    cafe_form = AddCafeForm()
    if cafe_form.validate_on_submit():
        cafe_name = cafe_form.name.data
        cafe_location = cafe_form.location.data
        existing_cafe = db.session.execute(db.Select(Cafe).where(Cafe.name == cafe_name, Cafe.location == cafe_location)
                                           ).scalar()
        if existing_cafe:
            flash('This café already exists', 'warning')
            return redirect(url_for('add_cafe'))
        new_cafe = Cafe(
            name=cafe_name,
            map_url=cafe_form.map_url.data,
            img_url=cafe_form.img_url.data,
            location=cafe_location,
            has_sockets=cafe_form.has_sockets.data,
            has_toilet=cafe_form.has_toilet.data,
            has_wifi=cafe_form.has_wifi.data,
            can_take_calls=cafe_form.can_take_calls.data,
            seats=cafe_form.seats.data,
            coffee_price=cafe_form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()

        added_cafe = db.session.execute(db.Select(Cafe).where(cafe_location == Cafe.location)).scalar()
        return redirect(url_for('location', location=added_cafe.location))
    return render_template('add_cafe.html', cafe_form=cafe_form)


if __name__ == '__main__':
    app.run(debug=True, port=5010)
