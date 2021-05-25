@app.route('/setupdatelimit',methods=["POST","GET"])
def setupdate():
    if 'user_id' in session:
        name= session['name']
        id=session["user_id"]
        
        email = session['email']
        if request.method == "POST":
            mon=request.form.get('month')
            month = mon+"-01"
            value=request.form.get('value')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM mlimit WHERE month = % s AND id = % s" ,(month,id))
            account = cursor.fetchone()
            if(account):
                cursor.execute("UPDATE mlimit SET value = % s WHERE month = % s",(value,month,))
                msg="Successful...!"
                cursor.connection.commit()
                return render_template("updatelimit.html",id=id,email=email,name=name,msg=msg,indicator="success",title="Update monthly limit")    
            else:
                msg="Please set limit before update"
                return render_template("updatelimit.html",id=id,email=email,name=name,msg=msg,indicator="failure",title="Update monthly limit")    
    else:
        return redirect('/') 
@app.route('/setlimit',methods=["POST","GET"])
def setlimit():
    if 'user_id' in session:
        email= session['email']
        id = session['user_id']
        
        
        msg=""
        count = 0
        alert=""
        
        if request.method=="POST":
            mon=request.form.get('month')
            month = mon+"-01"
            value=request.form.get('value')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM mlimit WHERE month = % s AND id = % s",(month,id))
            found = cursor.fetchone()
            print(found)
            if(found):
                msg="You've already set limit for the month"
                count = 1
            
            else:
                cursor.execute("INSERT INTO mlimit VALUES(NULL,% s,% s,% s)",(id,month,value,))
                msg="Successful...!"
                cursor.connection.commit()
            if(count==1):
                alert='failure'
            else:
                alert='success'
        
            return render_template("setlimit.html",msg=msg,indicator=alert,title="Set monthly limit")
        
    else:
        return redirect('/')    
