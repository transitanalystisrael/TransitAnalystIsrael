import docker
import ftplib
import json
import os
import platform
import progressbar
import requests
import subprocess
import sys
import time
import zipfile
import tarfile
import re
from io import BytesIO
from dateutil import parser
from scripts import gtfs2transfers
from scripts import send_email
from scripts import logger

_log = logger.get_logger()

def get_file_from_url_http(url):
    '''
    Donwloads a file to the working directory
    :param url:
    :return: the file's name
    '''
    _log.info("Going to download the latest osm from", url)
    r = requests.get(url, stream=True)
    local_file_name = "israel-and-palestine-latest.osm.pbf"
    file = open(local_file_name, 'wb')
    size = int(r.headers['Content-Length'])
    pbar = createProgressBar(size)
    # Download
    size_iterator = 0
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            file_write(chunk, file, pbar, size_iterator)
            size_iterator += 1
    file.close()
    pbar.finish()
    _log.info("Finished loading latest OSM to: ", local_file_name)
    return local_file_name

def createProgressBar(file_size):
    widgets = ['Downloading: ', progressbar.Percentage(), ' ',
               progressbar.Bar(marker='#', left='[', right=']'),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=file_size)
    pbar.start()
    return pbar


def file_write(data, dest_file, pbar, size_iterator):
    """
    Call back for writing the downlaoed data from FTP while updating the progress bar
    """
    dest_file.write(data)
    pbar.update(size_iterator)

def get_file_from_url_ftp(url, file_name_on_server):
    '''
    Donwloads a file to the working directory
    :param url:
    :param file_name_on_server:
    :return: the file name
    '''
    _log.info("Going to download the latest GTFS from", url)
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
                local_file_name = "GTFS-" + str(time.strftime('%b') + "-" + time.strftime('%y') + "shaked.zip")
                size = float(tokens[2])

        # Generate a progress bar and download
        local_file = open(local_file_name, 'wb')
        pbar = createProgressBar(size)
        # Download
        ftp.retrbinary("RETR " + file_name_on_server, lambda data: file_write(data, local_file, pbar, len(data)))

        # Finish
        local_file.close()
        ftp.quit()
        pbar.finish()
        sys.stdout.flush()

        _log.info("Finished loading latest GTFS to: ", local_file_name)
        return local_file_name

    except ftplib.all_errors as err:
        error_code = err.args[0]
        if error_code == 2:
            _log.error(file_name_on_server, "is not found on", url)
            ftp.quit()
        if error_code == 11001:
            _log.error("URL", url, "is not valid ")


def start_navitia_with_default_and_custom_coverage():
    pass


def copy_file_into_docker(container, dest_path, file_path, file_name):
    _log.info("Going to copy", file_name, "to", container.name, "@" + dest_path)
    file = open(file_path + '/' + file_name, 'rb')
    file = file.read()
    # Convert to tar file
    tar_stream = BytesIO()
    file_tar = tarfile.TarFile(fileobj=tar_stream, mode='w')
    tarinfo = tarfile.TarInfo(name=file_name)
    tarinfo.size = len(file)
    file_tar.addfile(tarinfo, BytesIO(file))
    file_tar.close()

    tar_stream.seek(0)
    success = container.put_archive(
        path=dest_path,
        data=tar_stream
    )
    if success:
        _log.info("Finished copying", file_name, "to", container.name, "@" + dest_path)



def copy_file_from_docker():
    pass


def get_docker_service_client():
    # TRAILS FOR RUNNING THE SERVICE
    # docker_run_command = "C:/Program Files/Docker/Docker/Docker for Windows.exe"
    # subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". \"./SamplePowershell\";", "&hello"])
    # subprocess.check_output('powershell Net start -ArgumentList  "com.docker.service" -Verb "runAs"',
    #                         shell=True)
    # _log.info(subprocess.check_output(["runas", "/noprofile", "/user:Administrator", "|", "echo", "shaked"]))

    # docker_run_command = "start-service *docker*"

    # proc = subprocess.Popen([docker_run_command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    # win32serviceutil.StartService(docker_run_command,None)
    docker_check_alive_cmd = "docker info"
    docker_is_up = False
    while not docker_is_up:
        docker_check_alive_process = subprocess.Popen(docker_check_alive_cmd, stdout=subprocess.PIPE, shell=True)
        output, error = docker_check_alive_process.communicate()
        docker_is_up = "Containers" in output.decode('utf-8')
    try:
        client = docker.from_env()
        return client
    except error:
        _log.error("Docker deamon service is not up")
        return None


def get_navitia_url_for_cov(cov_name):
    return "http://localhost:9191/v1/coverage/" + cov_name + "/status/"


def check_covereage_running(url, coverage_name):
    _log.info("checking if",coverage_name, "is up")
    response = requests.get(url)
    json_data = json.loads(response.text)
    if "status" not in json_data or "running" not in json_data["status"]["status"]:
        _log.error(coverage_name + " coverage is down")
    else:
        _log.info(coverage_name + " coverage is up")


