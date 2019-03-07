# """
import transitanalystisrael_config as cfg

from logger import _log
import os
from pathlib import Path
import shutil
import codecs

def unzip_gtfs(gtfs_zip_file_name, gtfspath, _log):
    """
    Unzip gtfs to gtfspath
    """
    _log.info("Going to unzip %s file to %s", gtfs_zip_file_name, gtfspath)
    pardir = Path(os.getcwd()).parent
    dest_folder = pardir / gtfspath / gtfs_zip_file_name[:-4] # removing the .zip end
    if not os.path.exists(dest_folder):
         os.mkdir(dest_folder)
    gtfs_contets_folder = Path(os.getcwd()).parent / gtfspath / gtfs_zip_file_name
    shutil.unpack_archive(gtfs_contets_folder, extract_dir=dest_folder, format='zip')
    _log.info("Finished unzipping")


def remove_bom_characters_from_unzipped_files(gtfspath):
    """
    Sometimes the GTFS files are preceded with a BOM set of characters (\ufeff)
    This method remvoed them
    """
    BUFSIZE = 4096
    BOMLEN = len(codecs.BOM_UTF8)

    gtfs_contets_folder = Path(os.getcwd()).parent / gtfspath
    for file in os.listdir(gtfs_contets_folder):
        if ".txt" in file:
            with open( gtfs_contets_folder / file, "r+b") as fp:
                chunk = fp.read(BUFSIZE)
                if chunk.startswith(codecs.BOM_UTF8):
                    i = 0
                    chunk = chunk[BOMLEN:]
                    while chunk:
                        fp.seek(i)
                        fp.write(chunk)
                        i += len(chunk)
                        fp.seek(BOMLEN, os.SEEK_CUR)
                        chunk = fp.read(BUFSIZE)
                    fp.seek(-BOMLEN, os.SEEK_CUR)
                    fp.truncate()


# Unzip GTFS
def gtfs_unzip():
    """
    Unzip GTFS and remove BOM charcters that interrupt with reasing the file
    :param _log:
    :return:
    """
    try:
        gtfs_zip_file_name = cfg.gtfsdirbase + cfg.gtfsdate + ".zip"
        unzip_gtfs(gtfs_zip_file_name, cfg.gtfspath, _log)
        remove_bom_characters_from_unzipped_files(os.path.join(cfg.gtfspath, cfg.gtfsdirbase+cfg.gtfsdate))
    except Exception as e:
        raise e

gtfs_unzip()


