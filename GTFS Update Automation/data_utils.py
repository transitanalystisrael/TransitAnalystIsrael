import ftplib
import progressbar
import sys
from dateutil import parser
import utils
import requests
import datetime
import boto3
import logger

omd_url = "https://api.transitfeeds.com/v1/getFeedVersions?key="

def get_osm_latest_version(url):
    return get_file_from_url_http(url, "israel-and-palestine-latest.osm.pbf")


def get_file_from_url_http(url, local_dest_file_name):
    """
    Downloads a file to the working directory
    :param url: HTTP utl to downloads from - not an FTP URL
    :return: file name of the downloaded content in the working directory
    """

    # Preparing file for fetching
    _log = get_logger()
    _log.info("Going to download the latest %s from %s", local_dest_file_name, url)
    r = requests.get(url, stream=True)
    file = open(local_dest_file_name, 'wb')

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
    _log.info("Finished downloading: %s", local_dest_file_name)
    return local_dest_file_name


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


def get_gtfs_file_from_url_ftp(url, file_name_on_server):
    """
    Downloads a GTFS file from an FTP server to the working directory
    :param url: the FTP server URL that points to file's containing folder
    :param file_name_on_server: The file name on the FTP server
    :return: file name of the downloaded content in the working directory
    """
    _log = get_logger()
    _log.info("Going to download the latest GTFS from %s", url)
    try:
        # Connect to FTP
        ftp = ftplib.FTP(url)
        ftp.login()

        # Get the GTFS time stamp and generate local file name, "GTFS-Dec-18"
        file_lines = []
        local_file_name = ""
        size = 0

        ftp.dir("", file_lines.append)
        for line in file_lines:
            tokens = line.split(maxsplit=4)
            name = tokens[3]
            if name == file_name_on_server:
                time_str = tokens[0]
                time = parser.parse(time_str)
                local_file_name = "GTFS-" + str(time.strftime('%b') + "-" + time.strftime('%y') + ".zip")
                size = float(tokens[2])

        # Generate a progress bar and download
        local_file = open(local_file_name, 'wb')
        pbar = createProgressBar(size)

        # Download
        ftp.retrbinary("RETR " + file_name_on_server, lambda data: file_write_update_progress_bar(data, local_file, pbar, len(data)))

        # Finish
        local_file.close()
        ftp.quit()
        pbar.finish()
        sys.stdout.flush()

        _log.info("Finished loading latest GTFS to: %s", local_file_name)
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


def get_gtfs_list_from_omd():
    """
    :return: List of dates indicating different versions of GTFS by starting date
    """
    _log = get_logger()
    _log.info("Retrieving list of available GTFS versions from OpenMobilityData")
    omd_list_of_feeds_url = omd_url + get_omd_api_key() +'&feed=ministry-of-transport-and-road-safety%2F820&page=1&limit=500&err=1&warn=1'
    r = requests.get(omd_list_of_feeds_url, stream=True)
    response = r.json()
    # Building a list of start production dates for each GTFS version
    gtfs_dates_and_urls = []
    if response['status'] == "OK":
        versions = response['results']['versions']
        for version in versions:
            version_entry = {}
            version_entry['date'] = datetime.datetime.strptime(version['d']['s'], '%Y%m%d')
            version_entry['url'] = version['url']
            gtfs_dates_and_urls.append(version_entry)
        return gtfs_dates_and_urls
    else:
        _log.error("OMD (TransitFeeds) isn't available")


def get_gtfs_from_omd(url, date):
    """
    Get GTFS file from OMD according to given url
    :return: local file name of downlaoded GTFS
    """
    local_file_name = get_file_from_url_http(url, "GTFS-"+date)
    return local_file_name


def get_omd_api_key():
    # s3 = boto3.resource('s3')
    # keys_buckets = s3.Bucket('transit-analyst-key-bucket')
    omd_api_key = 'omd_api_key.txt'
    # keys_buckets.download_file(omd_api_key, omd_api_key)
    omd_api_key = open(omd_api_key, 'rb').read()

    omd_api_key = '5bbfcb92-9c9f-4569-9359-0edc6e765e9f'
    return omd_api_key


def get_logger():
    return utils.get_logger()


if __name__ == '__main__':
    # main()
    pass