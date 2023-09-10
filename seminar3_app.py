from flask import Flask, render_template, request, flash, redirect, url_for
import os
from config import Config
from hw_3.models import db, User2
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, Registration2Form, Registration3Form

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)

category = [
    {"title": 'Home page', "func_name": 'index'},
    {"title": 'Registration 3', "func_name": 'registration3'}
]


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', category=category)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/registration3/', methods=['GET', 'POST'])
def registration3():
    form = Registration3Form()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        name = form.name.data.lower()
        surname = form.surname.data.lower()
        email = form.email.data
        user = User2(name=name, surname=surname, email=email)
        if User2.query.filter(User2.email == email).first():
            flash(f'Пользователь с e-mail {email} уже существует')
            return redirect(url_for('registration'))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Вы успешно зарегистрировались!')
        return redirect(url_for('registration3'))
    return render_template('registration3.html', form=form)


if __name__ == '__main__':
    app.run()
