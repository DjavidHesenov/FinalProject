import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, redirect, flash, abort    
from flasksite import app, db, bcrypt
from flasksite.models import User, Post
from flasksite.forms import RegistrationForm, LoginForm, UpdateAccForm, PostForm
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_img', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccForm()
    if form.validate_on_submit():
        if form.picture.data:   
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
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
    posts = Post.query.all() 
    return render_template("greet.html", posts=posts)



@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post is created', 'success')
        return redirect(url_for('greetings'))
    return render_template('create_post.html',
                            form=form, legend='New Post')
    

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post is updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':      
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                            form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post is deleted', 'success')
    return redirect(url_for('greetings'))
