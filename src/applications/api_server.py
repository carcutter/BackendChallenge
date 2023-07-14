import click
from flask import Flask, jsonify
from flask_cors import CORS
from flask_json_schema import JsonValidationError


from core.challenge_api import api as backend_challenge_api
from utils.schema import schema


def get_app():
    app = Flask("Backend Challenge API")
    schema.init_app(app)
    CORS(app)
    app.register_blueprint(backend_challenge_api, url_prefix="/backend")

    @app.errorhandler(JsonValidationError)
    def validation_error(e):
        return jsonify({"error": e.message, "errors": [validation_error.message for validation_error in e.errors]}), 400

    return app


@click.group(name="api-server")
def cli():
    pass


# noinspection HttpUrlsUsage
@cli.command(name="vehicle-features", help="Generate comparison images.")
@click.option(
    "--host",
    "host",
    help="The hostname to listen on.",
    default="127.0.0.1",
    type=str,
)
@click.option(
    "--port",
    "port",
    help="The port of the webserver.",
    default=8080,
    type=int,
)
def vehicle_features(host: str, port: int):
    """
    Serves an API with `Flask`.
    http://<host>:<port>/backend/

    Args:
        host: The hostname to listen on.
        port: The port of the webserver.
    """
    app = get_app()
    app.run(host=host, port=port, debug=True)
