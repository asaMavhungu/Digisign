from api import createApi

def createApp():

	app, _ = createApi(__name__)

	from .views import views

	app.register_blueprint(views, url_prefix='/')

	return app