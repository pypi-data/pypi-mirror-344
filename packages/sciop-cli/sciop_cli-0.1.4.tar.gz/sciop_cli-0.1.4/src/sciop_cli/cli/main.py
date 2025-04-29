import logging

import click

from sciop_cli.cli.manifest import manifest
from sciop_cli.cli.torrent import torrent


@click.group()
@click.version_option(package_name="sciop_cli")
@click.option(
    "--debug/--no-debug", type=bool, default=False, help="Whether to enable debug logging."
)
def cli(debug: bool) -> None:
    """SciOp, the CLI!!!"""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


cli.add_command(torrent)
cli.add_command(manifest)
