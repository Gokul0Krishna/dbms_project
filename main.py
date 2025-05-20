from flask import Flask, render_template, request,session, redirect, url_for,flash
from forms import *
import tableaction

table=tableaction.Tableaction()

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

@app.route("/",methods=['GET','POST'])
def home():
    form = Searchbar()
    firstname=table.findname()
    if form.validate_on_submit():
        print('i')
        dt=form.search_query.data
        if dt:
            return redirect(url_for('bookpage', bookname=dt))
        
    return render_template('home.html',form=form,data=firstname)


@app.route("/signup",methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        fname=form.Firstname.data
        lname=form.Lastname.data
        email = form.email.data
        password = form.password.data
        resources={
            "fname":fname,
            "lname":lname,
            "email":email,
            "password":password
        }
        try:
            table.getuid()
        except:
            pass
        table.adddatauser(resources=resources)
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route("/signin",methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        res=table.check(email=email,password=password)
        if res:
            return redirect(url_for('home'))
        else:
            flash('incorrect password or email')        
    return render_template('signin.html', form=form)

@app.route("/<bookname>",methods=['GET', 'POST'])
def bookpage(bookname):
    print(bookname)
    form = Borrow()
    data=table.fetchdata(bookname=bookname)
    name=table.findname()
    try:
        data=list(data)
        name=list(name) 
    except:
        pass
    if data:
        form = Borrow()
        if form.validate_on_submit():
            check=table.Signedin()
            print(check)
            if check:
                table.adddataborrow()
                print(name)
                data[3]=1-int(data[3])
                table.setstatus(data[3])         
                return render_template("book.html",data=data,name=name[0])
            else:
                return redirect(url_for('signin'))
        check=table.Signedin()
        if check:
            return render_template("book.html",data=data,form=form,name=name[0])
        else:
            return render_template("book.html",data=data,form=form) 
    else:
        return render_template('booknotfound.html')
    
@app.route("/<username>",methods=['GET', 'POST'])
def profile(username):
    print(username)
    try:
        res=table.getdataborrow()
        print(res)
    except:
        pass
    return render_template("profile.html")

if __name__ == '__main__':
    app.run(debug=True)