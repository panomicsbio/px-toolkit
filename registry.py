import gzip
import os
import re
import shutil


def gunzip(gzipped_file_name, work_dir):
    """gunzip the given gzipped file"""

    # see warning about filename
    filename = os.path.split(gzipped_file_name)[-1]
    filename = re.sub(r"\.gz$", "", filename, flags=re.IGNORECASE)

    with gzip.open(gzipped_file_name, 'rb') as f_in:
        with open(os.path.join(work_dir, filename), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def gzip_archive(file_name, work_dir, dry_run: bool = False, logger=None, owner=None, group=None):
    """gunzip the given file"""
    with open(file_name, "rb") as f:
        data = f.read()
    bindata = bytearray(data)
    archive_name = f"{file_name}.gz"
    with gzip.open(f"{os.path.join(work_dir, archive_name)}", "wb") as f:
        f.write(bindata)


def register():
    shutil.register_unpack_format('gz', ['.gz'], gunzip)
    shutil.register_archive_format('gz', gzip_archive)
