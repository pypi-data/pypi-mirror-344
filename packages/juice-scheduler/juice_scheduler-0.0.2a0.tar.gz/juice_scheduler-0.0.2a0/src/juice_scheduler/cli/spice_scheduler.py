import logging
from importlib import resources
from importlib.metadata import version
from pathlib import Path

import click

from juice_scheduler.common.exception import JuiceSchedulerError
from juice_scheduler.model.configuration import Configuration
from juice_scheduler.schedule.spice import SpiceRunner

base_package = __package__.split(".")[0]

@click.command()
@click.version_option(message="%(prog)s - version %(version)s")
@click.option("--template", "-t", is_flag=True,
               help="Get the template configuration file")

@click.option("--configuration", "-c",
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="Configuration json file")
def cli(configuration, template):

    if configuration and template:
        messg = "Don't use -t or -c at the same time"
        raise click.UsageError(messg)

    if not configuration and not template:
        messg = "Use -t or -c options"
        raise click.UsageError(messg)

    if template:
        dump_template()
    else:
        run(configuration)

def dump_template():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    template = resources.files(__package__) / "data" / "template_spice_scheduler.json"
    logging.info(template.read_text())


def run(configuration):
    # Setup of the logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Package: %s Version: %s", base_package, version(base_package))

    try:
        conf = Configuration.from_json_file(configuration)
        runner = SpiceRunner.from_configuration(conf)
        runner.run(conf.get_runner_configuration())
        logging.info("Execution completed")
    except JuiceSchedulerError:
        logging.exception()
        logging.exception("Execution aborted")


if __name__ == "__main__":
    cli()
