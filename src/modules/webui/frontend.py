from flask import Flask
from src.modules.webui.ui.routes import routes

__version__ = (1, 0, 0, "dev")

# Initialize the app
app = Flask(__name__, 
            instance_relative_config=True,
            static_folder="ui/static/",
            static_url_path="",
            template_folder="ui/templates/"
            )

# Register routes
app.register_blueprint(routes)

app.config.from_object('src.modules.webui.config.DevConfiguration')

# Create database
#db = SQLAlchemy(app)

