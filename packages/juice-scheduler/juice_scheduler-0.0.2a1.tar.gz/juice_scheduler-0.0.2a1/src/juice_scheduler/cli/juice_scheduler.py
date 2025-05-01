import logging
from importlib.metadata import version
from pathlib import Path

import click

from juice_scheduler.common.exception import JuiceSchedulerError
from juice_scheduler.model.configuration import Configuration
from juice_scheduler.schedule.basic import Runner

logger = logging.getLogger(__name__)

base_package = __package__.split(".")[0]

@click.command()
@click.version_option(message="%(prog)s - version %(version)s")
@click.option("--configuration", "-c",
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              required=True, help="Configuration json file")
def cli(configuration):
    # Setup of the logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger.info("%s %s", base_package, version(base_package))
    try:
        conf = Configuration.from_json_file(configuration)
        runner = Runner.from_configuration(conf)
        runner.run(conf.get_runner_configuration())
    except JuiceSchedulerError:
        logger.exception()
        logger.exception("Execution aborted")


if __name__ == "__main__":
    cli()
