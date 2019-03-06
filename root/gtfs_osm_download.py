# """
# Logger for logging info and error messages both to the console and logger file named
# "Transit_israel_monthly_update_<current_date_time>.txt"
#
# """
import transitanalystisrael_config as cfg
import time
import sys
from dateutil import parser
import progressbar
import ftplib
import requests
from Logger import _log
import os
from pathlib import Path


size_iterator = 0 # used for the progress bar for download. not the best practice, but quick and dirty becaue of the ftp callback

def get_file_from_url_http(url, file_name, file_path, _log):
    """
    Downloads a file to the working directory
    :param url: HTTP utl to downloads from - not an FTP URL
    :return: file name of the downloaded content in the working directory
    """

    # Preparing file for fetching
    local_file_path_and_name = Path(os.getcwd()).parent / file_path / file_name
    _log.info("Going to download the latest osm from %s to %s", url, local_file_path_and_name)

    download_complete = False
    download_attempts = 1
    max_download_attemtps = 24

    while not download_complete:
        if not download_complete and 24 > download_attempts > 1:
            _log.error("%s is unreachable. Sleeping for 60 minutes and trying again. This is attempt %s out of "
                       "%s attempts", url, download_attempts, max_download_attemtps)
            time.sleep(60*60)
        if not download_complete and download_attempts > 24:
            _log.error("%s is unreachable for more than 24 hours. Aborting update", url)
            raise Exception
        download_attempts += 1

        try:
            r = requests.get(url, stream=True)
            file = open(local_file_path_and_name, 'wb')

            # Creating a progress bar
            size = int(r.headers['Content-Length'])
            pbar = createProgressBar(size)

            # Fetching
            global size_iterator
            size_iterator = 0
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file_write_update_progress_bar(chunk, file, pbar)
            file.close()
            pbar.finish()
            _log.info("Finished loading latest OSM to: %s", local_file_path_and_name)
            download_complete = True
            return

        except Exception as e:
            continue


def get_gtfs_file_from_url_ftp(url, file_name_on_server, _log):
    """
    Downloads a GTFS file from an FTP server to the working directory
    :param url: the FTP server URL that points to file's containing folder
    :param file_name_on_server: The file name on the FTP server
    :return: file name of the downloaded content in the working directory
    """
    _log.info("Going to download the latest GTFS from %s ", url)
    download_complete = False
    download_attempts = 1
    max_download_attemtps = 24

    while not download_complete:
        if not download_complete and 24 > download_attempts > 1:
            _log.error("%s is unreachable. Sleeping for 60 minutes and trying again. This is attempt %s out of "
                       "%s attempts", url, download_attempts, max_download_attemtps)
            time.sleep(60*60)
        if not download_complete and download_attempts > 24:
            _log.error("%s is unreachable for more than 24 hours. Aborting update", url)
            raise Exception
        download_attempts += 1

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
                    actual_time = parser.parse(time_str)
                    local_file_name = local_file_name + str(actual_time.strftime('%Y') +  actual_time.strftime('%m')
                                                            + actual_time.strftime('%d')) + ".zip"
                    size = float(tokens[2])

            pardir = Path(os.getcwd()).parent
            local_file_path_and_name = pardir / cfg.gtfspath / local_file_name
            # Generate a progress bar and download
            local_file = open(local_file_path_and_name, 'wb')
            pbar = createProgressBar(size)

            # Download
            global size_iterator
            size_iterator = 0
            ftp.retrbinary("RETR " + file_name_on_server, lambda data, : file_write_update_progress_bar(data, local_file, pbar))

            # Finish
            local_file.close()
            ftp.quit()
            pbar.finish()
            sys.stdout.flush()
            download_complete = True
            _log.info("Finished loading latest GTFS to: %s", local_file_path_and_name)
            return local_file_name

        except ftplib.all_errors as err:
            error_code = err.args[0]
            # file not found on server
            if error_code == 2:
                _log.error(file_name_on_server, "is not found on %s", url)
                raise err
            # Unvalid URL
            if error_code == 11001:
                _log.error("URL %s is not valid", url)
                continue



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


def file_write_update_progress_bar(data, dest_file, pbar):
    """
    Call back for writing fetched or processed data from FTP while updating the progress bar
    """
    global size_iterator
    size_iterator += len(data)
    dest_file.write(data)
    pbar.update(size_iterator)

# Download GTFS & OSM
def gtfs_osm_download():
    """
    Downloads osm and gtfs files from the web.
    :param _log:
    :return:
    """
    try:
        get_gtfs_file_from_url_ftp(cfg.gtfs_url, cfg.gtfs_file_name_on_mot_server, _log)
        # get_file_from_url_http(cfg.osm_url, cfg.osm_file_name, cfg.osmpath,  _log)
    except Exception as e:
        raise e

gtfs_osm_download()


