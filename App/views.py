from App.form import RegistrationForm, LoginForm
from App import app,db
from App.models import User
from urllib.parse import urlsplit
from flask import redirect,render_template, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET','POST'],strict_slashes=False)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations {}, you are now a registered user!'.format(user.username), 'success')
        return redirect(url_for('index'))

    else:
        for error in form.errors.values():
            if error:
                flash(f"something went wrong: {error}",'danger')
    return render_template('register.html', title='Register', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page)[0]!= '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
