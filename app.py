from  flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow) 
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.name}"



#flask --app main.py --debug run
#/env/Scripts/Activate.ps1" -> activate envs

@app.route('/hi')

def index(): 
    return "Hello World"

@app.route('/',methods=['GET','POST'])
def html():
    if request.method=="POST":
        name=(request.form['name'])
        desc=(request.form['desc'])
        Todo=todo(name=name,desc=desc)
        db.session.add(Todo)
        db.session.commit()
    allTodo=todo.query.all()
    return render_template('index.html',allTodo=allTodo)


@app.route('/show')

def taskshow(): 
    allTodo=todo.query.all()
    print(allTodo)
    return "this is all tasks page"


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno): 
    Todo=todo.query.filter_by(sno=sno).first()
    if request.method=="POST":
        name=(request.form['name'])
        desc=(request.form['desc'])
        Todo=todo.query.filter_by(sno=sno).first()
        Todo.name=name
        Todo.desc=desc
        db.session.add(Todo)
        db.session.commit()
        return redirect("/")
        
    
    return render_template('update.html',Todo=Todo)


@app.route('/delete/<int:sno>')
def delete(sno): 
    Todo=todo.query.filter_by(sno=sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")
if __name__ =="__main__ " :
    app.run()    