if  account:
            msg="Account already exists !"
            return render_template("register.html", msg = msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg="Invalid email address !"
            return render_template("register.html", msg = msg)
        elif not  re.match(r'[A-Za-z0-9]+', email):        
            msg="name must contain only characters and numbers !"
            return render_template("register.html", msg = msg)
        elif not  name=="" or email == "" or p1 == ""or p2 == "":
            msg="please fill the form"
            return render_template("register.html", msg = msg)
        else:
            cursor.execute("INSERT INTO users VALUES (NULL, % s, % s, % s, % s)", (name,email, p1, p2, ))
            mysql.connection.commit()
            msg = "You have successfully registered !"
            return render_template("register.html", msg = msg) <!-- ======= Footer ======= -->
  <footer id="footer">

    <div class="footer-top">
      <div class="container">
        <div class="row">

          <div class="col-lg-3 col-md-6 footer-contact">
            <h3>Budgets on Fire</h3>

          </div>




    <div class="container d-md-flex py-4">

      <div class="mr-md-auto text-center text-md-left">
        <div class="copyright">
          &copy; Copyright <strong><span>Flattern</span></strong>. All Rights Reserved
        </div>
        <div class="credits">
          <!-- All the links in the footer should remain intact. -->
          <!-- You can delete the links only if you purchased the pro version. -->
          <!-- Licensing information: https://bootstrapmade.com/license/ -->
          <!-- Purchase the pro version with working PHP/AJAX contact form: https://bootstrapmade.com/flattern-multipurpose-bootstrap-template/ -->
          Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>
        </div>
      </div>
 
    </div>
  </footer><!-- End Footer -->

  <a href="#" class="back-to-top"><i class="icofont-simple-up"></i></a>
import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors

from helpers import apology, login_required, usd

app = Flask(__name__)
Session(app)
app.secret_key = 'a'

#app.config["TEMPLATES_AUTO_RELOAD"] = True

def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = 'eC2olOGFWo'
app.config['MYSQL_PASSWORD'] = 'sYjr7xrGdX'
app.config['MYSQL_DB'] = 'eC2olOGFWo'
mysql = MySQL(app)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

#db = SQL("sqlite:///budget.db")

#app.jinja_env.filters["usd"] = usd

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        user = request.form.get("username")
        password = request.form.get("password")
        cursor = mysql.connection.cursor()
        if user == "" or password == "":
            return apology("Must enter username and password")
        rows = cursor.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
        
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        username = request.form.get("username")
        p1 = request.form.get("password")
        p2 = request.form.get("password2")
        cursor = mysql.connection.cursor()
        if p1 != p2:
            return apology("Passwords don't match")
        rows = cursor.execute("SELECT * FROM users WHERE username = % s", (username,))
        #if len(rows) == 1:
           # return apology("Username taken")
        cursor.execute("INSERT INTO users VALUES (NULL, % s, % s, % s, % s)", (name, username, p1, p2, ))
        rows = cursor.execute("SELECT * FROM users WHERE username = % s)",( username,))
        session["user_id"] = rows[0]["id"]
        return redirect("/")
        
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    cursor = mysql.connection.cursor()
    username = cursor.execute("SELECT username FROM users WHERE id = :id", id = session["user_id"])[0]["username"]
    name = cursor.execute("SELECT name FROM users WHERE id = :id", id = session["user_id"])[0]["name"]
    if request.method == "GET":
        return render_template("account.html", username=username, name=name)
    if request.method == "POST":
        if request.form.get("name") != "":
            cursor.execute("UPDATE users SET name=:name WHERE id=:id", name=request.form.get("name"), id=session["user_id"])
        if request.form.get("password") != "" and request.form.get("password") == request.form.get("password2"):
            cursor.execute("UPDATE users SET hash=:newpass WHERE id=:id", newpass=generate_password_hash(request.form.get("password")), id=session["user_id"])
    return redirect("/account")
    

@app.route("/money", methods=["GET", "POST"])
@login_required
def money():
    cursor = mysql.connection.cursor()
    name = cursor.execute("SELECT name FROM users WHERE id = :id", id = session["user_id"])[0]["name"]
    balance = cursor.execute("SELECT balance FROM users WHERE id = :id", id = session["user_id"])[0]["balance"]
    date = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}"
    categories = cursor.execute("SELECT DISTINCT category FROM transactions WHERE id=:id AND amount < 0", id=session["user_id"])
    data = cursor.execute("SELECT category, amount FROM transactions WHERE id=:id AND amount < 0", id=session["user_id"])
    counts = {}
    for x in categories:
        for y in data:
            if x["category"] == y["category"]:
                if x["category"] not in counts:
                    counts[x["category"]] = [-y["amount"]]
                else:
                    counts[x["category"]][0] = round(counts[x["category"]][0] - y["amount"], 2)
    totalExpense = 0
    for item in counts:
        totalExpense += counts[item][0]
    for item in counts:
        counts[item].append(round(100 * (counts[item][0] / totalExpense), 1))
    rows = cursor.execute("SELECT * FROM transactions WHERE id=:id", id=session["user_id"])
    if request.method == "GET":
        return render_template("money.html", name=name, date=date, balance=usd(balance), rows=rows, counts=counts)
        
@app.route("/transact", methods=["GET", "POST"])
@login_required
def transact():
    cursor = mysql.connection.cursor()
    categories = cursor.execute("SELECT DISTINCT category FROM transactions WHERE id=:id", id=session["user_id"])
    if request.method == "GET":
        return render_template("transact.html", categories=categories)
    else:
        transact = request.form.get("type")
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        item = request.form.get("item")
        priorBalance = cursor.execute("SELECT balance FROM users WHERE id=:id", id=session["user_id"])[0]["balance"]
        if transact == "expense":
            amount = -amount
        newBalance = priorBalance + amount
        cursor.execute("INSERT INTO transactions (id, amount, item, category, time) VALUES (:id, :amount, :item, :category, :time)", id=session["user_id"], amount=amount, item=item, category=category, time=datetime.now())
        cursor.execute("UPDATE users SET balance=:balance WHERE id=:id", balance=newBalance, id=session["user_id"])
        return redirect("/money")
        
@app.route("/faq")
@login_required
def faq():
    return render_template("faq.html")
   
if __name__ == '__main__':
   app.run(debug = True)