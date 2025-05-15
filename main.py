from flask import Flask, render_template, request,session, redirect, url_for
from forms import SignupForm,SigninForm
import tableaction

table=tableaction.Tableaction()

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

@app.route("/")
def home():
    return render_template('home.html')

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
            
    return render_template('signin.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)