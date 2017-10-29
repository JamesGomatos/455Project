from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User

'''
render the index menu when called.
'''
@main.route('/')
def index():
    return render_template('index.html')

'''
render the worker menu when claled
'''
@main.route('/mechanic')
def mechanic_menu():
    return render_template('mechanic/menu.html')
