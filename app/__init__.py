
from flask import Flask


def create_app(config: dict | None = None):
	"""Create and configure the Flask application.

	Args:
		config: Optional dict of configuration values to apply to the app.

	Returns:
		The configured Flask app.
	"""
	app = Flask(__name__, template_folder='templates', static_folder='static')

	# apply simple config overrides if provided
	if config:
		app.config.update(config)

	# import and register views
	from .views import bp as main_bp

	app.register_blueprint(main_bp)

	return app
