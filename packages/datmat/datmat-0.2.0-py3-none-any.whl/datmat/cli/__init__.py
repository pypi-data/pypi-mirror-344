import click


@click.group()
def cli():
    """ Client for datmat."""
    pass


@click.command('helloworld', short_help="Hello world!")
def hello_world() -> None:
    click.echo("Hello world! I am datmat.")


cli.add_command(hello_world, name='helloworld')