def start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path,
                               navitia_docker_compose_file_name, extend_wait_time=False):
    '''
    :param secondary_custom_coverage_name:
    :param navitia_docker_compose_file_path:
    :param navitia_docker_compose_file_name:
    :param extend_wait_time: uLonger wait time is required when images are being re-downloaded, set True if needed
    :return:
    '''
    _log.info("Attempting to start Navitia with default coverage and ", secondary_custom_coverage_name, "coverage")
    navitia_docker_compose_file = open(navitia_docker_compose_file_path + navitia_docker_compose_file_name, mode='r')
    navitia_docker_compose_file_contents = navitia_docker_compose_file.read()
    navitia_docker_compose_file.close()

    if secondary_custom_coverage_name != "default" \
            and not secondary_custom_coverage_name in navitia_docker_compose_file_contents:
        _log.error("The custom configuration does not include a coverage area named: " + secondary_custom_coverage_name +
              ". Fix config, restart docker and start again")

    # run the custom cmopose and redirect logs while nuting the output
    navitia_docker_start_command = ["docker-compose", "-f", "docker-compose.yml", "-f", navitia_docker_compose_file_name, "up"]

    docker_start_up_process = subprocess.Popen(navitia_docker_start_command, cwd=navitia_docker_compose_file_path,
                                               stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    # output, error = docker_start_up_process.communicate()
    # print(output, error)
    if extend_wait_time:
        # Longer wait time is required because images are being re-downloaded
        t_wait = 60 * 5
    else:
        # wait 90 seconds for everything to go up
        t_wait = 120
    _log.info("Waiting", t_wait, "seconds to validate Navitia docker is up and running")
    time.sleep(t_wait)
    # Check if default and secondary_custom_coverage_name regions are up and running
    default_coverage_name = "default"
    check_covereage_running(get_navitia_url_for_cov(default_coverage_name), default_coverage_name)
    check_covereage_running(get_navitia_url_for_cov(secondary_custom_coverage_name), secondary_custom_coverage_name)


def move_one_graph_to_secondary(container, source_cov_name, dest_cov_name):
    command_list = "/bin/sh -c \"mv " + source_cov_name + ".nav.lz4 "+ dest_cov_name + ".nav.lz4\""
    exit_code, output = container.exec_run(cmd=command_list,  stdout=True, workdir="/srv/ed/output/")
    if exit_code != 0:
        _log.error("Couldn't change ", source_cov_name, " to ", dest_cov_name)
        raise Exception("STOP the program")
    _log.info("Changed the name of", source_cov_name + ".nav.lz4 ", "to", dest_cov_name + ".nav.lz4")


def copy_graph_to_local_host(container, coverage_name):
    # Create a local file for writing the incoming graph
    _log.info("Going to copy", coverage_name, ".nav.lz4 to", os.getcwd(), "on local host")
    local_graph_file = open('./' + coverage_name + '.nav.lz4', 'wb')
    bits, stat = container.get_archive('/srv/ed/output/' + coverage_name + '.nav.lz4')
    size = stat["size"]
    pbar = createProgressBar(size)
    # Download
    size_iterator = 0
    for chunk in bits:
        if chunk:
            file_write(chunk, local_graph_file, pbar, size_iterator)
            size_iterator += 1
    local_graph_file.close()
    pbar.finish()
    _log.info("Finished copying", coverage_name, ".nav.lz4 to", os.getcwd(), "on local host")


def copy_graph_from_remote_host_to_container(container, coverage_name):
    #THIS IS NOT IMPLEMENTED!
    # Create a local file for writing the incoming graph
    # _log.info(coverage_name + '.nav.lz4')
    # use copy_file_into_docker
    # success = container.put_archive('/srv/ed/output/', coverage_name + '.nav.lz4')
    # if success:
    #     _log.info("Finished copying ", coverage_name, ".nav.lz4 to ", container.name)
    pass

def delete_grpah_from_container(container, coverage_name):
    delete_command= "/bin/sh -c \"rm " + coverage_name +".nav.lz4\""
    exit_code, output = container.exec_run(cmd=delete_command,  stdout=True, workdir="/srv/ed/output/")
    if exit_code != 0:
        _log.error("Couldn't delete ", coverage_name, " graph")
        raise Exception("STOP the program")
    _log.info("Finished deleting graph", coverage_name, "from container ", container.name)


def stop_all_containers(docker_client):
    _log.info("Going to stop all Docker containers")
    for container in docker_client.containers.list():
        container.stop()
    _log.info("Stopped all Docker containers")


def generate_transfers_file(gtfs_file):
    # Unzip GTFS to get the stops.txt for processing
    with zipfile.ZipFile(gtfs_file, 'r') as zip_ref:
        zip_ref.extract(member="stops.txt")
    output_full_path = gtfs2transfers.generate_transfers(os.getcwd() + "/stops.txt")
    return output_full_path


def generate_gtfs_with_transfers(gtfs_file_name, gtfs_file_path):
    file = open(gtfs_file_path + '/' + gtfs_file_name, 'rb')
    gtfs_file = file.read()
    _log.info("Extracting stops.txt and computing transfers.txt")
    output_file_full_path = generate_transfers_file(gtfs_file)
    # transfers_file_full_path = os.getcwd() + "\\transfers.txt"
    with zipfile.ZipFile(gtfs_file, 'a') as zip_ref:
        zip_ref.write(output_file_full_path, os.path.basename(output_file_full_path))

    _log.info("Added transfers.txt to", gtfs_file)


def copy_osm_and_gtfs_to_default_cov(worker_con, osm_file_path, osm_file_name, gtfs_file_path, gtfs_file_name):
    copy_file_into_docker(worker_con, 'srv/ed/input/default', osm_file_path, osm_file_name)
    copy_file_into_docker(worker_con, 'srv/ed/input/default', gtfs_file_path, gtfs_file_name)


def clear_container_logs(con):
    clear_log_command = "sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' " + con.name + ")"
    subprocess.Popen(clear_log_command, shell=True)
    _log.info("Cleared", con.name, "logs")


def validate_osm_gtfs_convertion_to_graph_is_completed(worker_con, time_to_wait):
    '''
    Waits 15 minutes
    Validates that the following navitia tasks succeeded in the docker container:
    gtfs2ed, ed2nav
    :return:
    '''
    _log.info("Waiting", time_to_wait, "minutes to let OSM & GTFS conversions to lz4 graph takes place")
    time.sleep(time_to_wait)
    _log.info("I'm back! Verifying that the conversions took place")
    # Success status look like Task tyr.binarisation.ed2nav[feac06ca-51f7-4e39-bf1d-9541eaac0988] succeeded
    # and tyr.binarisation.gtfs2ed[feac06ca-51f7-4e39-bf1d-9541eaac0988] succeeded
    if re.compile(r"tyr\.binarisation\.gtfs2ed\[\S*\] succeeded").search(worker_con.logs().decode('utf-8'))\
            and re.compile(r'tyr\.binarisation\.gtfs2ed\[\S*\] succeeded').search(worker_con.logs().decode('utf-8')):
        _log.info("OSM conversion task ed2nav amd GTFS conversion task gtfs2ed are successful")
        return True
    else:
        _log.error("After", time_to_wait, "minutes - tasks aren't completed")
        return False



def validate_osm_gtfs_convertion_to_graph_is_running(docker_client, secondary_custom_coverage_name,
                                          navitia_docker_compose_file_path, navitia_docker_compose_file_name):
    # tyr_beat must be running as it manages the tasks for the worker, the latter generates the graph
    _log.info("Validating that tyr_beat is up and running")
    beat_con = docker_client.containers.list(filters={"name": "beat"})
    if not beat_con:
        # restarting tyr_beat
        _log.info("tyr_beat is down, attempting to re-run")
        tyr_beat_start_command = "docker-compose up tyr_beat"

        with open("tyr_beat_output.txt", "a+", encoding="UTF-8") as tyr_beat_output:
            subprocess.Popen(tyr_beat_start_command, cwd=navitia_docker_compose_file_path,
                                                shell=True, stdout=tyr_beat_output, stderr=tyr_beat_output)
        # Wait 10 seconds for it to come up
        _log.info("Waiting 10 seconds to see if tyr_beat is up")
        time.sleep(10)

        with open("tyr_beat_output.txt", "r", encoding="UTF-8") as tyr_beat_output:
            if "Sending due task udpate-data-every-30-seconds" not in tyr_beat_output.read():
                _log.info("tyr_beat is up and running")
                tyr_beat_output.close()
            # tyr_beat is malfunctioned, need to delete and re-download
            else:
                # stop all containers
                _log.info("Stopping all containers")
                stop_all_containers(docker_client)

                # delete container and image
                beat_con = docker_client.containers.list(all=True, filters={"name": "beat"})[0]
                beat_image = docker_client.images.list(name="navitia/tyr-beat")[0]
                beat_con_name = beat_con.name
                beat_image_id = beat_image.id
                beat_con.remove()
                _log.info(beat_con_name, "container is removed")
                docker_client.images.remove(beat_image.id)
                _log.info(beat_image_id, "image is removed")

                # re-run navitia docker-compose
                _log.info("Restarting docker with defauly coverage and custom coverage: ", secondary_custom_coverage_name)
                start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path,
                                           navitia_docker_compose_file_name, True)
    else:
        _log.info("Validated tyr_beat is up and running")


def send_log_to_email(subject, message):
    attached_file = logger.get_log_file_name()
    return send_email.create_msg_and_send_email(subject, message, attached_file)


def get_logger():
    return _log
