import os.path
import shutil
from pathlib import Path
from typing import Literal

import pandas as pd


def import_sample(filename: Path, sample_type: Literal['RNA-seq', 'scRNA-seq'],
                  file_format: Literal['flat', '2D'], gene_id_col: str, raw_count_col: str):
    workdir = f"{os.path.join(os.path.dirname(filename), 'workdir')}"
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    shutil.unpack_archive(filename, extract_dir=workdir)
    extracted_file_path = os.path.join(workdir, filename.stem)
    try:
        if sample_type == 'RNA-seq':
            if file_format == '2D':
                __import_rna_2d(extracted_file_path, gene_id_col)
            elif file_format == 'flat':
                __import_rna_flat(extracted_file_path, gene_id_col, raw_count_col)
            else:
                raise ValueError(f'invalid file format: {file_format}')
        elif sample_type == 'scRNA-seq':
            __import_sc_rna(filename)
        else:
            raise ValueError(f'unsupported sample type: {sample_type}')
    finally:
        shutil.rmtree(os.path.join(os.path.dirname(filename), "workdir"))


def __import_rna_2d(filepath: str, gene_id_col: str):
    df = pd.read_csv(filepath, sep='\t')
    if gene_id_col != 'gene_id':
        df = df.rename(columns={gene_id_col: "gene_id"})
    for sample_name in df.columns[1:]:
        sample_df = df[['gene_id', sample_name]].rename(columns={sample_name: 'raw_count'})
        sample_df.to_csv(f'{os.path.dirname(filepath)}/{sample_name}.csv', index=False)
        shutil.make_archive(f'{os.path.dirname(filepath)}/{sample_name}.csv', format='gz')
        # TODO: make API call
        os.remove(f'{os.path.dirname(filepath)}/{sample_name}.csv')
        os.remove(f'{os.path.dirname(filepath)}/{sample_name}.csv.gz')


def __import_rna_flat(filepath: str, gene_id_col: str, raw_count_col: str):
    df = pd.read_csv(filepath, sep='\t')
    df = df[[gene_id_col, raw_count_col]]
    if gene_id_col != 'gene_id':
        df = df.rename(columns={gene_id_col: "gene_id"})
    if raw_count_col != 'raw_count':
        df = df.rename(columns={raw_count_col: "raw_count"})
    df.to_csv(f'{os.path.splitext(filepath)[0]}.csv', index=False)
    shutil.make_archive(f'{os.path.splitext(filepath)[0]}.csv', format='gz')
    # TODO: make API call
    os.remove(f'{os.path.splitext(filepath)[0]}.csv')
    os.remove(f'{os.path.splitext(filepath)[0]}.csv.gz')


def __import_sc_rna(filename: Path):
    pass
