# """
# Logger for logging info and error messages both to the console and logger file named
# "Transit_israel_monthly_update_<current_date_time>.txt"
#
# """
import transitanalystisrael_config as cfg
import sys
from dateutil import parser
import progressbar
import ftplib
import requests
from Logger import _log
import os
from pathlib import Path
import shutil
import codecs

def get_file_from_url_http(url, file_name, file_path, _log):
    """
    Downloads a file to the working directory
    :param url: HTTP utl to downloads from - not an FTP URL
    :return: file name of the downloaded content in the working directory
    """

    # Preparing file for fetching
    local_file_path_and_name = os.path.join(file_path, file_name)
    _log.info("Going to download the latest osm from %s to %s", url, local_file_path_and_name)
    r = requests.get(url, stream=True)
    file = open(local_file_path_and_name, 'wb')

    # Creating a progress bar
    size = int(r.headers['Content-Length'])
    pbar = createProgressBar(size)

    # Fetching
    size_iterator = 0
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            file_write_update_progress_bar(chunk, file, pbar, size_iterator)
            size_iterator += 1
    file.close()
    pbar.finish()
    _log.info("Finished loading latest OSM to: %s", local_file_path_and_name)

def get_gtfs_file_from_url_ftp(url, file_name_on_server, _log):
    """
    Downloads a GTFS file from an FTP server to the working directory
    :param url: the FTP server URL that points to file's containing folder
    :param file_name_on_server: The file name on the FTP server
    :return: file name of the downloaded content in the working directory
    """
    _log.info("Going to download the latest GTFS from %s ", url)
    try:
        # Connect to FTP
        ftp = ftplib.FTP(url)
        ftp.login()
        # Get the GTFS time stamp and generate local file name, "israel20190225"
        file_lines = []
        size = 0

        local_file_name = cfg.gtfsdirbase
        ftp.dir("", file_lines.append)
        for line in file_lines:
            tokens = line.split(maxsplit=4)
            name = tokens[3]
            if name == file_name_on_server:
                time_str = tokens[0]
                time = parser.parse(time_str)
                local_file_name = local_file_name + str(time.strftime('%Y') +  time.strftime('%m') + time.strftime('%d')) + ".zip"
                size = float(tokens[2])

        local_file_path_and_name = os.path.join(cfg.gtfspath, local_file_name)
        # Generate a progress bar and download
        local_file = open(local_file_path_and_name, 'wb')
        pbar = createProgressBar(size)

        # Download
        ftp.retrbinary("RETR " + file_name_on_server, lambda data: file_write_update_progress_bar(data, local_file, pbar, len(data)))

        # Finish
        local_file.close()
        ftp.quit()
        pbar.finish()
        sys.stdout.flush()

        _log.info("Finished loading latest GTFS to: %s", local_file_path_and_name)

        return local_file_name

    except ftplib.all_errors as err:
        error_code = err.args[0]
        # file not found on server
        if error_code == 2:
            _log.error(file_name_on_server, "is not found on %s", url)
            ftp.quit()
        # Unvalid URL
        if error_code == 11001:
            _log.error("URL %s is not valid", url)


def createProgressBar(file_size, action='Downloading: '):
    """
    Craeting a progress bar for continious tasks like downloading file or processing data
    :param file_size: the total size of the file to set the 100% of the bar
    :param action: type of action for the progress bar description, default is "Downloading: "
    :return: a progress bar object
    """
    widgets = [action, progressbar.Percentage(), ' ',
               progressbar.Bar(marker='#', left='[', right=']'),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=file_size)
    pbar.start()
    return pbar


def file_write_update_progress_bar(data, dest_file, pbar, size_iterator):
    """
    Call back for writing fetched or processed data from FTP while updating the progress bar
    """
    dest_file.write(data)
    pbar.update(size_iterator)


def unzip_gtfs(gtfs_zip_file_name, gtfspath, _log):
    """
    Unzip gtfs to gtfspath
    """
    _log.info("Going to unzip %s file to %s", gtfs_zip_file_name, gtfspath)
    # zip_ref = zipfile.ZipFile(os.path.join(gtfspath, gtfs_zip_file_name), 'r')
    dest_folder = Path(gtfspath) / gtfs_zip_file_name[:-4] # removing the .zip end
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    shutil.unpack_archive(os.path.join(gtfspath, gtfs_zip_file_name), extract_dir=dest_folder, format='zip')
    # zip_ref.extractall(dest_folder)
    _log.info("Finished unzipping")
    # zip_ref.close()


def remove_bom_characters_from_unzipped_files(gtfspath):
    """
    Sometimes the GTFS files are preceded with a BOM set of characters (\ufeff)
    This method remvoed them
    """
    BUFSIZE = 4096
    BOMLEN = len(codecs.BOM_UTF8)

    for file in os.listdir(gtfspath):
        if ".txt" in file:
            with open(os.path.join(gtfspath,file), "r+b") as fp:
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


# Download GTFS & OSM
def gtfs_osm_download():
    """
    Downloads osm and gtfs files from the web. Also unzipps GTFS into cfg.gtfs_osm_download
    :param _log:
    :return:
    """
    get_gtfs_file_from_url_ftp(cfg.gtfs_url, cfg.gtfs_file_name_on_mot_server, _log)
    gtfs_zip_file_name = cfg.gtfsdirbase + cfg.gtfsdate + ".zip"
    unzip_gtfs(gtfs_zip_file_name, cfg.gtfspath, _log)
    remove_bom_characters_from_unzipped_files(os.path.join(cfg.gtfspath, cfg.gtfsdirbase+cfg.gtfsdate))
    get_file_from_url_http(cfg.osm_url, cfg.osm_file_name, cfg.osmpath,  _log)


gtfs_osm_download()


