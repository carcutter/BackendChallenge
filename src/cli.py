import click
from dotenv import load_dotenv

from applications.api_server import cli as api_server


DOTENV_PATH = "./.env.cli"  # use path from root folder


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


if __name__ == "__main__":
    # load and parse the .env.cli file to environment variables
    load_dotenv(dotenv_path=DOTENV_PATH)

    # noinspection PyTypeChecker
    cli.add_command(api_server)
    cli()
