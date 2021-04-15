from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Likes, Drink
from forms import RegisterForm, LoginForm, SearchName, SearchIng
from requests import get
import json


app = Flask(__name__)

app.config['SQLACHEMY_DATABASE_URI'] = 'postgresql:///drinks'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretdrink"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404

@app.route("/" , methods=["GET", "POST"])
def home_page():
    """Shows homepage with links to site area"""
    a_list = get("https://www.thecocktaildb.com/api/json/v1/1/random.php", "json").json()
    return render_template('home.html', res=a_list)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        
        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.username  # keep logged in
            return redirect("/random")
        else:
            form.username.errors = ["Bad name/password"]
        
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(name, pwd, first_name, last_name, email)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.username

        # on successful login, redirect to secret page
        return redirect("/random")
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("user_id")
    return redirect("/")

@app.route("/favorite")
def send_to_fav():
    """redirects to favorite drinks or to main page to register/login"""
    if 'user_id' in session:
        username1 = session['user_id']
        print("we are in user")
        user = User.query.filter_by(username=username1).first()
        if user:
            user_num = user.id
            return redirect(f"/{user_num}")
        else:
            return redirect("/")
    else:
        print("didnt find user")
        return redirect("/")

@app.route("/<int:user_id>")
def user_profile(user_id):
    """Handles a list of favorite drinks"""
    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    else:
        results = []
        user = User.query.get_or_404(user_id)
        drinks = Drink.query.filter_by(user_id=user_id).all()
        drink = [ dd.serialized() for dd in drinks]
        print(drink)
        for i in range(0, len(drink)):
            results.append(get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink[i]}", 'json').json())
        return render_template('favorite.html', user=user, likes=user.likes, drinks=results)


@app.route("/search")
def create_search_form():

    form_name = SearchName()
    form_ing = SearchIng()
    return render_template('search.html', form_name=form_name, form_ing=form_ing)


@app.route("/search", methods=["POST"])
def search_drink():
    """Retuirn a list of drinks"""
    if request.json["name1"] != "":
        name = request.json["name1"]
        n_list = get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}", 'json').json()
        return (jsonify(n_list), 201)
    else:
        return jsonify(form.errors, 201)
 

@app.route('/drinks/<int:drink_id>')
def list_drink_profile(drink_id):
    """Makes a drink"""
    
    results = get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}", 'json').json()
    if 'user_id' in session:
        username1 = session['user_id']
        print("we are in user")
        user = User.query.filter_by(username=username1).first()
        if user:
            return render_template("drink.html", drink_id=drink_id, results=results, user=user)
        else:
            return render_template("drink.html", drink_id=drink_id, results=results)
    return render_template("drink.html", drink_id=drink_id, results=results)


@app.route("/drinks/<int:drink_id>/like", methods=["POST"])
def add_to_favorite(drink_id):
    """Adds drink to users profile"""
    username1 = session['user_id']
 
    user = User.query.filter_by(username=username1).first()
    if user:
        user_num = user.id
    else:
        print("didnt find user")
    print(user)
   
    new_drink = [Drink(id=drink_id, user_id=user_num)]
    db.session.add_all(new_drink)
    db.session.commit()
    return redirect("/search")


@app.route("/random", methods=["GET","POST"])
def lis_of_drinks():
    """Example hidden page for logged-in users only."""
    a_list = get("https://www.thecocktaildb.com/api/json/v1/1/random.php", 'json').json()
    b_list = get("https://www.thecocktaildb.com/api/json/v1/1/random.php", 'json').json()
    c_list = get("https://www.thecocktaildb.com/api/json/v1/1/random.php", 'json').json()

    if 'user_id' in session:
        username1 = session['user_id']
        user = User.query.filter_by(username=username1).first()
        return render_template("random.html", a_list=a_list, b_list=b_list, c_list=c_list, user=user)
    else:
        return render_template("random.html", a_list=a_list, b_list=b_list, c_list=c_list)

@app.route("/<int:user_id>/<int:drink_id>/delete", methods=["POST"])
def delete_drink(user_id, drink_id):
    """Deletes favorite drink from user profile"""
    new_drink = Drink.query.filter_by(id=drink_id, user_id=user_id).first()
    db.session.delete(new_drink)
    db.session.commit()
    flash(f"Drink has been deteled:{drink_id}")
    return redirect(f"/{user_id}")