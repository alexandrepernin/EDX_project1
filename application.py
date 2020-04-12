import os
import requests
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Create Flask variable app (for routes definition for instance)
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html", incorrecr=False)


@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method=="GET":
        return "Please submit the form before accessing this page"
    else:
        username = request.form.get("username")
        pwd = request.form.get("password")
        # Make sure the username and password are correct.
        if db.execute("SELECT * FROM users WHERE username = :user AND pwd = :password",{"user": username, "password":pwd}).rowcount == 0:
            return render_template("sign_in.html", incorrect=True)
        else:
            session["Username"] = username
            return render_template("hello_existing_user.html", name=username)

@app.route("/first_visit", methods=["GET", "POST"])
def first_visit():
    if request.method=="GET":
        return "Please submit the form before accessing this page"
    else:
        new_username = request.form.get("username")
        new_pwd = request.form.get("password")
        # Handles case where user sign ups twice
        if db.execute("SELECT * FROM users WHERE username = :user",{"user": new_username}).rowcount > 0:
            return render_template("account_exists.html")
        else:
            db.execute("INSERT INTO users (username, pwd) VALUES (:username, :password)", {"username": new_username, "password": new_pwd})
            db.commit()
            session["Username"] = new_username
            return render_template("welcome_new_user.html", name=new_username)


@app.route("/book_search")
def search():
    return render_template("search.html")

@app.route("/books", methods = ["POST"])
def search_result():
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    isbn = '%'+str(isbn)+'%' if len(isbn)>0 else str(isbn)
    title = '%'+title+'%' if len(title)>0 else title
    author = '%'+author+'%' if len(author)>0 else author
    results = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author",{"isbn": isbn, "title":title, "author":author}).fetchall()
    #print(results)
    return render_template("search_result.html", results=results, len=len(results))


@app.route("/books/<string:isbn>")
def book(isbn):
    isbn=str(isbn)
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "0BnTXldL5qD8QiRIybiNg", "isbns": isbn}).json()
    rating = goodreads["books"][0]["average_rating"]
    ratings_count = goodreads["books"][0]["ratings_count"]
    return render_template("book.html",book=book, reviews=reviews, reviewnb=len(reviews), rating=[rating, ratings_count])

@app.route("/review", methods = ["POST"])
def review():
    review = request.form.get("review")
    grade = request.form.get("grade")
    isbn = request.form.get("isbn")
    user=db.execute("SELECT id FROM users WHERE username = :username", {"username": session["Username"]}).fetchone()

    previous_review = db.execute("SELECT * FROM reviews WHERE user_id = :user AND isbn = :isbn",{"user": user.id, "isbn": isbn}).fetchall()
    if len(previous_review)>0:
        return render_template("review.html", grade=previous_review[0].grade, review=previous_review[0].review, isbn=isbn, username=session["Username"], new=False)
    else:
        db.execute("INSERT INTO reviews (isbn, user_id, review, grade) VALUES (:isbn, :id, :review, :grade)",
                {"isbn": isbn, "id": user.id, "review": review, "grade": grade})
        db.commit()

        return render_template("review.html", grade=grade, review=review, isbn=isbn, username=session["Username"], new=True)
