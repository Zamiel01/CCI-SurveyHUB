from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login page - coming soon'

@auth.route('/logout')
def logout():
    return 'Logout - coming soon'