
from flask import Blueprint, render_template, request
import DataUnderstanding as DU

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

	data = DU.get_full_data_for_date(date,location)

	# Renders app/templates/search.html
	return render_template('search.html',results=data)
