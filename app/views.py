
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
	# Renders app/templates/index.html
	return render_template('index.html')
