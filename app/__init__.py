from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="../template")
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)
    return app