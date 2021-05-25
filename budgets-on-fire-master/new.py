

from flask import Flask,  redirect, render_template, request, session


from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re,datetime
from sendemail import sendgrid,forgotemail

from helpers import  login_required, usd

app = Flask(__name__)


app.secret_key = 'z'


app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = 'kUzHWiyOub'
app.config['MYSQL_PASSWORD'] = 'uljJV6Csxn'
app.config['MYSQL_DB'] = 'kUzHWiyOub'
mysql = MySQL(app)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")

   
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        p1 = request.form['password']
        p2= request.form['password2']
        

        cursor = mysql.connection.cursor()
        if p1 != p2:
            msg="Passwords don't match"
            return render_template("register.html", msg = msg)
        cursor.execute('SELECT * FROM users WHERE email = % s', (email, ))
        account = cursor.fetchone()
        print(account)
        
        if  account:
            msg="Account already exists !"
            return render_template("register.html", msg = msg)
        elif   name=="" or email == "" or p1 == ""or p2 == "":
            msg="please fill the form"
            return render_template("register.html", msg = msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg="Invalid email address !"
            return render_template("register.html", msg = msg)
       
        elif not  re.match(r'[A-Za-z0-9]+', email):        
            msg="name must contain only characters and numbers !"
            return render_template("register.html", msg = msg)
        #elif   name=="" or email == "" or p1 == ""or p2 == "":
         #   msg="please fill the form"
          #  return render_template("register.html", msg = msg)
        else:
            cursor.execute("INSERT INTO users VALUES (NULL, % s, % s, % s, % s)", (name,email, p1, p2, ))
            mysql.connection.commit()
            msg = "You have successfully registered !"
            return render_template("register.html", msg = msg)
        
        

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if email == "" or password == "":
            msg="Must enter email and password"
            return render_template("login.html", msg = msg)
        
       
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['logged_in'] = True
            session['user_id'] = account[0]
            session['name'] = account[1]
            session['email'] = account[2]
           
            
            user_id = account[0]
            name= account[1]
            email=account[2]
            mysql.connection.commit()
            msg = "Logged in successfully !"
            return render_template("index.html", msg = msg)
        
        else:
            msg="incorrect email and password"
            return render_template("login.html", msg = msg)
            
    
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():      
    msg = ''
    if 'user_id' in session:
        id = session['user_id']
        
        email = session['email']
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            password2 = request.form.get("password2")
            cursor = mysql.connection.cursor()
            if email == "" or password == "" :
                msg="Must enter email and password"
                return render_template("account.html",msg = msg)
            if password != password2:
                msg="Passwords don't match"
                return render_template("account.html",msg = msg)
            cursor.execute('SELECT * FROM users WHERE email = % s AND user_id=% s', (email,id ))
            v = cursor.fetchone()
            print(v)
            if not v:
             msg= "Account not already exists !"
             return render_template("account.html",msg=msg)
        
           
           
            cursor.execute('UPDATE users SET  password =% s WHERE email =% s ',( password, email),)
            cursor.execute('UPDATE users SET  password2 =% s WHERE email =% s ',( password2, email),)
            mysql.connection.commit()
            msg = "You have successfully updated !"
            return render_template("account.html",msg=msg)
        elif request.method == 'GET':
            msg = "Please fill out the form !"
            return render_template("account.html", msg = msg)
        return redirect('/')

@app.route('/monthlylimit')
def monlimit():
    if 'user_id' in session:
        id = session['user_id']
        
        email = session['email']
    
        return render_template("setlimit.html")
    return redirect('/')
@app.route('/updatelimit')
def updatelimit():
    if 'user_id' in session:
        id = session['user_id']
        name= session['name']
        email = session['email']
        return render_template("updatelimit.html")
    return redirect('/')
    

@app.route('/setlimit',methods=["POST","GET"])
def setlimit():
    if 'user_id' in session:
        email= session['email']
        id=session['user_id']
        
        
        msg=""
        count = 0
        alert=""
        
        if request.method=="POST":
            mon=request.form.get('month')
            month = mon+"-01"
            value=request.form.get('value')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM mlimit WHERE month = % s AND id= % s  ",(month,id))
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
@app.route('/setupdatelimit',methods=["POST","GET"])
def setupdate():
    if 'user_id' in session:
        name= session['name']
        id=session['user_id']
        email = session['email']
        if request.method == "POST":
            mon=request.form.get('month')
            month = mon+"-01"
            value=request.form.get('value')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM mlimit WHERE month = % s",(month,))
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
@app.route('/budget')
def budget():
   if 'user_id' in session:
        id=session["user_id"]
       
        email = session['email']
        
       
        return render_template("addbudget.html")
   return redirect("/")

    

@app.route('/addbudget',methods=["POST","GET"])
def addbudget():
    if 'user_id' in session:
        name=session["name"]
        id=session["user_id"]
        
       
       
        email= session['email']
        
        
        count = 0
        c=0
        sum=0
        dt = datetime.datetime.now()
        mn = { '01':"January",
                '02':"February",
                '03':"March",
                '04':"April",
                '05':"May",
                '06':"June",
                '07':"July",
                '08':"August",
                '09':"September",
                '10':"October",
                '11':"November",
                '12':"December"}
        if request.method=="POST":
            date = request.form.get('date')+""
            da = date.split("-")
            daa = da[0]+"-"+da[1]+"%"
            op = request.form.get('select')+""
            des = request.form.get('dincome')
            value = request.form.get('income')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM mlimit WHERE id = % s and month LIKE % s",(id,daa,))
            dat = cursor.fetchone()
            if(dat):
                mlimit = dat[3]
                if(op=='+'):
                    cursor.execute("INSERT INTO income VALUES(NULL,% s,% s,% s,% s,% s)",(id,date,des,value,dt))
                    count = 1
                    cursor.connection.commit()
                elif(op=='-'):
                    cursor.execute("INSERT INTO expense VALUES(NULL,% s,% s,% s,% s,% s)",(id,date,des,value,dt))
                    cursor.connection.commit()                
                cursor.execute("SELECT * FROM income WHERE date = % s AND id = % s",(date,id))
                inc = cursor.fetchall()
                cursor.connection.commit()
                cursor.execute("SELECT * FROM expense WHERE date = % s  AND id = % s",(date,id))
                exp = cursor.fetchall()
                cursor.connection.commit()
                for i in inc:
                    sum = sum+i[4]
                fi = sum
                sum = 0
                for j in exp:
                    sum= sum+j[4]
                ex = sum
                cursor.execute("SELECT * FROM expense WHERE id = % s and date LIKE % s",(id, daa,))
                mexp = cursor.fetchall()
                cursor.connection.commit()
                sum = 0
                for k in mexp:
                    sum = sum+k[4]
                monthexp = sum
                if(monthexp > mlimit):
                     TEXT = """\
                            <!DOCTYPE html>
                            <html>
                            <body>
                                <div class="limit">
                                    <span style="font-size: 48px;left: 20px;font-weight:bold; font-family:Arial, Helvetica, sans-serif; color:#7048a9;">Budget Buddy!</span>
                                    <h3 style="font-size: 24px; font-family:serif">Dear """+ name+""", </h3>
                                    <div class="side" style="position:relative; left:100px;" >
                                        <div class="details"style="position:relative; top:20px; left:60px; font-size:20px; font-family:'Courier New', Courier, monospace;text-align:left; font-weight:bold;">
                                            <p style="color: red;">Your Monthly limit of """+ mn[da[1]] +""" has been Exceeded</p>
                                            <p>Limit  : <span style="color: green;"> %s </span> </p>
                                            <p>Expenses  : <span style="color: red;"> %s</span> </p>
                                            <p style=" color:#7048a9;">Please update your limit accordingly.....</p>
                                        </div>
                                    </div>
                                </div>
                            </body>
                            </html>"""%(mlimit,monthexp)
                          
                     sendgrid(TEXT,email)     
                     c=1
                     cursor.connection.commit()
                if(fi>ex):
                    total = "%.2f"%(fi-ex)
                    total = "+ "+total
                elif(ex>fi):
                    total = "%.2f"%(ex-fi)
                    total = "- "+total
                else:
                    total=0
                if(count==1):
                    return render_template("addbudget.html",month=mn[da[1]],year=da[0],day=da[2],fincome=fi,fexpense=ex,incomes=inc,expenses=exp,finalamount=total,title="Add Budget")
                elif(count==0 and c==0):
                    return render_template("addbudget.html",month=mn[da[1]],year=da[0],day=da[2],fexpense=ex,fincome=fi,incomes=inc,expenses=exp,finalamount=total,title="Add Budget")
                else:
                    return render_template("addbudget.html",month=mn[da[1]],year=da[0],day=da[2],fexpense=ex,fincome=fi,incomes=inc,expenses=exp,finalamount=total,title="Add Budget")
            else:
                return render_template("addbudget.html",month=mn[da[1]],year=da[0],day=da[2],notice="You've not set monthly limit",title="Add Budget")

    else:
        return redirect('/')  
@app.route('/mbudget')
def mbudget():
    if 'user_id' in session:
        id=session["user_id"]
        
        email = session['email']
        return render_template("budgethistory.html")
    else:
        return redirect('/')    

@app.route('/history', methods=["POST","GET"])
def history():
    if 'user_id' in session:
        name= session['name']
        email= session['email']
        
        userid = session['user_id']
        
        msg=""
        mn = { '01':"January",
                '02':"February",
                '03':"March",
                '04':"April",
                '05':"May",
                '06':"June",
                '07':"July",
                '08':"August",
                '09':"September",
                '10':"October",
                '11':"November",
                '12':"December"}
        if request.method == "POST":
            date=request.form.get('date')+""
            da = date.split('-')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM income WHERE date = % s and id = % s ",(date,userid))
            inc = cursor.fetchall()
            cursor.execute("SELECT * FROM expense WHERE date= % s and id = % s",(date,userid))
            exp = cursor.fetchall()
            cursor.connection.commit()
            if(not(inc) and not(exp)):
                msg="No Items Found...!"
            return render_template("budgethistory.html",userid=userid,name=name,income=inc,expense=exp,day=da[2],month=mn[da[1]],year=da[0],notify=msg,title="Manage Budget")
    else:
        return redirect('/')    
@app.route('/remove/i<no>')
def removei(no):
    if 'user_id' in session:
        name= session['name']
        email= session['email']
        
        userid = session['user_id']
        Tid = int(no)
        cursor= mysql.connection.cursor()
        cursor.execute("DELETE FROM income WHERE Tid = % s",(Tid,))
        cursor.connection.commit()
        notify="Item Removed Successfully..!"
        return redirect("/mbudget")

    
    return redirect('/')    

@app.route('/remove/e<no>')
def removee(no):
    if 'user_id' in session:
        name= session['name']
        
        email = session['user_id']
        Tid = int(no)
        cursor= mysql.connection.cursor()
        cursor.execute("DELETE FROM expense WHERE Tid = % s",(Tid,))
        cursor.connection.commit()
       
        return redirect("/mbudget")
    else:
        return redirect('/')  
    
@app.route('/forgot',methods=["POST","GET"])
def forgot():
    return render_template("forgot.html",title = "Forgot")

@app.route('/forgotpassword',methods=["POST","GET"])
def forgotpassword():
    msg=""
    if request.method=="POST":
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = % s ",(email,))
        account = cursor.fetchone()
        if(account):
            TEXT ="""\
                    <!DOCTYPE html>
                    <html>
                    <body>
                        <div class="containter" style="display: block;">
                            <span style="font-size: 48px;left: 20px;font-weight:bold; font-family:Arial, Helvetica, sans-serif; color:#7048a9;">Budget Buddy!</span>
                            <h3 style="font-size: 24px; font-family:serif"> Dear """+account[1]+""", </h3>
                            <div class="side" style="width: 400px; height: 150px; border: 2px solid #7048a9; padding:30px; border-radius:10px; position:relative; left:100px;" >
                                <div class="details"style="position:relative; top:20px; left:60px; font-size:20px; font-family:'Courier New', Courier, monospace;text-align:left   ;">
                                    <p >email : <span style="color: green; font-weight:bold;">"""+ account[2]+"""</span> </p>
                                    <p>Password : <span style="color: green; font-weight:bold;">"""+account[4]+"""</span> </p>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>"""
            msg="Your login credentials are sent to your registered mail id"
            forgotemail(TEXT,email)
            return render_template("login.html",msg=msg,indicator="success",title = "Forgot")
        else:
            msg="No account found with Email %s"%(email)
            return render_template("forgot.html",msg=msg,indicator="failure",title = "Forgot")
    else:
        return redirect('/forgot')


           
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/") 
      
   
    
     

if(__name__ == '__main__'):
    app.run(host="0.0.0.0",port=8080)
