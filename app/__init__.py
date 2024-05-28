import json
import werkzeug.exceptions
from flask import Flask, Blueprint
from flask_restx import Api
from flask_cors import CORS

from app.config import db_path

from app.db.model import db

from app.rest.time_open import time_open_api


def create_app():
    # Create and configure app.
    app = Flask(__name__, template_folder="visual", static_folder="visual")
    # CORS() add to the app base cors details such as Access-Control-Allow-Origin (base is localhost)
    CORS(app)
    # Path for DB
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(db_path)
    # Needed for correct handling of error with flask_restx
    app.config['ERROR_INCLUDE_MESSAGE'] = False

    db.init_app(app)

    root_bp = Blueprint('root', __name__, url_prefix='/')

    api = Api(
        root_bp,
        title="API code_entretien",
        version="1.0.0",
        description="Documentation api for code_entretien.",
        validate=True
    )

    app.register_blueprint(root_bp)

    api.add_namespace(time_open_api)

    # Use api correct handling of error with flask_restx
    @api.errorhandler(Exception)
    def error_handler(e):
        if isinstance(e, werkzeug.exceptions.HTTPException):
            return e.name, e.code
        else:
            return "Internal Server Error", 500

    @app.after_request
    def after_request(response):
        # Try catch needed for swagger doc
        try:
            data_str = response.data.decode("utf-8")
            data = json.loads(data_str)

            # Necessary to deal with validation errors because there is a bug which skip ERROR_INCLUDE_MESSAGE status
            if response.status_code == 400 and all(key in data for key in ['errors', 'message']):

                data_str = json.dumps('Bad Request')
                response.data = data_str.encode()

        except Exception as e:
            pass

        # use add if not base CORS or set for replacing existing ones
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT, PATCH')
        response.headers.set('Access-Control-Allow-Credentials', 'true')
        response.headers.set('Access-Control-Allow-Headers', 'Accept, Protobuff, Authorization, Content-Type')
        response.headers.set('Access-Control-Expose-Headers', 'Protobuff, Content-Disposition')
        return response

    return app


# You can directly run a flask command from the console on the create_app() but it's simpler that way
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=8000)

    # My apologises I would have set up tests, but I not sure how to make tests with flask-sqlalchemy on functions.
    # I only know how to do so with request using test_client() and I was running out of time
    # Would also have made a docker for easy deployment but I was running out of time
