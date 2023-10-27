import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Check the portfolio information
    portfolio = db.execute(
        "SELECT * FROM portfolio WHERE user_id = ?", session["user_id"]
    )

    # Bool
    if not portfolio:
        return render_template("blank.html")

    # Define cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    if cash:
        cash = cash[0]['cash']
    else:
        cash = 0

    # Check the current value of the stock!
    symbols = [symbol['stock'] for symbol in portfolio]
    current_value = [lookup(symbol)['price'] for symbol in symbols]

    # Check the total value  of the shares and big total
    total_value = [(share['shares'] * value) for share, value in zip(portfolio, current_value)]
    big_total = sum(total_value) + cash

    # Convert all value to usd(str)
    cash = usd(cash)
    current_value = [usd(value) for value in current_value]
    total_value = [usd(value) for value in total_value]
    big_total = usd(big_total)

    return render_template("index.html", portfolio=portfolio, cash=cash, current_value=current_value, total_value=total_value, big_total=big_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        #Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 403)

        #Ensure stock shares is a positive number
        shares = int(request.form.get("shares"))
        if shares <= 0:
            return apology("must provide a positive number of shares", 403)

        # Check the stock
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("stock symbol doesnt exist", 403)

        # Check the funds
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if not cash or not (quote["price"]*shares) <= cash[0]["cash"]:
            return apology("insufficient funds", 403)

        # Create a new 'history' table for storing transactions information
        db.execute("""CREATE TABLE IF NOT EXISTS history (
                   transaction_id INTEGER PRIMARY KEY,
                   user_id INTEGER,
                   stock TEXT,
                   shares INTEGER,
                   price INTEGER,
                   date DATETIME,
                   action TEXT,
                   FOREIGN KEY (user_id) REFERENCES users(id))""")

        # Update portfolio table
        owned_stocks = db.execute("SELECT stock FROM portfolio WHERE user_id = ?", session["user_id"])
        if not owned_stocks:
                db.execute("INSERT INTO portfolio (user_id, stock, shares, value) VALUES (?, ?, ?, ?)", session["user_id"], quote["name"], shares, quote["price"])
        else:
            stocks = [stock['stock'] for stock in owned_stocks]
            if quote["name"] not in stocks:
                db.execute("INSERT INTO portfolio (user_id, stock, shares, value) VALUES (?, ?, ?, ?)", session["user_id"], quote["name"], shares, quote["price"])
            else:
                db.execute("UPDATE portfolio SET shares = shares + ? WHERE user_id = ? AND stock = ?", shares, session["user_id"], quote["name"])

        # Update history table
        db.execute("INSERT INTO history (user_id, stock, shares, price, date, action) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], quote["name"], shares, (quote["price"] * shares), datetime.now(), 'Buy')

        # Update the users cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (quote["price"] * shares), session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Check the history information
    history = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY date ASC", session["user_id"])

    # Bool
    if not history:
        return render_template("blank.html")

    # Define action (bought/sold) value
    values = [stock['price']/stock['shares'] for stock in history]

    # Convert all value to usd(str)
    values = [usd(value) for value in values]
    prices = [usd(price['price']) for price in history]

    return render_template("history.html", history=history, values=values, prices=prices)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        #Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 403)

        # Check the stock quote using lookup function
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("stock symbol doesnt exist", 403)

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password1"):
            return apology("must provide password", 403)

        # Ensure password was submitted
        if not request.form.get("password2"):
            return apology("must provide password confirmation", 403)

        # Check if the username already taken or not
        username = request.form.get("username")
        usernames = db.execute("SELECT username FROM users")
        if usernames:
            if username in usernames[0]["username"]:
                return apology("username is already taken", 403)

        # Check if the password matched
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if password1 != password2:
            return apology("passwords do not match", 403)

        # Generate password hash
        hash = generate_password_hash(request.form.get("password1"))

        # Store the user data
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 403)

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares amount", 403)

        # Quote the current stock
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("stock didn't exist", 403)

        # Check the owned stock
        owned_stocks = db.execute("SELECT stock FROM portfolio WHERE user_id = ?", session["user_id"])
        if not owned_stocks:
            return apology("you dont have any stocks", 403)
        stocks = [stock['stock'] for stock in owned_stocks]
        if quote["name"] not in stocks:
            return apology("stock not owned", 403)

        # Check if the user inputted the right amount of shares (positive int and not exceeding the amount of owned shares)
        shares = int(request.form.get("shares"))
        before_sell = db.execute("SELECT shares FROM portfolio WHERE user_id = ? AND stock = ?", session["user_id"], quote["name"])
        if shares <= 0 or shares > before_sell[0]["shares"]:
            return apology("must provide the right number/amount", 403)

        # Update portfolio table
        db.execute("UPDATE portfolio SET shares = shares - ? WHERE user_id = ? AND stock = ?", shares, session["user_id"], quote["name"])
        after_sell = db.execute("SELECT shares FROM portfolio WHERE user_id = ? AND stock = ?", session["user_id"], quote["name"])
        if after_sell[0]["shares"] == 0:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND stock = ? AND shares = ?", session["user_id"], quote["name"], 0)

        # Update history table after the sale
        db.execute("INSERT INTO history (user_id, stock, shares, price, date, action) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], quote["name"], shares, (quote["price"] * shares), datetime.now(), 'Sell')

        # Update the users cash after the sale
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (quote["price"] * shares), session["user_id"])

        return redirect("/")

    else:
        return render_template("sell.html")
