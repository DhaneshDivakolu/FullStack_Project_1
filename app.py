from flask import Flask,render_template,request,redirect
from flask_mail import Mail, Message
from pymongo import MongoClient

app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587 
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "Eneter your Mail@gmail.com"
app.config["MAIL_PASSWORD"] = "Enter your app password of your google"
mail = Mail(app)

myclient = MongoClient("localhost", 27017)
mydb = myclient["Calci"]
results = mydb["results"]
credentials = {}
isLoggedIn = False

@app.route("/",methods = ["GET","POST"])
def reg():
    users = {}
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phno = request.form["pno"]
        pwd = request.form["pwd"]

        users["name"]=name
        users["email"]=email
        users["phno"]=phno
        users["pwd"]=pwd
        credentials[email] = users
        return redirect("/")
    else:
        return render_template("reg.html")

@app.route("/a", methods = ["GET","POST"])
def log():
    global isLoggedIn
    if request.method == "POST":
        email=request.form["email"]
        pwd1 = request.form["pwd"]
        for key,val in credentials.items():
            if key == email and val["pwd"]==pwd1:
                isLoggedIn = True
                return redirect("/calci")
        else:
            return redirect("/a")
    else:
        return render_template("reg.html")
@app.route("/calci", methods=["GET" , "POST"])
def cal():
    if isLoggedIn ==True:
        if request.method == "POST":
            n1 = int(request.form["inp1"])
            opr = request.form["opr"]
            n2 = int(request.form["inp2"])
            msg = Message(subject="Calculation",sender="Eneter your Mail@gmail.com", 
                        recipients=["abc@gamil.com","def@gmail.com"])   #one or more reciever mail
            if opr=="add":
                res = f"{n1} + {n2} is {n1+n2}"
                results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                })
                msg.body=res
                mail.send(msg)
                return render_template("index.html" , output = res)
            if opr=="sub":
                res = f"{n1} - {n2} is {n1-n2}"
                results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                })
                msg.body=res
                mail.send(msg)
                return render_template("index.html" , output = res)
            if opr=="mul":
                res = f"{n1} x {n2} is {n1*n2}"
                results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                })
                msg.body=res
                mail.send(msg)
                return render_template("index.html" , output = res)
            if opr=="div":
                try:
                    res = f"{n1} / {n2} is {n1/n2}"
                    results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                    })
                    msg.body=res
                    mail.send(msg)
                    return render_template("index.html" , output = res)
                except ZeroDivisionError as e:
                    res = "Please change num2 as Non-Zero"
                    return render_template("index.html" , output = res)
        else: 
            return render_template("index.html")
    else:
        return redirect("/")

app.run(debug=True)