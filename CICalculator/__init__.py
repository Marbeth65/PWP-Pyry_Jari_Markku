import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SEND_FILE_MAX_AGE_DEFAULT= 0   ## Uutta koodia developpaukseen, mahdollistaa sivun päivittämisen lennosta
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    
    from . import models
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.populate_handle_command)
    app.cli.add_command(models.populate_plans_command)
    app.cli.add_command(models.generate_dummy)
    
    from . import api
    app.register_blueprint(api.api_bp)
    
    @app.route("/gallery")
    def admin_site():
        return app.send_static_file("html/gallery.html")
        
    @app.route("/main/")
    def main_site():
        return app.send_static_file("html/main.html")

    return app