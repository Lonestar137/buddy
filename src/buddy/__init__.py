import click

from buddy.workout.timer import workout

@click.group()
# @click.option('--debug', type=bool, is_flag=True, default=False)
def cli(debug: bool=False):
    # if debug:
    #     click.echo(f"Debug mode is on.")
    pass

cli.add_command(workout)
