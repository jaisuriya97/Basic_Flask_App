from flask import Flask,render_template,redirect,url_for,request,session,flash
import sqlite3
app=Flask(__name__)
app.secret_key="iuwbdcishdb"
con=sqlite3.connect("databas.db")
con.execute("create table if not exists map(name text,mail text,password text)")
con.close()
@app.route('/')
def Home():
    return render_template("Home.html")
@app.route('/singup',methods=["POST","GET"])
def signup():
    if request.method=="POST":
        name=request.form['name']
        mail=request.form['mail']
        password=request.form['password']
        con=sqlite3.connect("databas.db")
        cur=con.cursor()
        cur.execute("insert into map(name,mail,password)values(?,?,?)",(name,mail,password))
        con.commit()
        session["name"]=name
        session["logged_in"]=True
        return redirect(url_for("dashboard"))
        con.close()   
    return render_template("signup.html")
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("databas.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from map where password=? and name=?",(password,name))
        data=cur.fetchone()
        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            session["logged_in"]=True
            return redirect(url_for("dashboard"))
        else:
            flash("You are not Register")
            return render_template("LOGIN.html")
    return render_template("LOGIN.html")
@app.route('/dashboard')
def dashboard():
    if "name" in session:
        return render_template("dashboard.html")
    else:
        return redirect(url_for("signup"))
@app.route('/logout')
def logout():
    session.pop("name",None)
    session.clear()
    return redirect(url_for("Home"))
if __name__=="__main__":
    app.run(debug=True)