from flask import Flask, render_template, request, redirect
import mysql.connector

app=Flask(__name__)

db=mysql.connector.connect(host="localhost",user="root",password="your_password",database="helpdesk")
cur=db.cursor(dictionary=True)

@app.route("/")
def home():
    cur.execute("SELECT * FROM tickets")
    tickets=cur.fetchall()
    return render_template("dashboard.html",tickets=tickets)

@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        data=(request.form["name"],request.form["issue"],request.form["priority"],"Open")
        cur.execute("INSERT INTO tickets(name,issue,priority,status) VALUES(%s,%s,%s,%s)",data)
        db.commit()
        return redirect("/")
    return render_template("raise_ticket.html")

@app.route("/update/<int:id>",methods=["POST"])
def update(id):
    cur.execute("UPDATE tickets SET status=%s WHERE id=%s",(request.form["status"],id))
    db.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
