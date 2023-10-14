#!/usr/bin/env python

import logging
import os
from pathlib import Path
from typing import Literal

import click
import pandas as pd
from alive_progress import alive_bar

import app
from app.common import has_active_runtime
from registry import register

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logging.basicConfig(level=logging.INFO)


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
def list_gene_models():
    auth_config = app.get_auth()
    gene_models = app.list_gene_models(auth_config)
    for gm in gene_models:
        click.echo(gm.name)


@cli.command()
def list_assemblies():
    auth_config = app.get_auth()
    assemblies = app.list_assemblies(auth_config)
    for a in assemblies:
        click.echo(a)


@cli.command()
@click.option('-org', '--organism', 'organism',
              type=click.Choice(['human', 'mouse', 'rat'], case_sensitive=True),
              required=True, help='Organism: one of human, mouse, or rat')
@click.option('-a', '--assembly', 'assembly', type=str, required=True,
              help='Genome assembly: run "list-assemblies" to view supported options')
@click.option('-gm', '--gene_model', 'gene_model', type=str, required=False,
              help='Gene model: run "list-gene-models" to view supported options')
@click.option('-t', '--type', 'type_',
              type=click.Choice(['Microarray', 'RNA-seq', 'scRNA-seq', 'snRNA-seq'], case_sensitive=True),
              required=True, help='Sample type: one of Microarray, RNA-seq, or scRNA-seq')
@click.option('-g', '--gene_col', type=str,
              help='The name of the column representing the gene symbol. '
                   'If your sample use gene IDs, please provide a gene model as well.')
@click.option('-rc', '--raw_count_col', type=str,
              help='RNA-seq only: The name of the column representing the raw count.')
@click.option('-tpm', '--tpm_count_col', type=str,
              help='RNA-seq only: The name of the column representing the TPM count.')
@click.option('-fpkm', '--fpkm_count_col', type=str,
              help='RNA-seq only: The name of the column representing the TPM count.')
@click.option('-i', '--input_dir', type=str, help='Absolute path to sample files.', required=True)
@click.option('-o', '--output_file', type=str, help='Absolute path to where the sample sheet will be created.',
              required=False)
def generate_sample_sheet(organism: Literal['human', 'mouse', 'rat'], assembly: str, gene_model: str,
                          type_: Literal['Microarray', 'RNA-seq', 'scRNA-seq', 'snRNA-seq'],
                          gene_col: str, raw_count_col: str, tpm_count_col: str, fpkm_count_col: str,
                          input_dir: str, output_file: str):
    files_to_import = []
    for f in os.listdir(input_dir):
        pf = Path(os.path.join(input_dir, f))
        if pf.suffix in ['.zip', '.gz']:
            files_to_import.append(pf)

    click.echo(f'Found {len(files_to_import)} eligible sample files.')
    app.generate_sample_sheet(organism, assembly, gene_model, type_,
                              gene_col, raw_count_col, tpm_count_col, fpkm_count_col,
                              files_to_import, output_file)


@cli.command()
@click.option('-pid', '--project_id', type=int, help='The ID of the project to which to add these samples.')
@click.option('-ss', '--sample_sheet', type=str, help='Absolute path to the sample sheet.', required=True)
@click.option('-d', '--dry_run', is_flag=True, default=False, help='Dry run.')
def upload_samples(project_id: int, sample_sheet: str, dry_run: bool):
    """Example usage: px upload-samples -pid 1 -ss /home/user/sample_sheet.csv"""

    auth_config = app.get_auth()
    ok = has_active_runtime(auth_config)

    if ok:
        sample_sheet = pd.read_csv(sample_sheet)
        failed_files = []
        with alive_bar(sample_sheet.shape[0]) as bar:
            for i in range(0, sample_sheet.shape[0]):
                try:
                    if not dry_run:
                        app.upload_sample(auth_config, sample_sheet.iloc[i], project_id)
                except:
                    logging.exception(f'error uploading sample {sample_sheet.iloc[i]["file"]}')
                    failed_files.append(sample_sheet.iloc[i]["file"])
                bar()

        if len(failed_files) > 0:
            click.echo(f"{len(failed_files)} sample files failed to upload")
            for f in failed_files:
                click.echo(f)
            click.echo(f"Check the logs for more details")
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
