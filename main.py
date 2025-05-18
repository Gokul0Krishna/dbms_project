from flask import Flask, render_template, request,session, redirect, url_for,flash
from forms import SignupForm,SigninForm,Searchbar
import tableaction

table=tableaction.Tableaction()

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

@app.route("/",methods=['GET','POST'])
def home():
    form = Searchbar()
    firstname=table.findname()
    if form.validate_on_submit():
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
        table.adddata(tablename="user",resources=resources)
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
    data=table.fetchdata(bookname=bookname)
    # print(data)
    if data:
        return render_template("book.html") 
    else:
        return render_template('booknotfound.html')

if __name__ == '__main__':
    app.run(debug=True)