from flask import Blueprint, request, render_template, abort
from jinja2 import TemplateNotFound

# Blueprint for rendering home page
index_page = Blueprint('index_page', __name__, template_folder='templates')

@index_page.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
