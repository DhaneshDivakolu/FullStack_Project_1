from flask import Flask,render_template,request
from pymongo import MongoClient

app = Flask(__name__)
myclient = MongoClient("localhost", 27017)
mydb = myclient["Calci"]
results = mydb["results"]

@app.route("/", methods=["GET" , "POST"])
def frontend():
    if request.method == "POST":
       n1 = int(request.form["inp1"])
       opr = request.form["opr"]
       n2 = int(request.form["inp2"])
       if opr=="add":
           res = f"{n1} + {n2} is {n1+n2}"
           results.insert_one({
                "number1":n1, "number2":n2, "operator":opr, "output":res
            })
           return render_template("index.html" , output = res)
       if opr=="sub":
           res = f"{n1} - {n2} is {n1-n2}"
           results.insert_one({
                "number1":n1, "number2":n2, "operator":opr, "output":res
            })
           return render_template("index.html" , output = res)
       if opr=="mul":
           res = f"{n1} x {n2} is {n1*n2}"
           results.insert_one({
                "number1":n1, "number2":n2, "operator":opr, "output":res
            })
           return render_template("index.html" , output = res)
       if opr=="div":
           try:
                res = f"{n1} / {n2} is {n1/n2}"
                results.insert_one({
                "number1":n1, "number2":n2, "operator":opr, "output":res
            })
                return render_template("index.html" , output = res)
           except ZeroDivisionError as e:
               res = "Please change num2 as Non-Zero"
               return render_template("index.html" , output = res)
    else: 
        return render_template("index.html")

app.run(debug=True)