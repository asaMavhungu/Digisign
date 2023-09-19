from flask import Flask

def createClient(app: Flask):

	app.static_folder = 'assets'

	from .views import views

	app.register_blueprint(views, url_prefix='/')

	return app