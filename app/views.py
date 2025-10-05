
from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
	# Renders app/templates/index.html
	return render_template('index.html')

@bp.route('/search', methods = ['GET', 'POST'])
def search():
	if request.method == 'POST':
		location = request.form['q']
		date = request.form['calendar']
		# Get the search term from the
	else:
		location = request.args.get('q')
		date = request.args.get('calendar')

	# Renders app/templates/search.html
	return render_template('search.html',results=[location,date])
