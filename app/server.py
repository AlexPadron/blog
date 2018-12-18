import click
from flask import Flask

from config import app_config


flask_app = Flask(__name__.split('.')[0])


@flask_app.route('/', methods=['GET'], strict_slashes=False)
def statusz():
    """Get the statusz"""
    return 'Kowalski, status report!<br><br> -> Excellent', 200


@click.group()
def cli():
    """Cli group"""
    pass


@cli.command()
def run():
    """Wrapper to kick off simple server"""
    flask_app.run(
        host=app_config.FLASK_HOST,
        port=app_config.FLASK_PORT,
        debug=app_config.FLASK_DEBUG
    )


if __name__ == '__main__':
    cli()
