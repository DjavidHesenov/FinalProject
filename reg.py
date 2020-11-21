from flask import Flask, render_template, url_for, request, redirect, flash, session, logging    
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asdakdmasdamdklasdmlk1e1o3modaslds'
db = SQLAlchemy(app)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/reg', methods=['GET','POST'])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Welcome, {form.username.data}!", 'success')
        return redirect(url_for('greetings'))
    return render_template('reg.html', title='Register', form=form)
    # form = RegisterForm(request.form)
    # if request.method =='POST' and form.validate_on_submit():
    #     name = request.form['name']
    #     surname = request.form['surname']
    #     email = request.form['email']
    #     username = request.form['username']
    #     password = sha256_crypt.encrypt(str(request.form['password']))

    #     return "reg is done"

    #     user = Register(name=name, surname=surname, email=email, password=password, username=username)

    #     try:
    #         db.session.add(user)
    #         db.session.commit()
    #         return redirect('/posts')
    #     except:
    #         return "Error occured"

    # return render_template("reg.html", form=form)
    

@app.route('/')
def greetings():
    return render_template("greet.html")



# class Register(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     surname = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.Text, nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)


# class RegisterForm(Form):
#     name = StringField('Name', [validators.Length(min=1, max=20)])
#     username = StringField('Username', [validators.Length(min=4, max=25)])
#     email = StringField('Email', [validators.Email(), validators.Length(min=6, max=35)])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message="Passwords don't match")
#     ])
#     confirm = PasswordField('Confirm Password')



if __name__ == "__main__":
    app.run(debug=True)

