
from flask import Blueprint, render_template, request
import DataUnderstanding as DU
import datetime
import GetData
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

	

	date = date.split("-")
	date = datetime.datetime(year=int(date[0]),month=int(date[1]), day=int(date[2]))


	data = DU.get_full_data_for_date(date,location)
	rain_list, temp_list, humidity_list, wind_list,feel_list = prepare_for_display(data)

	# Renders app/templates/search.html
	return render_template('search.html', rain_results=rain_list, temp_results=temp_list, humid_results=humidity_list, wind_results=wind_list, feel_results=feel_list)


def prepare_for_display(data: dict):
	rain_data = data['Rain']
	temp_data = data['Temperature']
	humidity_data = data['Humidity']
	wind_data = data['Wind']
	feel_data = data['Feel']

	# rain_list = produce_data_lists(rain_data)
	# temp_list = produce_data_lists(temp_data)
	# humitidity_list = produce_data_lists(humidity_data)
	# wind_list = produce_data_lists(wind_data)

	return rain_data, temp_data, humidity_data, wind_data, feel_data


def produce_data_lists(data:dict):
	output_list = []
	for key, value in data.items():
		output_list.append(value)
	return output_list


