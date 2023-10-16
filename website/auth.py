from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return render_template("home.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if len(password) < 6:
            # error
            pass
        else:
            # add user
            pass

    return render_template("register.html", isTrue=True)

