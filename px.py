#!/usr/bin/env python

import logging
import os
import sys
from pathlib import Path
from typing import Literal

import click
from alive_progress import alive_bar

import app
from app.common import has_active_runtime
from registry import register

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('-s', '--scheme', type=str, help='The scheme used by the server.', default='https')
@click.option('-h', '--host', type=str, help='The host of your Panomics server.', default='api-platform.panomics.bio')
@click.option('-p', '--port', type=int, help='The server port.', default=443)
@click.option('-k', '--key', type=str, help='Your api key.', required=True)
def login(scheme, host, port, key):
    app.login(f"{scheme}://{host}:{port}", key)


@cli.command()
@click.option('-o', '--organism', 'organism', type=click.Choice(['human', 'mouse'], case_sensitive=True), required=True,
              help='Organism: one of human or mouse')
@click.option('-t', '--type', 'type_', type=click.Choice(['RNA-seq', 'scRNA-seq'], case_sensitive=True), required=True,
              help='Sample type: one of RNA-seq or scRNA-seq')
@click.option('-gid', '--gene_id_col', type=str, help='The name of the column representing the gene ID.')
@click.option('-gs', '--gene_symbol_col', type=str, help='The name of the column representing the gene symbol.')
@click.option('-rc', '--raw_count_col', type=str, help='The name of the column representing the raw count.')
@click.option('-i', '--input_dir', type=str, help='Absolute path to sample files.', required=True)
@click.option('-d', '--dry_run', is_flag=True, default=False, help='Dry run.')
def upload_samples(organism: Literal['human', 'mouse'], type_: Literal['RNA-seq', 'scRNA-seq'],
                   gene_id_col: str, gene_symbol_col: str, raw_count_col: str, input_dir: str, dry_run: bool):
    """
    All sample files must be .zip or .gz. Example usage:\n
    px upload-samples -o mouse -t RNA-seq -gid gene_id -i /home/user/samples \n
    px upload-samples -o human -t scRNA-seq -i /home/user/samples
    """

    auth_config = app.get_auth()
    ok = has_active_runtime(auth_config)

    if ok:
        files_to_import = []
        for f in os.listdir(input_dir):
            pf = Path(os.path.join(input_dir, f))
            if pf.suffix in ['.zip', '.gz']:
                files_to_import.append(pf)

        click.echo(f'Found {len(files_to_import)} eligible sample files.')
        cont = click.prompt('Do you want to continue? y/n', type=click.Choice(['Y', 'N'], case_sensitive=False),
                            show_choices=False)
        if cont.lower() == 'y':
            failed_files = []
            with alive_bar(len(files_to_import)) as bar:
                for f in files_to_import:
                    try:
                        if not dry_run:
                            app.upload_sample(auth_config, Path(f), organism, type_, gene_id_col, gene_symbol_col,
                                              raw_count_col)
                    except:
                        logging.exception(f'error uploading sample {f}, type {type_}')
                        failed_files.append(f)
                    bar()
            if len(failed_files) > 0:
                click.echo(f"{len(failed_files)} sample files failed to upload")
                for f in failed_files:
                    click.echo(f)
                click.echo(f"Check to logs for more details")
        else:
            sys.exit()
    else:
        click.echo(
            "You don't have an active runtime. Please create one or wait for it to become active before uploading samples.")


def initialize():
    conf_dir = os.path.join(Path.home(), ".panomics")
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
    logging.basicConfig(filename=f"{conf_dir}/log.txt",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.ERROR)


if __name__ == '__main__':
    register()
    initialize()
    cli()
