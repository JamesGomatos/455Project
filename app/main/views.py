from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .. import db


@main.route('/')
def index():
    return render_template('index.html')
