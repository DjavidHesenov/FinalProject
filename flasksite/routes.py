from flask import render_template, url_for, request, redirect, flash    
from flasksite import app, db, bcrypt
from flasksite.models import User, Post
from flasksite.forms import RegistrationForm, LoginForm, UpdateAccForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('greetings'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('greetings'))
        else:
            flash('Check inputs', 'danger') 
    return render_template('login.html', title='Login', form=form)

@app.route('/reg', methods=['GET','POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('greetings'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-email')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome, {form.username.data}!", 'success')
        return redirect(url_for('login'))
    return render_template('reg.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('greetings'))


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Info has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_img/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@app.route('/')
def greetings():
    return render_template("greet.html")


