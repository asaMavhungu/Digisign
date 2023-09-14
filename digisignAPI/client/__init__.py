from api import createApi


def createApp():

	app, _ = createApi(__name__)

	app.static_folder = 'assets'

	from .views import views

	app.register_blueprint(views, url_prefix='/')

	return app