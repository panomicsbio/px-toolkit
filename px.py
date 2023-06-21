import os
import sys
from pathlib import Path
from typing import Literal

import click

import app
from registry import register

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('-s', '--scheme', type=str, help='The scheme used by the server.', default='https')
@click.option('-h', '--host', type=str, help='The host of your Panomics server.', default='platform.panomics.bio')
@click.option('-p', '--port', type=int, help='The server port.', default=443)
@click.option('-k', '--key', type=str, help='Your api key.', required=True)
def login(scheme, host, port, key):
    app.login(f"{scheme}://{host}:{port}", key)


@cli.command()
@click.option('-t', '--type', 'type_', type=click.Choice(['RNA-seq', 'scRNA-seq'], case_sensitive=True), required=True,
              help='Sample type: one of RNA-seq or scRNA-seq')
@click.option('-f', '--format', 'format_', type=click.Choice(['flat', '2D'], case_sensitive=True),
              help='RNA-seq raw counts file type.')
@click.option('-gid', '--gene_id_col', type=str, help='The name of the column representing the gene ID.')
@click.option('-rc', '--raw_count_col', type=str, help='The name of the column representing the raw count.')
@click.option('-i', '--input_dir', type=str, help='Absolute path to sample files.', required=True)
def import_samples(type_: Literal['RNA-seq', 'scRNA-seq'], format_: Literal['flat', '2D'],
                   gene_id_col: str, raw_count_col: str, input_dir: str):
    """
    All sample files must be .zip or .gz. Example usage:\n
    px import-samples -t RNA-seq -f flat -gid gene_id -rc expected_count -i /home/user/samples \n
    px import-samples -t RNA-seq -f 2D -gid gene_id -i /home/user/samples \n
    px import-samples -t scRNA-seq -i /home/user/samples
    """
    files_to_import = []
    for f in os.listdir(input_dir):
        pf = Path(os.path.join(input_dir, f))
        if pf.suffix in ['.zip', '.gz']:
            files_to_import.append(pf)

    click.echo(f'Found {len(files_to_import)} eligible sample files.')
    cont = click.prompt('Do you want to continue? y/n', type=click.Choice(['Y', 'N'], case_sensitive=False),
                        show_choices=False)
    if cont.lower() == 'y':
        for f in files_to_import:
            app.import_sample(Path(f), type_, format_, gene_id_col, raw_count_col)
    else:
        sys.exit()


if __name__ == '__main__':
    register()
    cli()
